import os


amqp_url = os.environ.get('AMQP_URL', 'amqp://guest:guest@127.0.0.1:5672/')
broker_url = amqp_url
result_backend = amqp_url
accept_content = ['json']
include = ['twitter_bastion.tasks']
task_serializer = 'json'
