from bert_serving.client import BertClient
from drafts.milvus_ import milvus_client, drop_milvus_table
from drafts.insert_questions import load_data
from drafts.mongodb import mongodb_client, create_database, get_collection
from drafts.get_answer import get_similar_question
from QA.config import DEFAULT_TABLE


def get_answer(question, collection, client, bc):
    # client = milvus_client()
    # bc = BertClient(check_length=False)

    output = get_similar_question(question, collection, client, bc)
    if output:
        return {'status': True, 'msg': output}
    else:
        return {'status': False, 'msg': 'No similar questions in the database'}


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    milvus_client = milvus_client()
    bc = BertClient(ip='localhost', port=5555, port_out=5556, check_length=False)
    mongodb_client = mongodb_client()
    drop_milvus_table(DEFAULT_TABLE, milvus_client)
    database = create_database(mongodb_client)
    answers_collection = get_collection(database, "answers")
    load_data("../data.pkl", milvus_client, bc, answers_collection)

    while True:
        print("please enter a question:")
        question = input()
        answer = get_answer(question,answers_collection, milvus_client, bc)
        print("answer: ",answer)
