#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import multiprocessing
import sqlite3
from handlers import user_handler
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(ROOT_DIR)

from common.rabbitmq import on_message, publish_message

def init_db_connection():
    conn = sqlite3.connect('example.db')

def start_consuming_user_data():
    on_message("user_service_data", user_handler.handle_user_data)
    
def test():
    publish_message(queue_name="user_service_data", body="Funny ali")
    
def main():
    handler1 =  multiprocessing.Process(target=start_consuming_user_data)
    
    test_msg = multiprocessing.Process(target=test)
    
    handler1.start()
    
    time.sleep(10)
    
    test_msg.start()


if __name__ == '__main__':
    main()

    
    
    
