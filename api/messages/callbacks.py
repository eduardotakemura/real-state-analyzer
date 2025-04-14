import logging
import json

logger = logging.getLogger(__name__)

def _decode_body(body):
    try:
        if isinstance(body, bytes):
            return json.loads(body.decode('utf-8'))
        return body
    except json.JSONDecodeError:
        return body.decode('utf-8') if isinstance(body, bytes) else str(body)

def analyzer_callback(ch, method, properties, body):
    decoded_body = _decode_body(body)
    logger.info(f"Received Analyzer response: {decoded_body}")

def price_prediction_callback(ch, method, properties, body):
    decoded_body = _decode_body(body)
    logger.info(f"Received Price Prediction response: {decoded_body}")

def training_callback(ch, method, properties, body):
    decoded_body = _decode_body(body)
    logger.info(f"Received Training response: {decoded_body}")

def scraper_callback(ch, method, properties, body):
    decoded_body = _decode_body(body)
    logger.info(f"Received Scraping response: {decoded_body}")
