import os


amqp_url = os.environ.get('AMQP_URL', 'amqp://guest:guest@127.0.0.1:5672/')
broker_url = amqp_url
result_backend = amqp_url
accept_content = ['json']
include = ['twitter_bastion.tasks']
task_serializer = 'json'

beat_schedule = {
    'archive-old-tweets': {
        'task': 'twitter_bastion.tasks.archive_old_tweets',
        'schedule': float(os.environ.get('ARCHIVING_INTERVAL', 60)),
    },
    'monitor-tweet-count-variation': {
        'task': 'twitter_bastion.tasks.monitor_tweet_count_variation',
        'schedule': float(os.environ.get('MONITORING_INTERVAL', 300)),
    },
}
