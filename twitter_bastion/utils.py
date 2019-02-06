from datetime import datetime


def format_twitter_datetime_to_isoformat(value):
    return datetime.strptime(value, '%a %b %d %H:%M:%S %z %Y').isoformat()


def round_datetime_to_nearest_minutes(value, minutes=1):
    return datetime(
        value.year,
        value.month,
        value.day,
        value.hour,
        value.minute - (value.minute % minutes)
    )
