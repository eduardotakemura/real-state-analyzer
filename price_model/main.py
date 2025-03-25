import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=600, blocked_connection_timeout=300, port=5672, credentials=pika.PlainCredentials('guest', 'guest')))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='dummy_queue', durable=True)
channel.queue_declare(queue='dummy_response_queue', durable=True)

def callback(ch, method, properties, body):
    print(f"Received {body}")
    channel.basic_publish(exchange='', routing_key='dummy_response_queue', body=f"Received: {body}", properties=pika.BasicProperties(delivery_mode=2))

channel.basic_consume(queue='dummy_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()

