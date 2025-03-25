import pika
import pandas as pd
from utils import correlation_matrix, location_plots, summarize_by_location, summarize_by_type, type_distribution
import requests
import json
import time
from pika.exceptions import AMQPConnectionError

def run_analysis(filters):
    # Fetch data from database
    df = _fetch_data(filters)
    
    # Run analysis
    # corr_matrix = correlation_matrix(df)
    # loc_plots = location_plots(df)
    # loc_summary = summarize_by_location(df)
    # type_summary = summarize_by_type(df)
    # type_dist = type_distribution(df)
    
    # Return analysis
    #return _format_response(corr_matrix, loc_plots, loc_summary, type_summary, type_dist)
    return df

def _fetch_data(filters):
    try:
        response = requests.post(f"http://api:8000/properties/filter", timeout=10, json=filters)
        response.raise_for_status() 
        data = response.json()
        print(len(data))
        
        # Convert to dataframe
        df = pd.DataFrame(data)
        print(df.head())
        print(df.columns)
        
        # Return dataframe
        return df
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

    
def _format_response(corr_matrix, loc_plots, loc_summary, type_summary, type_dist):
    response =  {
        "corr_matrix": corr_matrix,
        "loc_plots": loc_plots,
        "loc_summary": loc_summary,
        "type_summary": type_summary,
        "type_dist": type_dist
    }
    print(response)
    
    return response

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
        print(report)
        
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

