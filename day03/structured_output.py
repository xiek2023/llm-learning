
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 1. 加载配置
project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model_name = os.getenv("OPENAI_MODEL")

if not api_key or not model_name:
    raise ValueError("请检查 .env 中的 API Key 和模型名称")


# 2. 定义结构化输出的数据模型
class FaultAnalysis(BaseModel):
    """技术故障分析结果。"""

    error_type: str = Field(
        description="故障类型，例如 ModuleNotFoundError"
    )
    root_cause: str = Field(
        description="最可能的故障原因；信息不足时明确说明"
    )
    solutions: list[str] = Field(
        description="按顺序排列的排查或解决步骤"
    )
    severity: Literal["low", "medium", "high"] = Field(
        description="故障严重程度：低、中、高"
    )
    needs_more_info: bool = Field(
        description="是否需要用户补充信息"
    )


# 3. 初始化模型
llm = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url or None,
    temperature=0,
)

# 4. 将模型配置为结构化输出
structured_llm = llm.with_structured_output(FaultAnalysis)

# 5. 定义提示词
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
你是一名资深 Python 和云平台技术支持工程师。

请根据用户提供的故障信息分析问题，并返回符合指定结构的数据。
不要把猜测当作已确认事实。
如果证据不足，请在 root_cause 中说明不确定性，
并在 needs_more_info 中反映是否需要补充信息。
severity 只能是 low、medium、high 之一。
"""
    ),
    ("human", "请分析以下故障：\n{issue}"),
])

# 6. 组合调用链
chain = prompt | structured_llm


def analyze_fault(issue: str) -> FaultAnalysis:
    if not issue.strip():
        raise ValueError("故障描述不能为空")

    return chain.invoke({"issue": issue})


if __name__ == "__main__":
    issue = (
        "运行 FastAPI 项目时报错："
        "ModuleNotFoundError: No module named 'sqlalchemy'"
    )

    try:
        result = analyze_fault(issue)

        print("=== 结构化分析结果 ===")
        print(result.model_dump_json(indent=2))

        print("\n=== 单独读取字段 ===")
        print("故障类型：", result.error_type)
        print("可能原因：", result.root_cause)
        print("严重程度：", result.severity)

        print("\n=== 解决步骤 ===")
        for index, solution in enumerate(result.solutions, start=1):
            print(f"{index}. {solution}")

    except Exception as exc:
        print(f"分析失败：{type(exc).__name__}: {exc}")
