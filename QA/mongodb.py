from pymongo import MongoClient


def mongodb_client():
    try:
        mongo_client = MongoClient(host="localhost", port=27017, username="root", password="password")
        return mongo_client
    except Exception as e:
        print("Mongo db client error:", e)


# def create_database(client):
#     return client["QA"]


def get_collection(database, coll_name):
    return database[coll_name]


def insert_data(collection, ids, questions, answers):
    data = []
    for i in range(len(ids)):
        record = {"_id": ids[i],
                  "question": questions[i],
                  "answer": answers[i]}
        data.append(record)
    collection.insert_many(data)
    print("Data inserted successfully into MongoDB.")


def search_collection(ids, collection):
    return list(collection.find({"_id": {"$in": ids}}))