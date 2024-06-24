from typing import Iterable, List
from langchain_core.documents import Document
from domain.ports.docs_port import DocsPort
from langchain_community.document_loaders import (
    PyPDFLoader, UnstructuredMarkdownLoader, UnstructuredWordDocumentLoader, CSVLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocsAdapter(DocsPort):
    def load(self, path: str, content_type: str):
            if content_type == "application/pdf":
                loader = PyPDFLoader(path)
            elif content_type == "text/markdown":
                loader = UnstructuredMarkdownLoader(path)
            elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                loader = UnstructuredWordDocumentLoader(path)
            elif content_type == "text/csv":
                loader = CSVLoader(path)
            else:
                raise ValueError(f"Unsupported file type: {content_type}")
            return loader.load()
        
    def split(self, documents: Iterable[Document]) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return text_splitter.split_documents(documents)
