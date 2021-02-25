from QA.config import MILVUS_HOST, MILVUS_PORT, SEAR_PARM, TOP_K#, collection_param, search_param, top_k
from QA import QAManager
import logging
if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    qa_manager = QAManager(mongo_host="local",
                           mongo_port=27017,
                           mongo_username="root",
                           mongo_password="password",
                           milvus_host=MILVUS_HOST,
                           milvus_port=MILVUS_PORT,
                           bert_ip="localhost",
                           bert_port=5555,
                           bert_port_out=5556)