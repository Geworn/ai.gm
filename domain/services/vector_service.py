from typing import List
from langchain_core.documents import Document
from domain.ports.vector_port import VectorPort
from langchain_core.vectorstores import VectorStore

class VectorService:
    def __init__(self , vector_port : VectorPort):
        self.vector_port = vector_port

    def embed_and_store_docs(self, splits: List[Document], user_id: str):
        return self.vector_port.embed_and_store_docs(splits, user_id)
    
    def vectorstore(self, user_id: str)->VectorStore:
        return self.vector_port.vectorstore(user_id)
    
    def delete_stored_docs(self, user_id: str, doc_ids: List[str]):
        return self.vector_port.delete_stored_docs(user_id, doc_ids)