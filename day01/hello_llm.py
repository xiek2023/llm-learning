
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. 加载项目根目录中的 .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model_name = os.getenv("OPENAI_MODEL")

# 2. 检查必要配置
if not api_key:
    raise ValueError("缺少 OPENAI_API_KEY，请检查 .env 文件")

if not model_name:
    raise ValueError("缺少 OPENAI_MODEL，请检查 .env 文件")

# 3. 创建大模型客户端
llm = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url or None,
    temperature=0.3,
)

# 4. 构造消息
messages = [
    SystemMessage(
        content="你是一名 Python 和云计算技术专家，请用中文简洁回答问题。"
    ),
    HumanMessage(
        content="请用三句话介绍什么是 Elasticsearch。"
    ),
]

# 5. 调用模型
response = llm.invoke(messages)

# 6. 输出结果
print("大模型回答：")
print(response.content)
