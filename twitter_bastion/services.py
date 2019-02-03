from twitter_bastion.extensions import db
from twitter_bastion.models import Tweet, TwitterUser, Hashtag
from twitter_bastion.utils import format_twitter_datetime_to_isoformat


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
