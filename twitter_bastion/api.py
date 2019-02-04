from flask import Blueprint, jsonify
from flask_jwt import jwt_required

from twitter_bastion.extensions import db


api_blueprint = Blueprint(
    name='api_blueprint',
    url_prefix='',
    import_name=__name__,
)


@api_blueprint.route('/')
def root():
    return "Hello World!"


@api_blueprint.route('/hashtag_counts')
@jwt_required()
def hashtag_counts():
    return jsonify([
        {'hashtag': row['h']['value'], 'count': row['hashtag_count']}
        for row in db.graph.run(
            'MATCH (t:Tweet)<-[:TAGGED_IN]-(h:Hashtag) '
            'RETURN h, count(t) AS hashtag_count '
            'WHERE NOT t:Archived '
            'ORDER BY hashtag_count '
            'DESC LIMIT 5'
        )
    ]), 200
