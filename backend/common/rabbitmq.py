import pika
from main_settings import RABBITMQ_HOST, RABBITMQ_PORT

def start_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
    return connection

def publish_message(queue_name, body, reply_to_queue_name):
    connection = start_connection()
    channel = connection.channel()
    
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=body, 
                          properties=pika.BasicProperties(reply_to=reply_to_queue_name))
    
    connection.close()

def on_message(queue_name, handleRequest):
    connection = start_connection()
    channel = connection.channel()
    
    def callback(channel, method, properties, body):
        
        response = handleRequest(body)
        
        if properties.reply_to is not None:
            reply(channel, properties, response)
    
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)
    
    connection.start_consuming()

def reply(channel, properties, response):
    channel.basic_publish(exchange='', body=response, properties=pika.BasicProperties(correlation_id = properties.correlation_id))