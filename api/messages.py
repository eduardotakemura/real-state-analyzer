import pika
import threading
import time
from pika.exceptions import AMQPConnectionError
import json

## ---- Requests ---- ##
def send_analysis_request(filters: dict):
    """Send a message to the RabbitMQ queue for analysis"""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='analyzer_queue', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='analyzer_queue',
            body=json.dumps(filters),
            properties=pika.BasicProperties(delivery_mode=2)
            )
        connection.close()
        return f" [x] Sent Analyzer request for filters:'{filters}'"
    except Exception as e:
        return f" [!] Error sending analysis request: {e}"

def send_price_prediction_request(input: dict):
    """Send a message to the RabbitMQ queue for price prediction"""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='price_prediction_queue', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='price_prediction_queue',
            body=json.dumps(input),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
        return f" [x] Sent Price Prediction request for input:'{input}'"
    except Exception as e:
        return f" [!] Error sending price prediction request: {e}"

def send_training_request():
    """Send a message to the RabbitMQ queue for training"""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='training_queue', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='training_queue',   
            body=json.dumps({}),
            properties=pika.BasicProperties(delivery_mode=2)    
        )
        connection.close()
        return f" [x] Sent Training request"
    except Exception as e:
        return f" [!] Error sending training request: {e}"

def send_features_cols_request(): 
    """Send a message to the RabbitMQ queue for features columns"""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='features_cols_queue', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='features_cols_queue',
            body=json.dumps({}),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
        return f" [x] Sent Features Columns request"
    except Exception as e:
        return f" [!] Error sending features columns request: {e}"


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
        connection = create_connection()
        channel = connection.channel()
        channel.queue_declare(queue='analyzer_response_queue', durable=True)
        channel.queue_declare(queue='price_prediction_response_queue', durable=True)
        channel.queue_declare(queue='training_response_queue', durable=True)
        channel.queue_declare(queue='features_cols_response_queue', durable=True)

        def analyzer_callback(ch, method, properties, body):
            print(f" [x] Received Analyzer response: {body}")  # Log response

        def price_prediction_callback(ch, method, properties, body):
            print(f" [x] Received Price Prediction response: {body}")  # Log response

        def training_callback(ch, method, properties, body):
            print(f" [x] Received Training response: {body}")  # Log response
            
        def features_cols_callback(ch, method, properties, body):
            print(f" [x] Received Features Columns response: {body}")  # Log response

        channel.basic_consume(queue='analyzer_response_queue', on_message_callback=analyzer_callback, auto_ack=True)
        channel.basic_consume(queue='price_prediction_response_queue', on_message_callback=price_prediction_callback, auto_ack=True)
        channel.basic_consume(queue='training_response_queue', on_message_callback=training_callback, auto_ack=True)
        channel.basic_consume(queue='features_cols_response_queue', on_message_callback=features_cols_callback, auto_ack=True)
        channel.start_consuming()
        
    except Exception as e:
        print(f" [!] Unexpected error: {e}")

# Run the listener in a separate thread
def start_listener():
    thread = threading.Thread(target=message_listener, daemon=True)
    thread.start()
