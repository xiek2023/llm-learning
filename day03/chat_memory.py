
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

# 1. 加载配置
project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model_name = os.getenv("OPENAI_MODEL")

if not api_key or not model_name:
    raise ValueError("请检查 .env 配置")

# 2. 初始化模型
llm = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url or None,
    temperature=0.3,
)

# 3. 定义包含历史消息的提示词
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
你是一名 Python、FastAPI 和云平台技术助手。
请使用中文回答。
如果用户的问题依赖之前的对话，请结合历史消息理解。
如果历史中没有相关信息，不要假装记得。
"""
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

# 4. 组合调用链
chain = prompt | llm | StrOutputParser()

# 5. 保存当前会话历史
history = []


def chat(question: str) -> str:
    if not question.strip():
        raise ValueError("问题不能为空")

    # 先请求模型，成功后再更新历史
    answer = chain.invoke({
        "history": history,
        "question": question,
    })

    history.extend([
        HumanMessage(content=question),
        AIMessage(content=answer),
    ])

    return answer


if __name__ == "__main__":
    print("=== 多轮聊天助手 ===")
    print("输入 /reset 清空对话，输入 exit 退出。")

    while True:
        question = input("\n你：").strip()

        if question.lower() in ("exit", "quit"):
            print("聊天结束。")
            break

        if question == "/reset":
            history.clear()
            print("当前会话历史已清空。")
            continue

        try:
            answer = chat(question)
            print(f"\n助手：{answer}")
        except Exception as exc:
            print(f"\n调用失败：{type(exc).__name__}: {exc}")
