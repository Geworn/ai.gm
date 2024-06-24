from fastapi import FastAPI
import uvicorn

from routes.file_route import router as file_router
from routes.chat_route import router as chat_router

api = FastAPI()

api.include_router(router=file_router , prefix="/files")
api.include_router(router=chat_router , prefix="/chat")

if __name__ == "__main__":
    uvicorn.run("main:api", host="0.0.0.0", port=7000, log_level="info", reload=True)
