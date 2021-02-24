from config import MILVUS_HOST, MILVUS_PORT, COLLECTION_NAME, COLLECTION_PARM,INDEX_PARM
from milvus import *
import logging
import pickle as pkl


def create_collection(self):
    try:
        logging.info("Creating %s collection in milvus".format(COLLECTION_NAME))
        status = self.client.create_collection(COLLECTION_PARM)
        return status
    except Exception as e:
        print("Milvus create collection error:", e)


def has_collection(client):
    try:
        logging.info("Checking the existence of %s collection in milvus".format(COLLECTION_NAME))
        status, ok = client.has_collection(collection_name=COLLECTION_NAME)
        return status, ok
    except Exception as e:
        print("Milvus has_table error:", e)


def create_index(client):
    try:
        logging.info("Creating an index in %s collection in milvus".format(COLLECTION_NAME))
        status = client.create_index(COLLECTION_NAME, IndexType.IVF_FLAT, INDEX_PARM)
        return status
    except Exception as e:
        print("Milvus create index error:", e)


def create_milvus_collection(client):
    client.create_collection()
    client.milvus.create_index()

def read_data(self, fname_path):
    data = pkl.load(open(fname_path,"rb"))
    question_data = data["Question"].tolist()[:50]
    answer_data = data["Answer"].tolist()[:50]
    print(len(question_data),len(answer_data))
    return question_data, answer_data


if __name__ == '__main__':

    print(MILVUS_HOST, MILVUS_PORT)

    milvus_client = Milvus(host=MILVUS_HOST, port=MILVUS_PORT)

    status, ok = has_collection(milvus_client)
    print("^^",status,ok)
    if not ok:
        status = create_collection(milvus_client)
        print(status)
        create_index(milvus_client)
        print(status)

    # question_data, answer_data = read_data(".data.pkl")

