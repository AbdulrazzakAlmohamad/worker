import os

os.environ['RABBITMQ_USERNAME'] = 'gpay'
os.environ['RABBITMQ_PASSWORD'] = 'SgKqEsafY4M4HehNf'
os.environ['RABBITMQ_HOST'] = '10.0.1.50'
os.environ['RABBITMQ_PORT'] = '5672'
os.environ['RABBITMQ_PORT_UI'] = '15672'
os.environ['RABBITMQ_VHOST'] = '/'
os.environ['HTTP_HTTPS'] = 'http://' 
os.environ['EPINTOWER_API_PROCESS_ORDER'] = "https://www.epintower.com/bot/processOrder"
os.environ['SECRET_KEY'] = 'assa__d890asdsj##4^sad'

# mongodb settings
os.environ['MONGODB_HOST'] = 'mongodb://10.0.1.60'
os.environ['MONGODB_PORT'] = '27017'

# Auth settings
os.environ['AUTH_USERNAME'] = 'Gpay'
os.environ['AUTH_PASSWORD'] = 'GPAYappPython'
