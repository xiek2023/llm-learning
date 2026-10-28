
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model_name = os.getenv("OPENAI_MODEL")

if not api_key or not model_name:
    raise ValueError("请检查 .env 配置")

llm = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url or None,
    temperature=0.2,
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
你是一名资深 Python 后端和云平台技术支持工程师。

请根据用户提供的故障信息进行分析。
回答必须包含以下四个部分：
1. 问题原因
2. 排查步骤
3. 解决方案
4. 验证方法

如果信息不足，请明确指出需要补充什么。
不要编造不存在的日志或执行结果。
"""
    ),
    (
        "human",
        "请分析以下技术问题：\n{issue}"
    ),
])

chain = prompt | llm | StrOutputParser()


def analyze_issue(issue: str) -> str:
    """分析一段技术故障描述并返回文本结果。"""
    return chain.invoke({"issue": issue})


def main():
    print("=== 技术问题分析助手 ===")
    print("输入 exit 退出。")

    while True:
        issue = input("\n请输入故障描述：").strip()

        if issue.lower() in ("exit", "quit"):
            break

        if not issue:
            print("故障描述不能为空。")
            continue

        try:
            result = analyze_issue(issue)
            print("\n=== 分析结果 ===")
            print(result)
        except Exception as exc:
            print(f"调用失败：{type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
