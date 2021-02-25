# Building a Q&A system based on semantic understanding

We are going to implement a question answering system through semantic similarity matching.

You have to collect a huge number of questions with answers(either in a specific field, or a standard question set) for
this task.

## Functionalities that can be done by a user:

### When a user asks a question:

* The BERT model converts the question to a feature vector.
* Milvus performs a similarity search and retrieves the ID most similar to the question (or could retrieve top k most
  similar IDs).
* MongoDB returns the corresponding answer(s).

### When a user wants to insert into the database:

* Pair of question(s) answer(s) will be inputed
* The BERT model converts the questions into feature vectors and store them in Milvus.
* Either use the vector ID that milvus will assign to each feature vector or own unique defined ids.
* Store these representative question IDs and their corresponding answers in MongoDB.

### When a user wants to delete pair(s) of question(s) with answer(s):

* A list of the pair(s) id(s) will be inputed
* Delete the id(s) from milvus then from mongodb


## Step-by-step to build the Q&A system:

*  Download a Pre-trained BERT Model then uncompress the zip file into a folder, like in our case "cased_L-12_H-768_A-12"
*  Change the highlighted place in the docker compose file with the path to your downloaded bert model in order to use [Bert-as-a-service](https://github.com/hanxiao/bert-as-service). 
* Run the docker compose file which will install Milvus, MongoDB and bert-as-service. <br>
  [Milvus](https://www.milvus.io/docs/v0.10.6/overview.md) is an open source vector similarity search engine.<br>
* Run the initialization.py script inorder to initialize the milvus collection and index.


[comment]: <> (eshra7 kif l fast api 3m est5dmo wle)

[comment]: <> (wbeshra7 el classes)