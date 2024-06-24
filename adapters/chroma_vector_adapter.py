__import__('pysqlite3')
import sys

from langchain_core.vectorstores import VectorStore
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from typing import List
from langchain_core.documents import Document
from domain.ports.vector_port import VectorPort
from langchain_chroma import Chroma
# from langchain_openai import OpenAIEmbeddings
from langchain_core.embeddings import Embeddings

class ChromaVectorAdapter(VectorPort):
    def __init__(self, embedding_model: Embeddings, persist_directory : str = "./vector_db"):
        self.vector_store = Chroma
        self.persist_directory = persist_directory
        self.embedding_function = embedding_model

    def embed_and_store_docs(self, splits: List[Document], user_id: str):
        vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=self.embedding_function,
                persist_directory=self.persist_directory,
                collection_name=f"user_{user_id}"
        )
        return vectorstore 
    
    def vectorstore(self, user_id: str) -> VectorStore:
        return Chroma(persist_directory=self.persist_directory, collection_name=f"user_{user_id}",embedding_function=self.embedding_function)
    
    def delete_stored_docs(self, user_id: str, ids):
        self.vectorstore(user_id).delete(ids)
        return super().delete_stored_docs(ids)