from bert_serving.client import BertClient
from QA.connectors import mongo_connector, milvus_connector
import pickle as pkl
import numpy as np
import logging

class QAManager:
    def __init__(self, mongo_host, mongo_port, mongo_username, mongo_password,
                 milvus_host, milvus_port, bert_ip, bert_port, bert_port_out):

        self.bc = BertClient(ip=bert_ip,
                             port=bert_port,
                             port_out=bert_port_out,
                             check_length=False)

        self.mongo = mongo_connector(host=mongo_host,
                                     port=mongo_port,
                                     username=mongo_username,
                                     password=mongo_password)

        self.milvus = milvus_connector(milvus_host,
                                       milvus_port)

    def read_data(self, fname_path):
        data = pkl.load(open(fname_path,"rb"))
        question_data = data["Question"].tolist()[:50]
        answer_data = data["Answer"].tolist()[:50]
        print(len(question_data),len(answer_data))
        return question_data, answer_data

    def normalize_vec(self, vec_list):
        question_vec = []
        for vec in vec_list:
            sqrt_square_sum = np.sqrt(np.sum(vec**2))
            vec = list(vec/sqrt_square_sum)
            question_vec.append(vec)
        return question_vec

    def insert(self, question_data, answer_data):
        question_vecs = self.bc.encode(question_data)
        print("The question data  is encoded by Bert successfully.")
        question_vecs = self.normalize_vec(question_vecs)
        print("The question vectors are normalized successfully.")
        status, ids = self.milvus.insert(question_vecs)
        print("The data is inserted into milvus successfully.")
        self.mongo.insert(ids, question_data, answer_data )
        print("The data is inserted into MongoDB successfully.")

    def delete(self, ids):
        self.milvus.delete(ids)
        print("The data is deleted successful from milvus.")
        self.mongo.delete(ids)
        print("The data is deleted successful from MongoDB.")

    def get_answer(self, question):
        query_data = [question]
        vectors = self.bc.encode(query_data)
        query_list = self.normalize_vec(vectors)
        logging.info("start search in milvus...")
        results = self.milvus.get_similar_question(query_list)
        if not results:
            return "No data in the database."

        if results[0][0].distance < 0.8:
            return "No similar questions in the database."

        logging.info("start search in mongodb ...")
        ids = []
        for result in results[0]:
            ids.append(result.id)
        rows = self.mongo.search(ids)

        output = []
        if len(rows):
            output = [row["answer"] for row in rows]

        if output:
            return {'status': True, 'msg': output}
        else:
            return {'status': False, 'msg': 'No similar questions in the database'}