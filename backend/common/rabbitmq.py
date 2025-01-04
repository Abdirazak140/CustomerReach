import pika

def start_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672))
    return connection

def publish_message(queue_name, body, correlation_id):
    connection = start_connection()
    channel = connection.channel()
    
    callback_queue = "amq.rabbitmq.reply-to"

    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=body, 
                          properties=pika.BasicProperties(reply_to=callback_queue, correlation_id=correlation_id))
    
    connection.close()

def on_request(queue_name, handleRequest):
    print(f'Started consuming {queue_name}')
    
    connection = start_connection()
    channel = connection.channel()
    
    def callback(channel, method, properties, body):
        response = handleRequest(body.decode())
        reply(channel, properties, response)
    
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)
    
    channel.start_consuming()
    
def on_response(correlation_id):
    connection = start_connection()
    channel = connection.channel()
    
    callback_queue = "amq.rabbitmq.reply-to"
    
    def callback(channel, method, properties, body):
        if properties.correlation_id == correlation_id:
            response = body.decode()
            connection.close()
            
            return response

    channel.basic_consume(queue=callback_queue, auto_ack=True, on_message_callback=callback)

    channel.start_consuming()

def reply(channel, properties, response):
    channel.basic_publish(exchange='', body=response, properties=pika.BasicProperties(correlation_id = properties.correlation_id))