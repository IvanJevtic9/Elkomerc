from celery import shared_task
from time import sleep

import requests
import json

AUTH_ENDPOINT = "http://localhost:8000/api/auth/"

@shared_task
def sleepy(duration=10, task_id=None):
    sleep(duration)
    return None


@shared_task
def schedular_import():
    auth_request = {
        'email': 'sinisa9@gmail.com',
        'password': 'sicapica1412'
    }
    post_header = {
        'Content-Type': 'application/json'
    }
    return 5