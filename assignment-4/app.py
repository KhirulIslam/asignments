from flask import Flask , json
import os
from flask import request
import json
import decimal
from elasticsearch import Elasticsearch
app = Flask("sample-app")


def save(doc_body):
    try:
        client = Elasticsearch(hosts=[os.getenv('ELASTICSEARCH_HOST_IP')])
        response = client.index(
        index = os.getenv('INDEX_NAME'),
        doc_type = '_doc',
        body = doc_body,
        request_timeout=45)

        print("indexed successfully:", response)

    except Exception as err:
        print("Elasticsearch index() ERROR:", err)

def delete(id):
    es = Elasticsearch(hosts=[os.getenv('ELASTICSEARCH_HOST_IP')])
    es.indices.delete(index=os.getenv('INDEX_NAME'), ignore=[400, 404])

def update(doc_body):
    try:
        client = Elasticsearch(hosts=[os.getenv('ELASTICSEARCH_HOST_IP')])
        response = client.index(
        index = os.getenv('INDEX_NAME'),
        doc_type = '_doc',
        body = doc_body,
        request_timeout=45)

        print("indexed updated successfully:", response)

    except Exception as err:
        print("Elasticsearch index() ERROR:", err)
 
def get():
    es = Elasticsearch(hosts=[os.getenv('ELASTICSEARCH_HOST_IP')])
    res = es.search(index=os.getenv('INDEX_NAME'), size=5)

    return res


@app.route('/save', methods=["POST"])
def save_product():
    try:
        if request.json:
            save(request.get_json())
		
        # return json.dumps("success"), 200, 
        return "success"
    except Exception as e:
        return e  ,200,
		

@app.route('/update', methods=["PUT"])
def update_product():
    if request.json:
        update(request.get_json())
        return json.dumps("success"), 200, 
    else:
        return "INVALID HTTP METHOD"

@app.route('/delete/<id>', methods=["DELETE"])
def delete_product(id):
    try:
        if request.method == 'GET':
            delete(id)
            return json.dumps("success"), 200, 
        else:
            return "INVALID HTTP METHOD"
		
    except Exception as e:
        return e

@app.route('/get', methods=["GET"])
def get_product():
    response=get()
    return response, 200

@app.route("/")
def hello():
    return "Hello, World!"