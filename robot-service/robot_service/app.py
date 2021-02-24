import logging

from flask import Flask

from robot_service.infra.db import init_db
from robot_service.infra.kafka import init_message_listening

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Starting')

app = Flask(__name__)

app.config['UPLOADED_ROBOTS_DEST'] = '/var/files/'
app.config['UPLOADED_ROBOTS_ALLOW'] = 'jar'

init_db(app)


with app.app_context():
    from robot_service.infra.upload import init_upload
    from robot_service.infra.web import init_web
    init_upload(app)
    init_web(app)
    init_message_listening(app)
