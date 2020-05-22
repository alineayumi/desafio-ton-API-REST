from datetime import datetime, date
from flask.views import MethodView
from app.resources.authentication import requires_auth, check_scopes
from flask import current_app
from .helper import (doSomething)
from flask_jwt import jwt_required, current_identity
from flask import jsonify


class HealthCheck(MethodView):
    def get(self):
        current_app.logger.info("mock logg")
        return {"mensagem": "ola"}


class MockEndpoint(MethodView):
    @jwt_required()
    @check_scopes(scopes=["sales"])
    def get(self):

        current_app.logger.info("mock logg")
        return jsonify({"now": datetime.now(), "today": date.today(), "identity": {"id": current_identity.id}})

