from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOllama(
    model="qwen2.5-coder:3b",
    temperature=0.7,
)

# system prompt
messages = [
    SystemMessage(content="You are a helpful assistant that helps translate English to french."),
    HumanMessage(content="Hello, how are youu?"),
]

response = llm.invoke(messages)

print(response.content)