import pika
from analysis import run_analysis
import json
import time
from pika.exceptions import AMQPConnectionError

def create_connection():
    retries = 20
    while retries > 0:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='rabbitmq',
                    heartbeat=600,
                    blocked_connection_timeout=300,
                    port=5672,
                    credentials=pika.PlainCredentials('guest', 'guest')
                )
            )
            return connection
        except AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ. Retries left: {retries}")
            retries -= 1
            if retries == 0:
                raise e
            time.sleep(5)  # Wait 5 seconds before retrying

# Replace the direct connection creation with the retry function
try:
    connection = create_connection()
    channel = connection.channel()

    # Declare a queues
    channel.queue_declare(queue='analyzer_queue', durable=True)
    channel.queue_declare(queue='analyzer_response_queue', durable=True)

    def callback(ch, method, properties, body):
        print(body)
        # Run analysis
        report = run_analysis(json.loads(body))
        
        # Send response
        channel.basic_publish(
            exchange='',
            routing_key='analyzer_response_queue',
            body=f"{report}",
            properties=pika.BasicProperties(delivery_mode=2)
        )

    # Consume messages
    channel.basic_consume(queue='analyzer_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages...')
    channel.start_consuming()
except AMQPConnectionError:
    print("Could not establish connection to RabbitMQ after multiple retries")
    raise

