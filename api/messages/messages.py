import pika
import threading
import time
import logging
from .callbacks import analyzer_callback, price_prediction_callback, training_callback, scraper_callback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RabbitMQConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self._closing = False
        self._consumer_tag = None
        self._consuming = False
        self._connection_attempts = 0
        self._max_connection_attempts = 20
        self._reconnect_delay = 5

        # Queue callbacks mapping
        self.queue_callbacks = {
            'analyzer_response_queue': analyzer_callback,
            'price_prediction_response_queue': price_prediction_callback,
            'training_response_queue': training_callback,
            'scraper_response_queue': scraper_callback,
        }

    def connect(self):
        """Create connection to RabbitMQ"""
        logger.info('Connecting to RabbitMQ...')
        return pika.SelectConnection(
            pika.ConnectionParameters(
                host='rabbitmq',
                heartbeat=600,
                blocked_connection_timeout=300,
                port=5672,
                credentials=pika.PlainCredentials('guest', 'guest')
            ),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed
        )

    def on_connection_open(self, _unused_connection):
        """Called when connection is established"""
        logger.info('Connection opened')
        self._connection_attempts = 0
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        """Called when connection fails to open"""
        logger.error(f'Connection open failed: {err}')
        self._connection_attempts += 1
        if self._connection_attempts < self._max_connection_attempts:
            logger.info(f'Retrying connection in {self._reconnect_delay} seconds...')
            time.sleep(self._reconnect_delay)
            self.connection = self.connect()
            self.connection.ioloop.start()
        else:
            logger.error('Max connection attempts reached. Giving up.')

    def on_connection_closed(self, _unused_connection, reason):
        """Called when connection is closed"""
        self._channel = None
        if self._closing:
            self.connection.ioloop.stop()
        else:
            logger.warning(f'Connection closed, reopening in {self._reconnect_delay} seconds: {reason}')
            time.sleep(self._reconnect_delay)
            self.connection = self.connect()
            self.connection.ioloop.start()

    def open_channel(self):
        """Open a new channel"""
        logger.info('Creating a new channel')
        self.connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """Called when channel is opened"""
        logger.info('Channel opened')
        self.channel = channel
        self.setup_exchanges()

    def setup_exchanges(self):
        """Setup exchanges and queues"""
        for queue_name in self.queue_callbacks.keys():
            self.channel.queue_declare(
                queue=queue_name,
                durable=True,
                callback=lambda frame, q=queue_name: self.setup_queue(q)
            )

    def setup_queue(self, queue_name):
        """Setup queue and start consuming"""
        logger.info(f'Setting up queue: {queue_name}')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=lambda ch, method, properties, body: self.on_message(ch, method, properties, body, queue_name)
        )

    def on_message(self, ch, method, properties, body, queue_name):
        """Called when a message is received"""
        try:
            callback = self.queue_callbacks.get(queue_name)
            if callback:
                callback(ch, method, properties, body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.error(f'Error processing message: {e}')
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def run(self):
        """Run the consumer"""
        self.connection = self.connect()
        self.connection.ioloop.start()

    def stop(self):
        """Stop the consumer"""
        logger.info('Stopping consumer')
        self._closing = True
        if self.channel:
            self.channel.close()
        if self.connection:
            self.connection.close()
        logger.info('Consumer stopped')

def start_listener():
    """Start the RabbitMQ consumer in a separate thread"""
    consumer = RabbitMQConsumer()
    thread = threading.Thread(target=consumer.run, daemon=True)
    thread.start()
    return consumer
