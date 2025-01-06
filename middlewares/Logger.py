import os
from pymongo import MongoClient
from datetime import datetime


class Logger:

    def __init__(self): 
        self._client = MongoClient(os.getenv("MONGODB_HOST") +":"+ os.getenv("MONGODB_PORT"))
        self._db = self._client["rmq"]
        self._log_collection = self._db["consumerApi"]
        self._pid = os.getpid()

    def prepare_data(self, log_type, msg):
        return {"type": log_type, "pId": self._pid, "msg": msg, "dateTime": datetime.now()}

    def insert(self, data):
        self._log_collection.insert_one(data)

    def info(self, msg):
        data = self.prepare_data("Info", msg)
        self.insert(data)

    def error(self, msg):
        data = self.prepare_data("Error", msg)
        self.insert(data)

    def warning(self, msg):
        data = self.prepare_data("Warning", msg)
        self.insert(data)
