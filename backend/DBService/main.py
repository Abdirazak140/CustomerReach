#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import multiprocessing
import sqlite3
import uuid
from handlers import user_handler, product_handler
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(ROOT_DIR)

from common.rabbitmq import on_request, on_response, publish_message

def start_consuming_user_data():
    on_request("user_data", user_handler.handle_user_data)

def start_consuming_product_data():
    on_request("product_data", product_handler.handle_product_data)

def main():
    user_handler =  multiprocessing.Process(target=start_consuming_user_data)
    product_handler =  multiprocessing.Process(target=start_consuming_product_data)
    
    user_handler.start()
    product_handler.start()
    
    
if __name__ == '__main__':
    main()

    
    
    
