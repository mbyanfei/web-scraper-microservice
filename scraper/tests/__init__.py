import os
import unittest

from flask_script import Command, Option

basedir = os.path.abspath(os.path.dirname(__file__))


class TestCommand(Command):
    def get_options(self):
        return (
            Option('-v', '--verbosity',
                   dest='verbosity',
                   type=int,
                   default=1),
        )

    def run(self, *args, **kwargs):
        tests = unittest.TestLoader().discover(__name__, pattern='*.py')
        unittest.TextTestRunner(verbosity=kwargs.get('verbosity')).run(tests)


class TestConfig:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
