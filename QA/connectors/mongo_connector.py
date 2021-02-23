from pymongo import MongoClient


class MongoConnector:
    def __init__(self, host, port, username, password, collection_name):
        self.client = self.mongodb_client(host, port, username, password)
        self.collection_name = collection_name
        self.database = self.client["QA"]
        self.collection = self.database[self.collection_name]

    def mongodb_client(self, host, port, username, password):
        try:
            mongo_client = MongoClient(host=host, port=port, username=username, password=password)
            return mongo_client
        except Exception as e:
            print("Mongo db client error:", e)

    # def insert_one(self, collection, id, question, answer):
    #     record = {"_id": id,
    #               "question": question,
    #               "answer": answer}
    #     collection.insertOne(record)

    def insert(self, ids, questions, answers):
        data = []
        for i in range(len(ids)):
            record = {"_id": ids[i],
                      "question": questions[i],
                      "answer": answers[i]}
            data.append(record)
        self.collection.insert_many(data)
        print("Data inserted successfully into MongoDB.")

    # def delete_one(self, id):
    #     self.collection.deleteOne({"_id": id})

    def delete(self, ids):
        ids = [str(i) for i in ids]
        self.collection.remove({"_id": {"#in": ids}})

    def search(self, ids):
        output = list(self.collection.find({"_id": {"$in": ids}}))
        print(output)
        return output
