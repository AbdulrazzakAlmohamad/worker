import threading
from flask import json 
from gateway.Rabbitmq import RabbitMQ
from gateway.ConsumerThread import ConsumerThread
from middlewares.Logger import Logger
import requests
from services.ResponseMessages import ResponseMessages
import os


class WorkerRMQ:
    def __init__(self, queue_name):
        self.client_id = None
        self.queue_name = queue_name
        self.logger = Logger()

    def create(self):  
        consumer_thread = ConsumerThread(self.queue_name , self.on_message)
        consumer_thread.start()
        return ResponseMessages.CONSUMER_HAS_CREATED

    def set_queue_name(self, queue_name):
        self.queue_name = queue_name
        return self

    def get_queue_name(self):
        return self.queue_name

    def set_client_id(self, client_id):
        self.client_id = client_id
        return self

    def get_client_id(self):
        return self.client_id

    def on_message(self, chan, method_frame, _header_frame, body, userdata=None):
        self.logger.info(
            '1- Start sending Message : %s, Userdata: %s, Message body: %s' % (self.queue_name, userdata, body))
        try:
            data = json.loads(body)
            if data is None or get_array_element(data,'clientId')   is None or get_array_element(data,'shipmentPackageId') is None :
                self.logger.error('2- Sending Message - Invalid Message' + str(data))
                result = False
            else: 
                result = self.process(data)  
        except ValueError as e:
            self.logger.info('2- Start sending Message Error : %s , %s, Userdata: %s, Message body: %s' % (
            e, self.queue_name, userdata, body))
            result = False

        chan.basic_ack(delivery_tag=method_frame.delivery_tag)
        # if result:
        #     chan.basic_ack(delivery_tag=method_frame.delivery_tag)
        # else:
        #     chan.basic_reject(delivery_tag=method_frame.delivery_tag, requeue=False)

    @staticmethod
    def get_payload(shipment_package_id, client_id):
        return {
            'shipment_package_id': shipment_package_id,
            'secret_key': os.getenv('SECRET_KEY'),
            'client_id': client_id,
            'consumerId': threading.get_ident()
        }

    def process(self, data) -> bool: 
        # if data is None or get_array_element(data,'clientId')   is None or get_array_element(data,'shipmentPackageId') is None :
        #     self.logger.error('2- Sending Message - Invalid Message' + str(data))
        #     return False

        shipment_package_id = data['shipmentPackageId']
        try:
            payload = self.get_payload(shipment_package_id, data['clientId'])
            response = requests.post(os.getenv("EPINTOWER_API_PROCESS_ORDER"), data=payload)
            self.logger.info(
                '2- Response after Sending Message - ShipmentPackageId: %s, Response Code : %s' % (
                shipment_package_id, response))

            if response.status_code != requests.codes.ok:
                self.logger.error('3- Failed Request - ShipmentPackageId: %s, Failed Request with '
                                  'Response Code : %s'
                                  % (shipment_package_id,
                                     response.status_code))
                return False

            data = response.json()
            self.logger.info(
                '3- Received Response - ShipmentPackageId: %s, errorCode: %s Message body: %s' % (shipment_package_id,
                                                                                                  data.get('error'),
                                                                                                  data.get('message')))
            return True

        except ValueError as ex:
            self.logger.error('4- Failed Request with ValueError - Invalid Json:  %s' % ex)
            return False
        except requests.exceptions.RequestException as ex:
            self.logger.error('4- Failed Request with RequestException - ShipmentPackageId: %s - %s' % (
            shipment_package_id, repr(ex)))
            return False


def get_array_element(arr, index):
    try:
        return arr[index]
    except Exception:
        return None 