import os
import logging

from flask import Flask
from flask_limiter import Limiter
from flask_restful_swagger import swagger

from logging.handlers import RotatingFileHandler

from config import DefaultConfig, ExemptionApi, support_jsonp

import api.user as user
import api.account as account

template_folder = 'static'
UPLOAD_FOLDER = '/tmp/upload/'

app = Flask(__name__, template_folder=template_folder)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.from_object(DefaultConfig)

# If you want to create your own enviroment then create a virtual environment with the path fot your settings.cfg
if os.path.isfile(os.getenv('CONFIG_PATH', '/flask/settings.cfg')):
    app.config.from_envvar('CONFIG_PATH')

# Logs
path = '/var/log/flask/'
logger = logging.getLogger('api_flask')
handler = logging.handlers.TimedRotatingFileHandler(
    '%s%s.log' % (path, 'api_flask'), 'midnight', 1, backupCount=2)
handler.suffix = '%Y-%m-%d.log'
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

limiter = Limiter(app)
api = swagger.docs(ExemptionApi(limiter, app), apiVersion='0.1')
support_jsonp(api)

api.add_resource(user.User, '/get_user')
api.add_resource(account.Account, '/get_account')
api.add_resource(account.withdraw, '/withdraw')
api.add_resource(account.pay, '/pay')

if __name__ == '__main__':
    app.run(debug=True, port=5999)