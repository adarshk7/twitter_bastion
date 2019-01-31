from py2neo.ogm import GraphObject, Label, Property, RelatedFrom, RelatedTo


class Tweet(GraphObject):
    __primarykey__ = 'id'

    id = Property()  # This is a foreign id referencing id from the source.
    text = Property()
    created_at = Property()

    archived = Label()

    tweeter = RelatedFrom('TwitterUser', 'TWEETED')
    user_mentions = RelatedFrom('TwitterUser', 'MENTIONED_IN')

    hashtags = RelatedFrom('Hashtag', 'TAGGED_IN')


class TwitterUser(GraphObject):
    __primarykey__ = 'id'

    id = Property()  # This is a foreign id referencing id from the source.
    created_at = Property()
    name = Property()
    screen_name = Property()
    description = Property()

    tweeted = RelatedTo(Tweet)
    mentioned_in = RelatedTo(Tweet)


class Hashtag(GraphObject):
    __primarykey__ = 'value'

    value = Property()

    tagged_in = RelatedTo(Tweet)


class User(GraphObject):
    __primarykey__ = '__id__'

    name = Property()
    access_key_token = Property()
    access_key_secret = Property()
