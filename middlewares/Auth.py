from werkzeug.wrappers import Request, Response
from middlewares.IpAddresses import IpAddresses
from middlewares.Logger import Logger
import os

class Auth:

    def __init__(self, app):
        self.app = app
        self.userName = os.getenv('AUTH_USERNAME')
        self.password = os.getenv('AUTH_PASSWORD')
        self.logger = Logger()

    def __call__(self, environ, start_response):
        request = Request(environ)
        if request.authorization is None:
            res = Response('Authorization is required', mimetype='text/plain', status=401)
            return res(environ, start_response)

        ipRemote = request.remote_addr

        if request.authorization['username'] == self.userName \
                and request.authorization['password'] == self.password :
            environ['user'] = {'name': 'Gpay'}
            return self.app(environ, start_response)

        res = Response('Authorization failed from Ip : '+ipRemote, mimetype='text/plain', status=401)
        return res(environ, start_response)
