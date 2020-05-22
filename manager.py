import os
from app import create_app, db
from app.database import AppClients
from flask_script import Manager, Shell

app = create_app(os.getenv("APP_SETTINGS", default="config.ProductionConfig"))
manager = Manager(app)


def make_shell_context():
    return dict(app=app, AppClients=AppClients, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()