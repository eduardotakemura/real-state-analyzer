import pika
import threading
import time
from pika.exceptions import AMQPConnectionError
from .callbacks import analyzer_callback, price_prediction_callback, training_callback, features_cols_callback, scraper_callback

## ---- Listener ---- ##
def create_connection():
    print(" [*] Trying to connect to RabbitMQ...")
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

def message_listener():
    """Listen for responses from RabbitMQ"""
    try:
        # Create connection
        connection = create_connection()
        channel = connection.channel()

        # Declare queues
        channel.queue_declare(queue='analyzer_response_queue', durable=True)
        channel.queue_declare(queue='price_prediction_response_queue', durable=True)
        channel.queue_declare(queue='training_response_queue', durable=True)
        channel.queue_declare(queue='features_cols_response_queue', durable=True)
        channel.queue_declare(queue='scraper_response_queue', durable=True)

        # Consume messages
        channel.basic_consume(queue='analyzer_response_queue', on_message_callback=analyzer_callback, auto_ack=True)
        channel.basic_consume(queue='price_prediction_response_queue', on_message_callback=price_prediction_callback, auto_ack=True)
        channel.basic_consume(queue='training_response_queue', on_message_callback=training_callback, auto_ack=True)
        channel.basic_consume(queue='features_cols_response_queue', on_message_callback=features_cols_callback, auto_ack=True)
        channel.basic_consume(queue='scraper_response_queue', on_message_callback=scraper_callback, auto_ack=True)
        channel.start_consuming()
        
    except Exception as e:
        print(f" [!] Unexpected error: {e}")

# Run the listener in a separate thread
def start_listener():
    thread = threading.Thread(target=message_listener, daemon=True)
    thread.start()
