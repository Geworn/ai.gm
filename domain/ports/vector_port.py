from abc import ABC, abstractmethod
from typing import List, Optional
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore

class VectorPort(ABC):
    """
    An abstract base class that defines the interface for a vector storage port.
    
    This class provides two abstract methods:
    
    1. `embed_and_store_docs(splits: List[Document], user_id: str)`:
       This method is responsible for embedding a list of `Document` objects
       and storing them in the vector store for the given `user_id`.
    
    2. `vectorstore(user_id: str) -> VectorStore`:
       This method returns the `VectorStore` instance for the given `user_id`.
    """
    
    @abstractmethod
    def embed_and_store_docs(splits: List[Document], user_id: str):
        """
        Embed and store a list of documents in the vector store for the given user.
        
        Args:
            splits (List[Document]): A list of `Document` objects to be embedded and stored.
            user_id (str): The ID of the user for whom the documents should be stored.
        """
        pass
    
    @abstractmethod
    def vectorstore(user_id: str) -> VectorStore:
        """
        Retrieve the `VectorStore` instance for the given user.
        
        Args:
            user_id (str): The ID of the user whose `VectorStore` instance should be returned.
        
        Returns:
            VectorStore: The `VectorStore` instance for the given user.
        """
        pass
    
    @abstractmethod
    def delete_stored_docs(user_id: str , ids):
        """
        Delete stored documents from the vector store for the given user.

        Args:
            user_id (str): The ID of the user whose documents should be deleted.
            ids (List[str]): A list of document IDs to be deleted.
        """
        pass