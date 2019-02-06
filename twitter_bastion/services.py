from datetime import datetime, timedelta

from twitter_bastion.extensions import db
from twitter_bastion.models import Tweet, TwitterUser, Hashtag
from twitter_bastion.utils import (
    format_twitter_datetime_to_isoformat,
    round_datetime_to_nearest_minutes,
)


def add_tweet_and_related_data(data):
    transaction = db.graph.begin()

    tweet = Tweet()
    tweet.id = data['id']
    tweet.text = data['text']
    tweet.created_at = (
        format_twitter_datetime_to_isoformat(data['created_at'])
    )
    tweet.tweeter.add(add_twitter_user(data['user']))

    entities = data['entities']

    for row in entities['user_mentions']:
        tweet.user_mentions.add(add_twitter_user(row))

    for row in entities['hashtags']:
        tweet.hashtags.add(add_hashtag(row))

    transaction.create(tweet)
    transaction.commit()


def add_twitter_user(data):
    tweeter = TwitterUser()
    tweeter.id = data['id']
    tweeter.name = data['name']
    tweeter.screen_name = data['screen_name']
    tweeter.description = data.get('description')

    created_at = data.get('created_at')
    if created_at:
        tweeter.created_at = format_twitter_datetime_to_isoformat(created_at)

    return tweeter


def add_hashtag(data):
    hashtag = Hashtag()
    hashtag.value = data['text']
    return hashtag


def get_tweet_count_for_time_inteval(start_time, end_time):
    return db.graph.evaluate(
        f"MATCH (t:Tweet) "
        f"WHERE t.created_at >= '{start_time.isoformat()}' AND "
        f"      t.created_at < '{end_time.isoformat()}' AND"
        f"      NOT t:Archived "
        f"RETURN count(*)"
    )


def get_tweet_count_percent_difference_between_time_windows(
    window_1_start_time,
    window_1_end_time,
    window_2_start_time,
    window_2_end_time,
):
    window_1_count = get_tweet_count_for_time_inteval(
        window_1_start_time, window_1_end_time
    )
    window_2_count = get_tweet_count_for_time_inteval(
        window_2_start_time, window_2_end_time
    )
    if not window_1_count or not window_2_count:
        return 0
    return 100 * (float(window_2_count - window_1_count) / window_1_count)


def get_tweet_count_percent_difference_for_subsequent_time_windows(
    time_window_length_in_minutes, time_window_interval_in_minutes
):
    window_length_timedelta = timedelta(minutes=time_window_length_in_minutes)
    window_interval_timedelta = timedelta(
        minutes=time_window_interval_in_minutes
    )
    rounded_current_time = round_datetime_to_nearest_minutes(
        datetime.utcnow(), minutes=time_window_length_in_minutes
    )
    current_window_start_time = (
        rounded_current_time - window_length_timedelta
    )
    current_window_end_time = rounded_current_time
    previous_window_start_time = (
        current_window_start_time - window_interval_timedelta
    )
    previous_window_end_time = (
        current_window_end_time - window_interval_timedelta
    )
    return (
        get_tweet_count_percent_difference_between_time_windows(
            previous_window_start_time,
            previous_window_end_time,
            current_window_start_time,
            current_window_end_time,
        )
    )
