from twitter_bastion.utils import format_twitter_datetime_to_isoformat


class TestUtils(object):
    def test_format_twitter_datetime_to_isoformat(self):
        assert (
            format_twitter_datetime_to_isoformat(
                'Fri Dec 14 13:37:41 +0000 2018'
            ) == '2018-12-14T13:37:41+00:00'
        )
