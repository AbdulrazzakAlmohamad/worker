import os

os.environ['RABBITMQ_USERNAME'] = 'admin'
os.environ['RABBITMQ_PASSWORD'] = '123'
os.environ['RABBITMQ_HOST'] = '127.0.0.1'
os.environ['RABBITMQ_PORT'] = '5672'
os.environ['RABBITMQ_PORT_UI'] = '15672'
os.environ['RABBITMQ_VHOST'] = '/'
os.environ['HTTP_HTTPS'] = 'http://' 
os.environ['EPINTOWER_API_PROCESS_ORDER'] = "http://127.0.0.1:8000/bot/testProcessOrder"
os.environ['SECRET_KEY'] = 'assa__d890asdsj##4^sad'

# mongodb settings
os.environ['MONGODB_HOST'] = 'mongodb://127.0.0.1'
os.environ['MONGODB_PORT'] = '27017'

# Auth settings
os.environ['AUTH_USERNAME'] = 'gpay123'
os.environ['AUTH_PASSWORD'] = 'gpayapppython'