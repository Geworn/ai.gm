from langchain_core.vectorstores import VectorStore
from typing import List
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from domain.ports.vector_port import VectorPort
from langchain_elasticsearch import ElasticsearchStore
from elasticsearch import Elasticsearch

class ElasticsearchVectorAdapter(VectorPort):
    def __init__(self, embedding_model: Embeddings, index_name: str = "vector_index"):
        self.index_name = index_name
        self.embedding_function = embedding_model
        self.es = Elasticsearch("http://localhost:9200")

    def create_index_if_not_exists(self, index_name: str):
        if not self.es.indices.exists(index=index_name):
            mappings = {
                "mappings": {
                    "properties": {
                        "vector": {
                            "type": "dense_vector",
                            "dims": 768  # ปรับตามขนาดของเวคเตอร์ที่คุณใช้
                        }
                    }
                }
            }
            self.es.indices.create(index=index_name, body=mappings)
            print(f"Index {index_name} created with mappings.")

    def vectorstore(self, user_id: str) -> VectorStore:
        index_name = f"user_{user_id}_{self.index_name}"
        self.create_index_if_not_exists(index_name)
        return ElasticsearchStore(index_name=index_name, embedding=self.embedding_function, es_url="http://localhost:9200")

    def embed_and_store_docs(self, splits: List[Document], user_id: str):
        vectorstore = self.vectorstore(user_id).from_documents(
            documents=splits,
            embedding=self.embedding_function,
        )
        return vectorstore
