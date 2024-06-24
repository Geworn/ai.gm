from domain.ports.file_port import FilePort
from fastapi import UploadFile

class FileService:
    def __init__(self , file_port : FilePort) -> None:
        self.file_port = file_port
        pass
    
    def get(self, user_id : str, file_name : str):
        return self.file_port.get(user_id , file_name)
    
    def save(self, user_id : str, file : UploadFile):
        return self.file_port.save(user_id ,file)
    
    def delete(self, user_id : str, file_name : str):
        return self.file_port.delete(user_id , file_name)
    
    def list(self, user_id : str):
        return self.file_port.list(user_id)