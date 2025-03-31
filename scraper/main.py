from driver import Driver
from scraper import Scraper
from preprocessor import Preprocessor
from datetime import datetime
import pika
import json
import time
from pika.exceptions import AMQPConnectionError

def start_scrapping(input):
    # Initialize the webdriver
    config = Driver()
    driver = config.start_driver()
    
    script_date = datetime.now().strftime('%Y-%m-%d')
    scraper = Scraper(driver, script_date)

    result = scraper.start(input['url'], input['pages'], input['file_name'], input['operation'])

    return result
    # url = 'https://www.vivareal.com.br/aluguel/sp/sao-paulo/#onde=Brasil,S%C3%A3o%20Paulo,S%C3%A3o%20Paulo,,,,,,BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo,,,'
    # pages = 10
    # file_name = 'rent'
    # operation = 'renting'

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

# url = 'https://www.vivareal.com.br/aluguel/sp/sao-paulo/#onde=Brasil,S%C3%A3o%20Paulo,S%C3%A3o%20Paulo,,,,,,BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo,,,'
# pages = 1
# file_name = 'rent'
# operation = 'renting'
# input = {'url': url, 'pages': pages, 'file_name': file_name, 'operation': operation}
# start_scrapping(input)

preprocessor = Preprocessor()
# file = 'data/2025-03-31/rent.csv'
file = 'data/2025-03-31/rent_preprocessed.csv'
preprocessor.include_lat_lng(file)

# try:
#     connection = create_connection()
#     channel = connection.channel()

#     channel.queue_declare(queue='scraper_queue', durable=True)
#     channel.queue_declare(queue='scraper_response_queue', durable=True)

#     def callback(ch, method, properties, body):
#         print(f"Task received: {json.loads(body)}")
#         # Run scrapping
#         result = start_scrapping(json.loads(body))

#         # Preprocess data
#         file = result['file_name']

#         # Load data into db
        
#         # Send response
#         channel.basic_publish(
#             exchange='',
#             routing_key='scraper_response_queue',
#             body=f"Scraping completed, report: {result}",
#             properties=pika.BasicProperties(delivery_mode=2)
#         )

#     # Consume messages
#     channel.basic_consume(queue='scraper_queue', on_message_callback=callback, auto_ack=True)

#     print('Waiting for messages...')
#     channel.start_consuming()
# except AMQPConnectionError:
#     print("Could not establish connection to RabbitMQ after multiple retries")
#     raise


    
  