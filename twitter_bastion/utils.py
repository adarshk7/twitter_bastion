from datetime import datetime


def format_twitter_datetime_to_isoformat(value):
    return datetime.strptime(value, '%a %b %d %H:%M:%S %z %Y').isoformat()
