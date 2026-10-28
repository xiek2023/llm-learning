
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. 加载项目根目录的 .env
project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model_name = os.getenv("OPENAI_MODEL")

if not api_key or not model_name:
    raise ValueError("请检查 .env 中的 API Key 和模型名称")

# 2. 初始化云端大模型
llm = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url or None,
    temperature=0.3,
)

# 3. 创建提示词模板
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "你是一名专业的{role}。"
        "请使用中文回答，表达清晰，并尽量给出实际例子。"
    ),
    (
        "human",
        "请回答以下问题：{question}"
    ),
])

# 4. 创建输出解析器
parser = StrOutputParser()

# 5. 组合调用链
chain = prompt | llm | parser

# 6. 调用整个链
result = chain.invoke({
    "role": "Python 技术专家",
    "question": "什么是 FastAPI？它适合什么场景？",
})

# 7. 输出结果
print("=== LangChain 调用链演示 ===")
print(result)
