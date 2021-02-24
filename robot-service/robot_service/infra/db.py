import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, VARBINARY

db = SQLAlchemy()


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://robot-service:robotsarecool@robot-service-db:3306/robot-service'
    db.init_app(app)


class UUID(TypeDecorator):
    """ A memory-efficient MySQL UUID-type. """

    impl = VARBINARY(16)

    def result_processor(self, dialect, coltype):
        return lambda value: self.process_result_value(value, dialect)

    def bind_processor(self, dialect):
        """ Simple override to avoid pre-processing before
        process_bind_param. This is for when the Python type can't
        be easily coerced into the `impl` type."""
        return lambda value: self.process_bind_param(value, dialect)

    def process_bind_param(self, value, dialect):
        """ Emit the param in hex notation. """
        if isinstance(value, str) and value:
            value = uuid.UUID(value)
        return value.bytes if value else value

    def process_result_value(self, value, dialect):
        if value:
            assert len(value) == 16, "Expected 16 bytes, got %d" % len(value)
            return uuid.UUID(bytes=value)
        else:
            return None
