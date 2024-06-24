from fastapi import APIRouter , UploadFile , HTTPException
from fastapi.responses import JSONResponse, FileResponse

from langchain_openai import OpenAIEmbeddings

from domain.services.file_service import FileService
from domain.services.vector_service import VectorService
from domain.services.docs_service import DocsService

from adapters.docs_adapter import DocsAdapter
from adapters.file_adapter import FileAdapter
from adapters.chroma_vector_adapter import ChromaVectorAdapter

from settings import OPENAI_API_KEY

embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

file_service = FileService(FileAdapter())
vector_service = VectorService(ChromaVectorAdapter(embedding_model))
docs_service = DocsService(DocsAdapter())

router = APIRouter()

@router.get("/ping")
async def pong():
    return {"ping": "pong!"}

@router.post("/{user_id}/upload")
async def upload(user_id: str , file: UploadFile):
    try:
        if file.content_type not in ["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/markdown", "text/csv"]:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")
        
        saved_path = file_service.save(user_id, file)

        loaded_docs = docs_service.load(path=saved_path,content_type=file.content_type)

        splited_docs = docs_service.split(docs=loaded_docs)
        
        vector_service.embed_and_store_docs(splits=splited_docs , user_id=user_id)
        
        return JSONResponse(status_code=200, content={"message": "Files uploaded and indexed successfully"})
    
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{user_id}/download/{filename}")
async def download(user_id: str, filename: str):
    try:
        file_path = file_service.get(user_id, filename)
        return FileResponse(file_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
async def list_files(user_id: str):
    try:
        files = file_service.list(user_id)
        return JSONResponse(status_code=200, content={"files": files})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{user_id}/delete/{filename}")
async def delete(user_id: str, filename: str):
    try:
        file_service.delete(user_id, filename)
        vector_service.delete_stored_docs(user_id=user_id, doc_ids=[f"{user_id}_{filename}"])
        return JSONResponse(status_code=200, content={"message": "File deleted successfully"})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    