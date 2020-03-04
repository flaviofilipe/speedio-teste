from flask import jsonify, request
from app import app, mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from app.RabbitMQ import Operations


@app.route("/comment", methods=['POST'])
def newMessages():
    # collection_transactions = mongo.db.transactions
    data = request.data
    queue = Operations.write_messages(data.decode('utf8'))
    return queue


@app.route("/comment", methods=['GET'])
def getMessages():
    messages = Operations.read_messages()
    return saveInMongoDB(messages)


def saveInMongoDB(data):
    collection_transactions = mongo.db.transactions
    new_transaction = collection_transactions.insert(data)
    query = {"_id": ObjectId(new_transaction)}
    get_transaction = dumps(collection_transactions.find(query))

    return get_transaction
