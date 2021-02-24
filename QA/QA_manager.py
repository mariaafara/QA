from bert_serving.client import BertClient
from connectors import MongoConnector, MilvusConnector
import pickle as pkl
import numpy as np
import logging


class QAManager:
    def __init__(self,
                 mongo_host, mongo_port, mongo_username, mongo_password,
                 milvus_host, milvus_port, bert_ip, bert_port, bert_port_out,
                 database_name, collection_name):
        print(bert_ip, bert_port, bert_port_out)
        self.bc = BertClient(ip=bert_ip,
                             port=bert_port,
                             port_out=bert_port_out,
                             check_length=False)

        self.mongo = MongoConnector(host=mongo_host,
                                     port=mongo_port,
                                     username=mongo_username,
                                     password=mongo_password,
                                    database_name=database_name,
                                    collection_name=collection_name)

        self.milvus = MilvusConnector(milvus_host,
                                       milvus_port,
                                      collection_name)


    def normalize_vec(self, vec_list):
        """Method that normalizes question(s) vector(s).

        :param vec_list:
        :return:
        """
        question_vec = []
        for vec in vec_list:
            sqrt_square_sum = np.sqrt(np.sum(vec**2))
            vec = list(vec/sqrt_square_sum)
            question_vec.append(vec)
        return question_vec

    def insert(self, insert_query):
        """Method that inserts pair(s) of question(s) answer(s) into Milvus and MongoDb.

        :param insert_query: List of dictionaries in the format: [{"question": "answer"}]
        :return:
        """

        question_data = [ele.question for ele in insert_query]
        answer_data = [ele.answer for ele in insert_query]
        question_vecs = self.bc.encode(question_data)
        print("The question data  is encoded by Bert successfully.")
        question_vecs = self.normalize_vec(question_vecs)
        print("The question vectors are normalized successfully.")
        status, ids = self.milvus.insert(question_vecs)
        print("The data is inserted into milvus successfully.")
        self.mongo.insert(ids, question_data, answer_data )
        print("The data is inserted into MongoDB successfully.")

    def delete(self, ids):
        """Method that deletes question(s) answer(s) pair(s) based on their id(s) in the database.

        :param ids: List of ids.
        :return:
        """
        self.milvus.delete(ids)
        print("The data is deleted successful from milvus.")
        self.mongo.delete(ids)
        print("The data is deleted successful from MongoDB.")

    def get_answer(self, question, top_k, search_parm):
        """Method that search for an answer in a DataBase.

        :param question: The question of which needs to be answered.
        :param top_k: Number of top answers returned.
        :param search_parm:
        :return: top_k answers found in database.
        """
        query_data = [question]
        vectors = self.bc.encode(query_data)
        query_list = self.normalize_vec(vectors)
        logging.info("start search in milvus...")
        results = self.milvus.get_similar_question(query_list, top_k, search_parm)
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

    def drop_milvus_collection(self):
        self.milvus.drop_milvus_collection()