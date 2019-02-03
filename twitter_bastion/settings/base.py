import os


# Neo4j settings

NEO4J_USER = os.environ.get('NEO4J_USER', 'neo4j')
NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', 'neo4j')

NEO4J_BOLT = os.environ.get('NEO4J_BOLT', True)
NEO4J_SERVER_ADDRESS = os.environ.get('NEO4J_SERVER_ADDRESS', 'localhost')
BOLT_PORT = os.environ.get('BOLT_PORT', 7687)


# Twitter API credentials

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')


# Target hashtag

TARGET_HASHTAG = os.environ['TARGET_HASHTAG']


# Authentication/Flask-JWT settings

SECRET_KEY = 'secret-key'
JWT_AUTH_USERNAME_KEY = 'username'
JWT_AUTH_PASSWORD_KEY = 'password'
