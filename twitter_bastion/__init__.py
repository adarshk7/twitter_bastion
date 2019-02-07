import os

from flask import Flask

from .extensions import db, twitter


class Application(Flask):
    def __init__(self, environment=None):
        super(Application, self).__init__(__name__)
        self._init_settings()
        self._init_extensions()

    def _init_settings(self, environment=None):
        if environment is None:
            environment = os.environ.get('FLASK_ENV', 'development')
        settings_module = 'twitter_bastion.settings.' + environment
        self.config.from_object(settings_module)

    def _init_extensions(self):
        db.init_app(self)
        twitter.init_app(self)


app = Application()

import twitter_bastion.api  # noqa
