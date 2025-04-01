from pipeline import pipeline
import pika
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

try:
    connection = create_connection()
    channel = connection.channel()

    channel.queue_declare(queue='scraper_queue', durable=True)
    channel.queue_declare(queue='scraper_response_queue', durable=True)

    def callback(ch, method, properties, body):
        print(f"Task received: {json.loads(body)}")

        # Run pipeline
        report = pipeline(json.loads(body))
        print(f" [*] Report: {report}")

        # Send response
        channel.basic_publish(
            exchange='',
            routing_key='scraper_response_queue',
            body=f"Task completed.\nInput: {json.loads(body)}\nReport: {report}",
            properties=pika.BasicProperties(delivery_mode=2)
        )

    # Consume messages
    channel.basic_consume(queue='scraper_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages...')
    channel.start_consuming()
except AMQPConnectionError:
    print("Could not establish connection to RabbitMQ after multiple retries")
    raise