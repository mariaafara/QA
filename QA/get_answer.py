import logging
from QA.milvus_ import milvus_search
from QA.config import DEFAULT_TABLE
from QA.mongodb import search_collection
from QA.insert_questions import normalize_vec


def get_similar_question(question, collection, milvus_client, bc):
    logging.info("start process ...")
    query_data = [question]
    try:
        vectors = bc.encode(query_data)
        logging.info("get query vector!")
    except Exception as e:
        info = "bert Error: " + e
        logging.info(info)
        return info
    query_list = normalize_vec(vectors)
    try:
        logging.info("start search in milvus...")
        # search_params = {'nprobe': 64}
        status, results = milvus_search(milvus_client, query_list, DEFAULT_TABLE)
        print(status, results)
        if not results:
            return "No data in the database."

        print("distance:", results[0][0].distance)
        if results[0][0].distance < 0.8:
            return "No similar questions in the database."
    except Exception as e:
        info = "Milvus search error: " + e
        logging.info(info)
        return info
    try:
        logging.info("start search in mongodb ...")
        ids = []
        for result in results[0]:
            ids.append(result.id)
        rows = search_collection(ids, collection)
        print("rows:")
        print(rows)
        outputs = []
        if len(rows):
            outputs = [row["answer"] for row in rows]
        print("len")
        print(len(outputs))
        return outputs
    except Exception as e:
        info = "search in mongodb error: " + e
        logging.info(info)
        return info
