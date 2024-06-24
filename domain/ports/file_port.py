from abc import ABC, abstractmethod
from fastapi import UploadFile
from typing import Union, Iterable

class FilePort(ABC):
    """
    An abstract base class that defines the interface for file-related operations.

    Subclasses of this class should provide their own implementation of the abstract methods,
    tailored to the specific storage solution they are using (e.g., local file system, cloud storage, database).
    """

    @abstractmethod
    def get(self, user_id: str, file_name: str) -> Union[bytes, None]:
        """
        Retrieves the contents of a file for the given user and file name.

        Args:
            user_id (str): The ID of the user whose file is being retrieved.
            file_name (str): The name of the file to be retrieved.

        Returns:
            Union[bytes, None]: The contents of the file as a bytes object, or None if the file is not found.
        """
        pass

    @abstractmethod
    def save(self, user_id: str, file: UploadFile) -> str:
        """
        Saves a file for the given user.

        Args:
            user_id (str): The ID of the user whose file is being saved.
            file (UploadFile): The file data to be saved.
            
        Returns:
            str: The pathname of the saved file.
        """
        pass

    @abstractmethod
    def delete(self, user_id: str, file_name: str) -> bool:
        """
        Deletes a file for the given user and file name.

        Args:
            user_id (str): The ID of the user whose file is being deleted.
            file_name (str): The name of the file to be deleted.
        """
        pass

    @abstractmethod
    def list(self, user_id: str) -> Iterable[str]:
        """
        Returns a list of all files associated with the given user.

        Args:
            user_id (str): The ID of the user whose files are being listed.

        Returns:
            Iterable[str]: An iterable (e.g., list, generator) containing the names of all files for the specified user.
        """
        pass
