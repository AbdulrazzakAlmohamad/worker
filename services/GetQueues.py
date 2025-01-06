from services.RabbitMqHttpService import RabbitMqHttpService


class GetQueues(RabbitMqHttpService):
    PATH_LINK = "api/queues"

    def execute(self):
        url = self.baseLink + "/" + self.PATH_LINK
        response = self.requests.get(url,
                                     auth=(self.os.getenv("RABBITMQ_USERNAME"), self.os.getenv("RABBITMQ_PASSWORD")))
        return response.json()
