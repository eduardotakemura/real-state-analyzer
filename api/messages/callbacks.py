import logging
import json
import asyncio
from typing import List
from fastapi import WebSocket

logger = logging.getLogger(__name__)

connected_clients: List[WebSocket] = []

async def broadcast_report(message: dict):
    """Broadcast a message to all connected WebSocket clients"""
    logger.info(f"Broadcasting report to {len(connected_clients)} clients")
    for client in connected_clients:
        try:
            await client.send_json(message)
        except:
            # Remove client if it's disconnected
            connected_clients.remove(client)

## ---------------- Callbacks ---------------- ##
def analyzer_callback(ch, method, properties, body):
    logger.info(f"Received Analyzer Response")
    try:
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Decode the body if it's bytes
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        
        # Parse the JSON if it's a string
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                logger.error("Failed to decode JSON from body")
                return
        
        # Broadcast the message
        loop.run_until_complete(broadcast_report({
            "type": "analysis",
            "data": body
        }))
        
        # Close the loop
        loop.close()
    except Exception as e:
        logger.error(f"Error in analyzer_callback: {e}")
    
def price_prediction_callback(ch, method, properties, body):
    decoded_body = json.loads(body)
    logger.info(f"Received Price Prediction response: {decoded_body}")

def training_callback(ch, method, properties, body):
    decoded_body = json.loads(body)
    logger.info(f"Received Training response: {decoded_body}")


def scraper_callback(ch, method, properties, body):
    decoded_body = json.loads(body)
    logger.info(f"Received Scraper response: {decoded_body}")

