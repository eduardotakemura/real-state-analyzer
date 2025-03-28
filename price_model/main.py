import pika
import time
import json
from pika.exceptions import AMQPConnectionError
from utils import run_training, make_prediction, retrieve_features_cols

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

    # Declare a queues
    channel.queue_declare(queue='price_prediction_queue', durable=True)
    channel.queue_declare(queue='price_prediction_response_queue', durable=True)
    channel.queue_declare(queue='training_queue', durable=True)
    channel.queue_declare(queue='training_response_queue', durable=True)
    channel.queue_declare(queue='features_cols_queue', durable=True)
    channel.queue_declare(queue='features_cols_response_queue', durable=True)

    def training_callback(ch, method, properties, body):
        print(f" [*] Training Task received")
        # Run training
        result = run_training()
        
        if result:
            response = "Training completed"
        else:
            response = "Training failed"
            
        # Send response
        channel.basic_publish(
            exchange='',
            routing_key='training_response_queue',
            body=response,
            properties=pika.BasicProperties(delivery_mode=2)
        )

    def price_prediction_callback(ch, method, properties, body):
        print(f" [*] Price Prediction Task received")
        print(f"[*] Input data: {body}")

        # Make prediction
        prediction = make_prediction(json.loads(body))

        # Send response
        channel.basic_publish(
            exchange='',
            routing_key='price_prediction_response_queue',
            body=f"Price prediction completed: {prediction}",
            properties=pika.BasicProperties(delivery_mode=2)
        )
        
    def features_cols_callback(ch, method, properties, body):
        print(f" [*] Features Columns Task received")
        # Retrieve features columns
        features_cols = retrieve_features_cols()

        # Send response
        channel.basic_publish(
            exchange='',
            routing_key='features_cols_response_queue',
            body=f"Features columns retrieved: {features_cols}",
            properties=pika.BasicProperties(delivery_mode=2)
        )
        
    # Consume messages
    channel.basic_consume(queue='price_prediction_queue', on_message_callback=price_prediction_callback, auto_ack=True)
    channel.basic_consume(queue='training_queue', on_message_callback=training_callback, auto_ack=True)
    channel.basic_consume(queue='features_cols_queue', on_message_callback=features_cols_callback, auto_ack=True)

    print('Waiting for messages...')
    channel.start_consuming()
except AMQPConnectionError:
    print("Could not establish connection to RabbitMQ after multiple retries")
    raise

