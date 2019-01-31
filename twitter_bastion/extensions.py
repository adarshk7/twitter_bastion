from flask import current_app
from py2neo import Graph


class Neo4jConnection(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.extensions['graph'] = Graph(
            bolt=app.config.get('NEO4J_BOLT', True),
            host=app.config.get('NEO4J_SERVER_ADDRESS', 'localhost'),
            bolt_port=app.config.get('NEO4J_PORT', 7687),
            user=app.config['NEO4J_USER'],
            password=app.config['NEO4J_PASSWORD'],
        )

    def _get_app(self, app=None):
        if app is not None:
            return app
        if current_app is not None:
            return current_app
        if self.app is not None:
            return self.app
        raise RuntimeError('No applicationr registered.')

    @property
    def graph(self, app=None):
        app = self._get_app(app=app)
        return app.extensions['graph']


db = Neo4jConnection()
