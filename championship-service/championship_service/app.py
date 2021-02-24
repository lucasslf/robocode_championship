import logging

from flask import Flask

from championship_service.infra.kafka import init_championship_event_listening

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Starting')

app = Flask(__name__)

with app.app_context():
    from championship_service.infra.web import init_web
    init_web(app)
    init_championship_event_listening(app)
