from celery import Celery

from twitter_bastion import Application
from twitter_bastion.settings import celery as celeryconfig


celery_app = Celery('twitter_bastion.tasks')
celery_app.config_from_object(celeryconfig)


if __name__ == '__main__':
    app = Application()
    with app.app_context():
        celery_app.start()
