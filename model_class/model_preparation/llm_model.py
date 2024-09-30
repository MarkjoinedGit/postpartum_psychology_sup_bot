from langchain_openai import ChatOpenAI
def get_chat_llm():
    return ChatOpenAI(base_url="http://zep.hcmute.fit/7500/v1", api_key="llama.cpp")