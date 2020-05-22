from app import db
import os
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from passlib.hash import sha256_crypt


class Base(db.Model):

    __abstract__ = True

    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def to_dict(self):
        d = {}
        for c in self.__dict__.keys():
            if c != '_sa_instance_state':
                d[c] = self.__dict__[c]
        return d


class AppClients(Base):
    __tablename__ = 'app_clients'

    id = db.Column(db.String(36), primary_key=True, default=uuid.uuid4())
    _password = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(255), unique=True)
    scopes = db.Column(db.String)
    age = db.Column(db.Integer)
    position = db.Column(db.String(255))

    def __init__(self, name, password):

        self.name = name
        self._password = sha256_crypt.encrypt(password)        

    def check_password(self, plaintext_password):
        return sha256_crypt.verify(plaintext_password, self._password)

    def set_password(self, plaintext_password):
        self._password = sha256_crypt.encrypt(plaintext_password)
