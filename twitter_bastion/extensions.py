from flask import current_app
from py2neo import Graph
from twitter import Api
from werkzeug.local import LocalProxy


class _ApplicationExtension(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def _get_app(self, app=None):
        if app is not None:
            return app
        if current_app is not None:
            return current_app
        if self.app is not None:
            return self.app
        raise RuntimeError('No application registered.')


class Neo4jConnection(_ApplicationExtension):
    def init_app(self, app):
        app.extensions['graph'] = Graph(
            bolt=app.config.get('NEO4J_BOLT', True),
            host=app.config.get('NEO4J_SERVER_ADDRESS', 'localhost'),
            bolt_port=app.config.get('NEO4J_PORT', 7687),
            user=app.config['NEO4J_USER'],
            password=app.config['NEO4J_PASSWORD'],
        )

    @property
    def graph(self, app=None):
        app = self._get_app(app=app)
        return app.extensions['graph']


class TwitterAPI(_ApplicationExtension):
    def init_app(self, app):
        app.extensions['twitter_api'] = Api(
            app.config['CONSUMER_KEY'],
            app.config['CONSUMER_SECRET'],
            app.config['ACCESS_TOKEN'],
            app.config['ACCESS_TOKEN_SECRET'],
        )

    @property
    def api(self, app=None):
        app = self._get_app(app=app)
        return app.extensions['twitter_api']


db = LocalProxy(Neo4jConnection)
twitter = LocalProxy(TwitterAPI)
