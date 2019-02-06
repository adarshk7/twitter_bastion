import time
from datetime import timedelta

from flask import current_app
from sentry_sdk import capture_message

from twitter_bastion.celery import celery_app
from twitter_bastion.extensions import db
from twitter_bastion.models import Tweet
from twitter_bastion.services import (
    get_tweet_count_percent_difference_for_subsequent_time_windows,
)


@celery_app.task
def archive_old_tweets():
    max_unarchived_tweets = current_app.config['MAX_UNARCHIVED_TWEETS']

    for record in db.graph.run(
        'MATCH (t:Tweet) '
        'WHERE NOT t:Archived '
        'RETURN t '
        'ORDER BY t.created_at DESC '
        'SKIP $max_unarchived_tweets',
        max_unarchived_tweets=max_unarchived_tweets
    ):
        archivable_tweet = Tweet()
        archivable_tweet.id = record['t']['id']
        archivable_tweet.archived = True
        db.graph.push(archivable_tweet)


@celery_app.task
def monitor_tweet_count_variation():
    time_window_length_in_minutes = (
        current_app.config['TIME_WINDOW_LENGTH_IN_MINUTES']
    )
    time_window_interval_in_minutes = (
        current_app.config['TIME_WINDOW_INTERVAL_IN_MINUTES']
    )
    warning_threshold_difference = (
        current_app.config['WARNING_THRESHOLD_DIFFERENCE']
    )
    # while True:
    difference = (
        get_tweet_count_percent_difference_for_subsequent_time_windows(
            time_window_length_in_minutes, time_window_interval_in_minutes
        )
    )
    if difference >= warning_threshold_difference:
        capture_message(
            f'Increase by {difference}% tweets since last time window.'
        )
    elif difference <= -warning_threshold_difference:
        capture_message(
            f'Reduction by {difference}% tweets since last time window.'
        )
