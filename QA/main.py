from QA_manager import QAManager
from fastapi import FastAPI
from typing import Optional, List
from pydantic import BaseModel
from config import MILVUS_HOST, MILVUS_PORT, COLLECTION_NAME, MONGO_HOST, MONGO_PORT, MONGO_USERNAME, MONGO_PASSWORD, \
    BERT_IP, BERT_PORT, BERT_PORT_OUT, MONGO_DATABASE_NAME
import logging

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S')


class get_answer_query_model(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "question": "What is your name?",
                "top_k": 3,
                "nprobe": 32
            }
        }

    question: str
    top_k: Optional[int] = 5
    nprobe: Optional[int] = 32


class insert_query_model(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "question": "What is your name?",
                "answer": "My name is X."
            }
        }

    question: str
    answer: str


class delete_query_model(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "ids": [0]
            }
        }

    ids: List[int]


app = FastAPI()
print(BERT_IP)
manager = QAManager(
    mongo_host=MONGO_HOST,
    mongo_port=MONGO_PORT,
    mongo_username=MONGO_USERNAME,
    mongo_password=MONGO_PASSWORD,
    milvus_host=MILVUS_HOST,
    milvus_port=MILVUS_PORT,
    bert_ip=BERT_IP,
    bert_port=BERT_PORT,
    bert_port_out=BERT_PORT_OUT,
    database_name=MONGO_DATABASE_NAME,
    collection_name=COLLECTION_NAME
)


# mongo_host="localhost",
# mongo_port=27017,
# mongo_username="root",
# mongo_password="password",
# milvus_host="127.0.0.1",
# milvus_port=19530,
# bert_ip="localhost",
# bert_port=5555,
# bert_port_out=5556,
# database_name="QA",
# collection_name="QA"


@app.get("/")
async def root():
    return {"message": "Welcome to my FastAPI app :)"}


@app.post("/get_answer")
async def search(question_query: get_answer_query_model):
    return manager.get_answer(
        question_query.question,
        question_query.top_k,
        {"nprobe": question_query.nprobe}
    )


@app.post("/insert")
async def insert(insert_query: List[insert_query_model]):
    return manager.insert(
        insert_query
    )


@app.post("/delete")
async def delete(delete_query: delete_query_model):
    manager.delete(
        delete_query.ids
    )
    return
