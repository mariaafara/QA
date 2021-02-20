import os
from milvus import MetricType

MILVUS_HOST = os.getenv("MILVUS_HOST", "127.0.0.1")
MILVUS_PORT = os.getenv("MILVUS_PORT", 19530)

DEFAULT_TABLE = os.getenv("DEFAULT_TABLE", "qa_system")

COLLECTION_PARM = {
    'collection_name': DEFAULT_TABLE,
    'dimension': 768,
    'index_file_size':2048,
    'metric_type':  MetricType.IP
}

SEAR_PARM = {'nprobe': 32}
TOP_K = 5
