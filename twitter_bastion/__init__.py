import os

from flask import Flask
from flask_jwt import JWT

from .extensions import db, twitter


class Application(Flask):
    def __init__(self, environment=None):
        super(Application, self).__init__(__name__)
        self._init_settings()
        self._init_extensions()
        self._init_authentication_hander()
        self._init_blueprints()

    def _init_settings(self, environment=None):
        if environment is None:
            environment = os.environ.get('FLASK_ENV', 'development')
        settings_module = 'twitter_bastion.settings.' + environment
        self.config.from_object(settings_module)

    def _init_extensions(self):
        db.init_app(self)
        twitter.init_app(self)

    def _init_authentication_hander(self):
        # For the sake of brevity, the authentication is based on a fake user.
        class FakeUser(object):
            id = 123
            username = 'fakeuser'
            password = 'fakepassword'
        fakeuser = FakeUser()

        def _authenticate(username, password):
            if fakeuser.username == username and fakeuser.password == password:
                return fakeuser

        def _identity(payload):
            return fakeuser

        jwt = JWT(self, _authenticate, _identity)
        jwt.init_app(self)

    def _init_blueprints(self):
        from twitter_bastion.api import api_blueprint
        self.register_blueprint(api_blueprint)


app = Application()
