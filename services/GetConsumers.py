from services.RabbitMqHttpService import RabbitMqHttpService


class GetConsumers(RabbitMqHttpService):
    PATH_LINK = "api/consumers"

    def __init__(self, queue_name=None):
        super().__init__()
        self.queueName = queue_name

    def execute(self):
        url = self.baseLink + "/" + self.PATH_LINK
        response = self.requests.get(url,
                                     auth=(self.os.getenv("RABBITMQ_USERNAME"), self.os.getenv("RABBITMQ_PASSWORD")))
        responseText = self.json.loads(response.text)
        data = []
        if self.queueName is not None and response is not None:
            for item in responseText:
                if item['queue']['name'] == self.queueName:
                    data.append(item)
            return data
        else:
            return response.json()
