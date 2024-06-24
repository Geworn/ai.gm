from abc import ABC, abstractmethod
from typing import List , Iterable
from langchain_core.documents import Document

class DocsPort(ABC):
    @abstractmethod
    def load(self, path: str , content_type: str)-> List[Document]:
        pass
    
    @abstractmethod
    def split(self, documents: Iterable[Document])-> List[Document]:
        """Split documents."""
        pass