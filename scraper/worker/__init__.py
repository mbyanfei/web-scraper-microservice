from app import create_celery_app

celery_app = create_celery_app()

from worker.tasks import *
