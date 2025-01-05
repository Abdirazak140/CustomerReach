import json
import pika

def start_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672))
    return connection

def publish_message(queue_name, body, correlation_id=None, reply_to=False):
    connection = start_connection()
    channel = connection.channel()
    
    callback_queue = f"reply-{correlation_id}" if reply_to else None

    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(body), 
                          properties=pika.BasicProperties(reply_to=callback_queue, correlation_id=correlation_id))
    
    connection.close()

def on_request(queue_name, handleRequest):
    print(f'Start consuming {queue_name}')
    
    connection = start_connection()
    channel = connection.channel()
    
    def callback(channel, method, properties, body):
        response = handleRequest(json.loads(body.decode()))
        
        if properties.reply_to is not None:
            reply(channel, properties, response)
    
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)
    
    channel.start_consuming()
    
def on_response(correlation_id):
    connection = start_connection()
    channel = connection.channel()
    
    callback_queue = f"reply-{correlation_id}"
    channel.queue_declare(queue=callback_queue)
    response = None
    
    def callback(channel, method, properties, body):
        nonlocal response
        response = json.loads(body.decode())
        channel.stop_consuming()

    channel.basic_consume(queue=callback_queue, auto_ack=True, on_message_callback=callback)
    
    channel.start_consuming()
    connection.close()
    
    return response

def reply(channel, properties, response):
    channel.queue_declare(queue=properties.reply_to)
    channel.basic_publish(exchange='', routing_key=properties.reply_to, body=json.dumps(response), properties=pika.BasicProperties(correlation_id = properties.correlation_id))