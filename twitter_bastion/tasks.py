import time

from flask import current_app

from twitter_bastion.celery import celery_app
from twitter_bastion.extensions import db, twitter
from twitter_bastion.models import Tweet
from twitter_bastion.services import add_tweet_and_related_data


@celery_app.task
def stream_twitter_data():
    target_hashtag = current_app.config['TARGET_HASHTAG']
    for tweet_data in twitter.api.GetStreamFilter(track=[target_hashtag]):
        add_tweet_and_related_data(tweet_data)


@celery_app.task
def archive_old_tweets():
    max_unarchived_tweets = current_app.config['MAX_UNARCHIVED_TWEETS']
    archiving_interval = current_app.config['ARCHIVING_INTERVAL']

    while True:
        transaction = db.graph.begin()
        for archivable_tweet in (
            Tweet.match(db.graph)
            .where('NOT _:Archived')
            .order_by('_.created_at DESC')
            .skip(max_unarchived_tweets)
        ):
            archivable_tweet.archived = True
            transaction.push(archivable_tweet)
        transaction.commit()
        time.sleep(archiving_interval)
