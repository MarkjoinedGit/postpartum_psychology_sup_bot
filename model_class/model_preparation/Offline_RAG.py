from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain

class Offline_RAG:
    def __init__(self, llm) -> None:
        self.llm = llm

        self.history_chat =[]
        
        condense_question_template = """
        Với đoạn hội thoại sau và một câu hỏi tiếp theo, hãy diễn đạt lại câu hỏi tiếp theo để nó trở thành một câu hỏi độc lập.
        
        Lịch sử hội thoại:
        {chat_history}
        Câu hỏi tiếp theo: {question}
        Câu hỏi độc lập:"""
        
        self.condense_question_prompt = ChatPromptTemplate.from_template(condense_question_template)

        qa_template = """
        Bạn là trợ lý AI hỗ trợ về sức khoẻ tâm lý sau sinh. 
        Dựa vào nội dung gợi ý trả lời bên dưới, hãy đưa ra câu trả lời và lời khuyên phù hợp cho câu hỏi của họ.
        Nếu bạn không biết câu trả lời, hãy nói không biết, đừng cố tạo ra câu trả lời.

        Lịch sử hội thoại:
        {chat_history}

        Nội dung gợi ý trả lời:
        {context}

        Câu hỏi: {question}
        """

        self.qa_prompt = ChatPromptTemplate.from_template(qa_template)

    def get_chain(self, retriever):
        rag_chain = ConversationalRetrievalChain.from_llm(
            self.llm,
            retriever,
            condense_question_prompt=self.condense_question_prompt,
            combine_docs_chain_kwargs={
                "prompt": self.qa_prompt,
            },
            return_source_documents=True,
        )
        return rag_chain
    
    def add_history(self, user_chat, bot_chat):
        self.history_chat.append(("user", user_chat))
        self.history_chat.append(("assistant", bot_chat))
        if len(self.history_chat) > 5:
            self.history_chat.pop(0)
    
    def get_input_data(self,question):
        return {
            "chat_history": self.history_chat,
            "question": question
        }