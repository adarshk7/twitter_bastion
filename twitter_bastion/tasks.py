from flask import current_app

from twitter_bastion.celery import celery_app
from twitter_bastion.extensions import twitter
from twitter_bastion.services import add_tweet_and_related_data


@celery_app.task
def stream_twitter_data():
    target_hashtag = current_app.config['TARGET_HASHTAG']
    for tweet_data in twitter.api.GetStreamFilter(track=[target_hashtag]):
        add_tweet_and_related_data(tweet_data)
