# files
from werkzeug.exceptions import HTTPException

from worker.WorkerRMQ import WorkerRMQ
from gateway.Rabbitmq import RabbitMQ
from middlewares.Logger import Logger
from services.DeleteConsumer import DeleteConsumer
from services.GetConnections import GetConnections
from services.GetConsumers import GetConsumers
from services.Helper import Helper
from services.GetQueues import GetQueues
from services.ResponseError import ResponseError
from services.ResponseMessages import ResponseMessages
from middlewares.Auth import Auth
from flask import json
import threading
import os
import env 


# modules
import logging

from flask import Flask, jsonify
from flask import request

app = Flask(__name__)
app.config["DEBUG"] = False
app.wsgi_app = Auth(app.wsgi_app)
logger = Logger()  


if app.config["DEBUG"] : 
  import dev 
else: 
  import env 
  

@app.errorhandler(HTTPException)
def server_error(err):
    data = repr(err)
    logger.error(data)
    return data, 500


@app.errorhandler(HTTPException)
def server_error(e):
    logger.error(repr(e))
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.route('/getQueues', methods=['GET'])
def get_queue():
    queues = GetQueues()
    return jsonify(queues.process())


@app.route('/getConnections', methods=['GET'])
def get_connections():
    connections = GetConnections()
    return jsonify(connections.process())


@app.route('/getConsumers/', methods=['GET'])
@app.route('/getConsumers/<string:queue_name>', methods=['GET'])
def get_consumers(queue_name=None):
    consumers = GetConsumers(queue_name)
    return jsonify(consumers.process())


@app.route('/deleteConsumer', methods=['POST'])
def delete_consumer():
    deleteConsumer = DeleteConsumer()
    return jsonify(deleteConsumer.process())


@app.route('/createQueue', methods=['POST'])
def create_queue():
    data = Helper.get_data()
    result = RabbitMQ().create_queue(data['queueName'])
    if result:
        return ResponseMessages.QUEUE_HAS_CREATED
    else:
        return ResponseError.SERVER_HAS_ERROR


@app.route('/getQueueInfo', methods=['POST'])
def get_queue_info():
    data = Helper.get_data()
    return jsonify(RabbitMQ().get_queue_info(data['queueName']))


@app.route('/deleteQueue', methods=['POST'])
def delete_queue():
    data = Helper.get_data()
    result = RabbitMQ().delete_queue(data['queueName'])
    if result:
        return ResponseMessages.QUEUE_HAS_DELETED
    else:
        return ResponseError.SERVER_HAS_ERROR


@app.route('/createConsumer', methods=['POST'])
def create_consumer():
    data = Helper.get_data()
    worker = WorkerRMQ(data['queueName'])
    return worker.create() 

    
# this route for testing publish a message
@app.route('/messagePublish', methods=['POST'])
def publish_message():
    data = Helper.get_data()
    result = RabbitMQ().publish(data)
    if result:
        return ResponseMessages.MESSAGE_HAS_PUBLISHED
    else:
        return ResponseError.SERVER_HAS_ERROR

    # def shutdown_server():


#     func = request.environ.get('werkzeug.server.shutdown')
#     if func is None:
#         raise RuntimeError('Not running with the Werkzeug Server')
#     func()


# you can shutdown server by this route
# @app.route('/shutdownserver', methods=['POST'])
# def shutdown():
#     shutdown_server()
#     return 'Server shutting down...'        

@app.errorhandler(404)
def not_found(code):
    return jsonify("not found 404")


@app.errorhandler(500)
def not_found(code):
    return jsonify("server error 500")