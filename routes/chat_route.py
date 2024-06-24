from pydantic import BaseModel

from fastapi import APIRouter , UploadFile , HTTPException
from fastapi.responses import JSONResponse

from langchain_openai import ChatOpenAI , OpenAIEmbeddings
from langchain_core.vectorstores import VectorStore
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from domain.services.file_service import FileService
from domain.services.vector_service import VectorService
from domain.services.docs_service import DocsService

from adapters.docs_adapter import DocsAdapter
from adapters.file_adapter import FileAdapter
from adapters.chroma_vector_adapter import ChromaVectorAdapter
# from adapters.es_vector_adapter import ElasticsearchVectorAdapter

from settings import OPENAI_API_KEY, CUSTOM_PROMPT

class Question(BaseModel):
    question: str

file_service = FileService(FileAdapter())
vector_service = VectorService(ChromaVectorAdapter(OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)))
docs_service = DocsService(DocsAdapter())

def chain(vectorstore : VectorStore):
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125" , openai_api_key=OPENAI_API_KEY)
    retriever = vectorstore.as_retriever()
    prompt = PromptTemplate.from_template(CUSTOM_PROMPT)
    
    def format_docs(docs):
        formatted_docs = "\n\n".join(doc.page_content for doc in docs)
        return formatted_docs

    chain : ChatOpenAI = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    return chain

router = APIRouter()

@router.get("/ping")
async def pong():
    return {"ping": "pong!"}

@router.post("/{user_id}")
async def ask_question(user_id: str, json_body: Question):
    try:
        vectorstore = vector_service.vectorstore(user_id=user_id)
        response = chain(vectorstore).invoke(json_body.question)
        return JSONResponse(status_code=200, content={"response": response.to_json()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
