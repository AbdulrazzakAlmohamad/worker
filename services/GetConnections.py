from services.RabbitMqHttpService import RabbitMqHttpService


class GetConnections(RabbitMqHttpService):
    PATH_LINK = "api/connections"

    def execute(self):
        url = self.baseLink + "/" + self.PATH_LINK
        response = self.requests.get(url,
                                     auth=(self.os.getenv("RABBITMQ_USERNAME"), self.os.getenv("RABBITMQ_PASSWORD")))

        return response.json()
