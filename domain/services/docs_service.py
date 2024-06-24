from domain.ports.docs_port import DocsPort
from typing import List
from langchain_core.documents import Document

class DocsService:
    
    def __init__(self, docs_port : DocsPort):
        self.docs_port = docs_port

    def load(self, path: str , content_type: str):
        return self.docs_port.load(path, content_type)
    
    def split(self, docs: List[Document]):
        return self.docs_port.split(documents=docs)