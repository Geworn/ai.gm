from domain.ports.file_port import FilePort
from pathlib import Path
from fastapi import UploadFile

class FileAdapter(FilePort):
    def __init__(self, base_directory: str = "./files"):
        self.file: Path = Path(base_directory)
        self.file.mkdir(parents=True, exist_ok=True)  # Ensure the base directory exists

    def get(self, user_id: str, file_name: str):
        file_path = self.file / user_id / file_name
        if file_path.exists():
            with open(file_path, 'rb') as buffer:
                return buffer.read()
        else:
            return None

    def save(self, user_id: str, file: UploadFile) -> str:
        path_to_save = self.file / user_id
        path_to_save.mkdir(parents=True, exist_ok=True)

        file_path = path_to_save / file.filename  # Define the full path including the filename
        try:
            with file_path.open('wb') as buffer:
                buffer.write(file.file.read())
        except Exception as e:
            # Handle any exceptions that may occur
            print(f"Error saving file: {e}")
            return ""

        return str(file_path)

    def delete(self, user_id: str, file_name: str):
        file_path = self.file / user_id / file_name
        if file_path.exists():
            file_path.unlink()
            return True
        else:
            return False

    def list(self, user_id: str):
        path_to_list = self.file / user_id
        if path_to_list.exists():
            return [str(file) for file in path_to_list.iterdir()]
        else:
            return []
