import pika
import threading
import time

def send_message(message):
    """Send a message to the RabbitMQ queue"""
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='analyzer_queue', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='analyzer_queue',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )

    print(f" [x] Sent Analyzer request '{message}'")
    connection.close()

def message_listener():
    """Listen for responses from the analyzer with a retry mechanism"""
    while True:
        try:
            print(" [*] Trying to connect to RabbitMQ...")
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()
            channel.queue_declare(queue='analyzer_response_queue', durable=True)

            def callback(ch, method, properties, body):
                print(f" [x] Received Analyzer response: {body}")  # Log response

            channel.basic_consume(queue='analyzer_response_queue', on_message_callback=callback, auto_ack=True)

            print(" [*] Connected! Waiting for Analyzer responses...")
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print(" [!] RabbitMQ not ready. Retrying in 5 seconds...")
            time.sleep(5)  # Wait before retrying
        except Exception as e:
            print(f" [!] Unexpected error: {e}")
            time.sleep(5)  # Avoid fast retry loops

# Run the listener in a separate thread
def start_listener():
    thread = threading.Thread(target=message_listener, daemon=True)
    thread.start()
