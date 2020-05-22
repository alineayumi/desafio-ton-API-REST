from flask import has_request_context, request
from flask_jwt import current_identity
from logging import Formatter


class RequestFormatter(Formatter):
    def format(self, record):
        record.request_id = 'NA'
        record.app_client_key = 'NA'

        if has_request_context():
            record.request_id = request.environ.get("HTTP_X_REQUEST_ID")
            record.path = request.path
        if current_identity:
            record.app_client_key = current_identity.id

        return super().format(record)


formatter = RequestFormatter(
    '[%(asctime)s] [%(levelname)s] [%(request_id)s] [%(app_client_key)s] %(path)s: %(message)s')
