import pika
from settings import RABBITMQ_HOST, RABBITMQ_PORT

def start_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
    return connection

def publish_message(queue_name, body):
    connection = start_connection()
    channel = connection.channel()
    
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=body, 
                          properties=pika.BasicProperties(reply_to=queue_name))
    
    connection.close()

def on_request(queue_name):
    connection = start_connection()
    channel = connection.channel()
    
    def callback(ch, method, properties, body):
        # TODO: Process request and reply
        print(f" [x] Received {body}")
        
        if False:
            reply(ch=ch, response=null, properties=properties)
    
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)
    
    connection.start_consuming()

def reply(ch, properties, response):
    ch.basic_publish(exchange='', body=response, properties=pika.BasicProperties(correlation_id = properties.correlation_id))