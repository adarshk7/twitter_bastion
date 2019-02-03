from flask import jsonify

from twitter_bastion import app
from twitter_bastion.extensions import db


@app.route('/')
def root():
    return "Hello World!"


@app.route('/hashtag_counts')
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
