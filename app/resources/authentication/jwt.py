from app.database import AppClients


def authenticate(app_client_id, password):
    app_client = AppClients.query.filter_by(id=app_client_id).first()
    if app_client and app_client.check_password(password):
        return app_client


def identity(payload):
    app_client_id = payload['identity']
    app_client = AppClients.query.filter_by(id=app_client_id).first()
    return app_client
