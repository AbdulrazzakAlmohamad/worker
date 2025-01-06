import threading
from gateway.Rabbitmq import RabbitMQ  
import pika
from middlewares.Logger import Logger


 
# Define the consumer thread
class ConsumerThread(threading.Thread):
    def __init__(self, queue_name , callback):
        super(ConsumerThread, self).__init__()
        self.queue_name = queue_name
        self.callback = callback
        self.logger = Logger()
 
    def run(self):
        # Connect to RabbitMQ
        try: 
            connection = RabbitMQ()._connection
            channel = connection.channel()
    
            # Start consuming messages
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)

            try:
                channel.start_consuming()
            except KeyboardInterrupt as ex:
                channel.stop_consuming()
                self.logger.error(str(ex)) 
            except pika.exceptions.AMQPConnectionError as ex:
                channel.stop_consuming()
                self.logger.error("Connection error:" +str(ex))  
            except pika.exceptions.ChannelClosed as ex:
                channel.stop_consuming()
                self.logger.error("Channel closed:" +str(ex)) 
            except pika.exceptions.ChannelWrongStateError as ex:
                channel.stop_consuming()
                self.logger.error("Channel in wrong state:" +str(ex))  
            except pika.exceptions.DuplicateConsumerTag as ex:
                channel.stop_consuming()
                self.logger.error("Duplicate consumer tag:" +str(ex))  
            except pika.exceptions.IncompatibleProtocolError as ex:
                channel.stop_consuming()
                self.logger.error("Incompatible protocol version:" +str(ex))  
            except Exception as ex:
                channel.stop_consuming()
                self.logger.error("An unexpected error occurred:" +str(ex))  

            connection.close() 

        except pika.exceptions.AMQPConnectionError as ex:
          self.logger.error(str(ex)) 
        except Exception as ex:
          self.logger.error(str(ex))     
