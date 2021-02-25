from QA.config import DEFAULT_TABLE
from drafts.mongodb import insert_data
from drafts.milvus_ import has_table, create_table, milvus_insert, create_index
import pickle as pkl
import numpy as np


def has_table(table_name, client):
    try:
        status, ok = client.has_collection(collection_name=table_name)
        print(status)
        return status, ok
    except Exception as e:
        print("Milvus has_table error:", e)


def normalize_vec(vec_list):
    question_vec = []
    for vec in vec_list:
        sqrt_square_sum = np.sqrt(np.sum(vec**2))
        vec = list(vec/sqrt_square_sum)
        question_vec.append(vec)
    return question_vec


def read_data(fname_path):
    data = pkl.load(open(fname_path,"rb"))
    question_data = data["Question"].tolist()[:50]
    answer_data = data["Answer"].tolist()[:50]
    print(len(question_data),len(answer_data))
    return question_data, answer_data


def load_data(fname_path, client, bc, collection):
    try:
        question_data, answer_data = read_data(fname_path)
        print("The data is loaded successfully.")
    except Exception as e:
        print("read data faild: ",e)
        print("Failed to read data, please check the data file format.")
        return False
    try:
        init_table(DEFAULT_TABLE, client)
        question_vecs = bc.encode(question_data)
        question_vecs = normalize_vec(question_vecs)
        status, ids = milvus_insert(DEFAULT_TABLE, client, question_vecs)
        print("The data is inserted into milvus successfully.")

        insert_data(collection, ids, question_data, answer_data)
        print("The data is inserted into mongo db successfully.")

        print(len(ids))
        return True
    except Exception as e:
        print("load data faild: ",e)
        print("Failed to load data.")
        return False


def init_table(table_name, client):
    status, ok = has_table(table_name, client)
    print("has_table:", status, ok)
    if not ok:
        print("create collection.")
        create_table(table_name, client)
        create_index(table_name, client)
