fastapi快速开始的一个学习项目

安装依赖包 

conda env list

conda activate worldquant

conda install python-dotenv langchain langchain-openai

 
整个过程可以理解为：
Python 程序
    │
    ├── 加载 API 配置
    ├── 创建 ChatOpenAI 客户端
    ├── 组织 SystemMessage + HumanMessage
    │
    ▼
LangChain
    │
    ▼
云端模型 API
    │
    ▼
模型生成回答
    │
    ▼
response.content




来自极维空间 https://jiweisys.com/
