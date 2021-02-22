from milvus import *
from QA.config import MILVUS_HOST, MILVUS_PORT, SEAR_PARM, TOP_K#, collection_param, search_param, top_k


class MilvusConnector:
    def __init__(self, host, port, collection_name):

        self.collection_name = collection_name
        self.client = self.milvus_client(host, port)
        #TODO: create collection

    def milvus_client(self, host=MILVUS_HOST, port=MILVUS_PORT):
        try:
            milvus = Milvus(host=host, port=port)
            return milvus
        except Exception as e:
            print("Milvus client error:", e)

    def create_collection(self):
        try:
            collection_param = {
                'collection_name': self.collection_name,
                'dimension': 768,
                'index_file_size':2048,
                'metric_type':  MetricType.IP
            }
            status = self.client.create_collection(collection_param)
            return status
        except Exception as e:
            print("Milvus create table error:", e)

    def create_index(self):
        param = {'nlist': 16384}
        try:
            status = self.client.create_index(self.collection_name, IndexType.IVF_FLAT, param)
            return status
        except Exception as e:
            print("Milvus create index error:", e)

    def insert(self, vectors):
        "can insert either single or multiple vectors; in any case the vectors must be a list"
        try:
            status, ids = self.client.insert(collection_name=self.collection_name, records=vectors)
            return status, ids
        except Exception as e:
            print("Milvus insert error:", e)

    def delete(self, ids):
        "either delete single or multiple entities by id or ids, in any case the ids must be a list"
        self.client.delete_entity_by_id('demo_films', ids)

    def get_similar_question(self, question_query):
        status, results = self.search(question_query)

        return results

    def search(self, vec):
        try:
            status, results = self.client.search(collection_name=self.collection_name, query_records=vec, top_k=TOP_K, params=SEAR_PARM)
            return status, results
        except Exception as e:
            print("Milvus search error:", e)