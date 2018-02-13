import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rekrutacja.settings')


app = Celery('rekrutacja',
             broker='amqp://localhost',
             backend='rpc://',
             include=['skaner.tasks'])
