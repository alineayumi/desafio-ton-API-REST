from flask import Blueprint

from .controller import HealthCheck, MockEndpoint


def setup_blueprint():

    bp = Blueprint("mock-api", __name__, url_prefix="/mock-api")

    bp.add_url_rule('/health-check', view_func=HealthCheck.as_view('health-check'))
    bp.add_url_rule('/mock', view_func=MockEndpoint.as_view('mock'))

    return bp
