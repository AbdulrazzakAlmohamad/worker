import os
import logging
import requests

import json

from abc import abstractmethod


class RabbitMqHttpService:
    username = ''
    password = ''
    baseLink = ''
    requests = requests
    os = os
    json = json

    def __init__(self):
        self.username = os.geteResponseErrornv("RABBITMQ_USERNAME")
        self.password = os.getenv("RABBITMQ_PASSWORD")
        self.baseLink = os.getenv("HTTP_HTTPS") + os.getenv("RABBITMQ_HOST") + ":" + os.getenv("RABBITMQ_PORT_UI")

    def process(self):
        try:
            return self.execute()
        except Exception as e:
            return str(e)

    @abstractmethod
    def execute(self):
        pass
