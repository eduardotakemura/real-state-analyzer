import pika
import json

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

def send_training_request(operation: str):
    """Send a message to the RabbitMQ queue for training"""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='training_queue', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='training_queue',   
            body=json.dumps({"operation": operation}),
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
    
def send_scraping_request(input: dict): 
    """Send a message to the RabbitMQ queue for scraping"""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='scraper_queue', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='scraper_queue',
            body=json.dumps(input),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
        return f" [x] Sent Scraping request for input:'{input}'"
    except Exception as e:
        return f" [!] Error sending scraping request: {e}"

