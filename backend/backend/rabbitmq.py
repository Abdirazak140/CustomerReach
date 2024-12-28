import pika
from settings import RABBITMQ_HOST, RABBITMQ_PORT

def start_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
    return connection

def send_message(queue_name, body, routing_key):
    connection = start_connection()
    channel = connection.channel()
    
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=routing_key, body=body)
    
    connection.close()

def on_request(queue_name):
    connection = start_connection()
    channel = connection.channel()
    
    def callback(ch, method, properties, body):
        # TODO: Process request and reply
        print(f" [x] Received {body}")
    
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(auto_ack=True, on_message_callback=callback)
    
    connection.start_consuming()

def reply():
    pass