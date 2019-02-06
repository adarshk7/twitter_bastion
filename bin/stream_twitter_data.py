from flask import current_app

from twitter_bastion import Application
from twitter_bastion.extensions import twitter
from twitter_bastion.services import add_tweet_and_related_data


def stream_twitter_data():
    target_hashtag = current_app.config['TARGET_HASHTAG']
    for tweet_data in twitter.api.GetStreamFilter(track=[target_hashtag]):
        add_tweet_and_related_data(tweet_data)


if __name__ == '__main__':
    app = Application()
    with app.app_context():
        stream_twitter_data()
