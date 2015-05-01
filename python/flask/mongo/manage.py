from flask.ext.script import Server, Manager
from app import app

manager = Manager(app)
manager.add_command("runserver", Server())

if __name__ == "__main__":
    manager.run()