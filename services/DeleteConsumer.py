from services.RabbitMqHttpService import RabbitMqHttpService
from services.Helper import Helper
import urllib.parse


class DeleteConsumer(RabbitMqHttpService):
    PATH_LINK = "api/connections"

    def execute(self):
        data = Helper.get_data()
        consumerName = data['consumerName']
        url = self.baseLink + "/" + self.PATH_LINK + "/" + urllib.parse.quote(consumerName)
        response = self.requests.delete(url,
                                        auth=(self.os.getenv("RABBITMQ_USERNAME"), self.os.getenv("RABBITMQ_PASSWORD")))
        return response.json()
