import os
from milvus import MetricType

MILVUS_HOST = os.getenv("MILVUS_HOST", "127.0.0.1")
MILVUS_PORT = os.getenv("MILVUS_PORT", 19530)

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "QA")

COLLECTION_PARM = {
    'collection_name': COLLECTION_NAME,
    'dimension': 768,
    'index_file_size':2048,
    'metric_type':  MetricType.IP
}
INDEX_PARM =  {'nlist': 16384}
SEARCH_PARM = {'nprobe': 32}
TOP_K = 5

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_USERNAME = "root"
MONGO_PASSWORD = "password"
BERT_IP = "localhost"
BERT_PORT = 5555
BERT_PORT_OUT = 5556
MONGO_DATABASE_NAME = "QA"