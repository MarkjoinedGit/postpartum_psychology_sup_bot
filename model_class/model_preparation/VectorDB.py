import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
class VectorDB:
    def __init__(self,
                 embedding = HuggingFaceEmbeddings()) -> None:
        os.environ['PINECONE_API_KEY'] = "73bdec39-1f93-47fc-bd2f-f02883d7be83"
        self.pinecone_api_key = os.getenv('PINECONE_API_KEY')
        self.embedding = embedding
        self.db = self._build_db()
    
    def _build_db(self):
        db = PineconeVectorStore.from_existing_index(
            index_name="docs-rag-chatbot",
            namespace="docs-store",
            embedding=self.embedding
        )
        return db
    
    # tính similarity
    def get_retriever(self,
                      search_type: str = "similarity",
                      search_kwargs: dict = {"k": 5}
                      ):
        retriever =self.db.as_retriever(search_type=search_type,
                                        search_kwargs=search_kwargs)
        return retriever