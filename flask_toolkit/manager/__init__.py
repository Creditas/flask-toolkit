from flask_script import Manager
from .command_list_routes import command_list_routes


def create_application_manager(app):
    manager = Manager(app)

    @manager.command
    def list_routes():
        command_list_routes(app)

    return manager
