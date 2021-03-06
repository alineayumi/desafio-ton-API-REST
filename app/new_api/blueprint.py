from flask import Blueprint

from .controller import HealthCheck, MockEndpoint, Home, Dashboard, Login, SignUp, Add, Edit, Delete


def setup_blueprint():

    bp = Blueprint("new-api", __name__, url_prefix="/new-api")

    bp.add_url_rule('/health-check', view_func=HealthCheck.as_view('health-check'))
    bp.add_url_rule('/mock', view_func=MockEndpoint.as_view('mock'))
    bp.add_url_rule('/', view_func=Home.as_view('home'))
    bp.add_url_rule('/admin/dashboard', view_func=Dashboard.as_view('dashboard'))
    bp.add_url_rule('/login', view_func=Login.as_view('login'))
    bp.add_url_rule('/sign-up', view_func=SignUp.as_view('sign-up'))
    bp.add_url_rule('/admin/add', view_func=Add.as_view('add'))
    bp.add_url_rule('/admin/edit', view_func=Edit.as_view('edit'))
    bp.add_url_rule('/admin/delete', view_func=Delete.as_view('delete'))

    return bp
