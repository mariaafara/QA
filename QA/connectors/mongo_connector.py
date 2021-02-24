from pymongo import MongoClient


class MongoConnector:
    """A class that manages all the operations related to Mongo db"""

    def __init__(self, host, port, username, password, database_name, collection_name):
        self.client = self.mongodb_client(host, port, username, password)
        self.collection_name = collection_name
        self.database = self.client[database_name]
        self.collection = self.database[self.collection_name]

    def mongodb_client(self, host, port, username, password):
        try:
            mongo_client = MongoClient(host=host, port=port, username=username, password=password)
            return mongo_client
        except Exception as e:
            print("Mongo db client error:", e)

    def insert(self, ids, questions, answers):
        data = []
        for i in range(len(ids)):
            record = {"_id": str(ids[i]),
                      "question": questions[i],
                      "answer": answers[i]}
            data.append(record)
        self.collection.insert_many(data)
        print("Data inserted successfully into MongoDB.")

    # def delete_one(self, id):
    #     self.collection.deleteOne({"_id": id})

    def delete(self, ids):
        res = self.collection.delete_many({"_id": {"$in": [str(i) for i in ids]}})
        print("{} were deleted".format(res.deleted_count))

    def search(self, ids):
        output = list(self.collection.find({"_id": {"$in": [str(i) for i in ids]}}))
        print(output)
        return output
