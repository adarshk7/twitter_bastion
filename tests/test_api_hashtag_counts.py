import pytest
from flexmock import flexmock

from twitter_bastion.extensions import db


@pytest.mark.usefixtures('app_ctx')
class TestAPIHashtagCounts():
    @pytest.fixture
    def access_token(self, xhr_client):
        return xhr_client.post(
            '/auth', data={'username': 'fakeuser', 'password': 'fakepassword'}
        ).json['access_token']

    @pytest.fixture
    def fake_neo4j_result(self):
        return [
            {'h': {'value': 'abcde'[i]}, 'hashtag_count': 5 - i}
            for i in range(5)
        ]

    @pytest.fixture
    def cypher_query(self):
        return (
            'MATCH (t:Tweet)<-[:TAGGED_IN]-(h:Hashtag) '
            'RETURN h, count(t) AS hashtag_count '
            'ORDER BY hashtag_count DESC LIMIT 5'
        )

    def test_without_authentication(self, xhr_client, app):
        response = xhr_client.get('/hashtag_counts')
        assert response.status_code == 401

    def test_with_authentication(
        self, access_token, xhr_client, fake_neo4j_result, cypher_query
    ):
        (
            flexmock(db.graph)
            .should_receive('run')
            .with_args(cypher_query)
            .once()
            .and_return(fake_neo4j_result)
        )
        response = xhr_client.get(
            '/hashtag_counts', headers={'Authorization': f'JWT {access_token}'}
        )
        assert response.status_code == 200
        assert response.json == [
            {'hashtag': 'abcde'[i], 'count': 5 - i} for i in range(5)
        ]
