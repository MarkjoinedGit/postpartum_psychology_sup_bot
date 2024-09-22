from model_preparation.llm_model import get_chat_llm
from model_preparation.VectorDB import VectorDB
from model_preparation.Offline_RAG import Offline_RAG
import time

def build_rag_chain():
    llm = get_chat_llm()
    retriever = VectorDB().get_retriever()
    off_rag = Offline_RAG(llm)
    rag_chain = off_rag.get_chain(retriever)
    return rag_chain, off_rag

def run_rag_chain(rag_chain, off_rag, question):
    response = rag_chain.invoke(off_rag.get_input_data(question))
    #print(f"History: {response['chat_history']}")
    off_rag.add_history(question, response["answer"])
    return response

