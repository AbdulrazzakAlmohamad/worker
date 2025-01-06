import os
import pika
import json 

class RabbitMQ:

    def __init__(self):
        self._channel = None
        self._connection = None
        self._host = os.getenv("RABBITMQ_HOST")
        self._username = os.getenv("RABBITMQ_USERNAME")
        self._password = os.getenv("RABBITMQ_PASSWORD")
        self._port = os.getenv("RABBITMQ_PORT")
        self._vhost = os.getenv("RABBITMQ_VHOST") 
        self.init_channel()

    def init_channel(self):
        credentials = pika.PlainCredentials(self._username, self._password)
        parameters = pika.ConnectionParameters(self._host, self._port, self._vhost, credentials=credentials)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()

    def create_queue(self, queue_name):
        self._channel.queue_declare(queue=queue_name, durable=True)
        return True

    def delete_queue(self, queue_name):
        self._channel.queue_delete(queue=queue_name)
        return True

    def get_queue_info(self, queue_name):
        queue = self._channel.queue_declare(queue=queue_name, durable=True, exclusive=False, auto_delete=False)
        return queue.method.message_count

    # def create_consumer(self, queue_name, callback):
    #     self._channel.queue_bind(exchange='amq.direct', queue=queue_name)
    #     self._channel.basic_qos(prefetch_count=1)
    #     self._channel.basic_consume(queue=queue_name, on_message_callback=callback)
    #     try:
    #         self._channel.start_consuming()
    #     except KeyboardInterrupt as ex:
    #         self._channel.stop_consuming()
    #         return str(ex)

    #     self._connection.close()

    # this for pushing message 
    def publish(self,data):
        for i in range (1,101): 
            if i == 50 :
                body = json.dumps({'clientId': data['clientId'], 'shipmentPackageId': 1})
            else:
                body = json.dumps({'clientId': data['clientId'], 'shipmentPackageId': i})

            self._channel.exchange_declare(data['queueName'], 'direct', False, False, False)
            self._channel.basic_publish(
                exchange='',
                routing_key=data['queueName'],
                body=body,
                properties=pika.BasicProperties(content_type='application/json')
            )
            print(body)
            
        self._connection.close()
        return True
