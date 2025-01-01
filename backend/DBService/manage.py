#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import multiprocessing
from DBService.handlers import handle_user_data
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(ROOT_DIR)

from common.rabbitmq import on_message, publish_message

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DBService.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def start_consuming_user_data():
    on_message("user_service_data", handle_user_data.handle_user_data)
    
def test():
    publish_message(queue_name="user_service_data", body="Funny ali")
    
if __name__ == '__main__':
    # Django App
    # djapp = multiprocessing.Process(target=main)
    
    # DB handlers
    handler1 =  multiprocessing.Process(target=start_consuming_user_data)
    
    test = multiprocessing.Process(target=test)
    
    # djapp.start()
    handler1.start()
    
    time.sleep(10)
    
    test.start()
    
    
    
