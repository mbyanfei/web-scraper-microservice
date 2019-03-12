from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app
from tests import TestCommand

manager = Manager(create_app())

manager.add_command('db', MigrateCommand)
manager.add_command('test', TestCommand)

if __name__ == '__main__':
    manager.run()
