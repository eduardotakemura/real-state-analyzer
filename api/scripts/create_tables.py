from extensions import engine, Base
from models import Properties, PriceModels
import logging
from sqlalchemy import inspect

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    try:
        logger.info("Starting table creation...")
        logger.info(f"Database URL: {engine.url}")
        
        # Get inspector to check existing tables
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        logger.info(f"Existing tables in database: {existing_tables}")
        
        # List of models to create
        models_to_create = [Properties, PriceModels]
        
        for model in models_to_create:
            table_name = model.__tablename__
            if table_name not in existing_tables:
                logger.info(f"Creating table: {table_name}")
                model.__table__.create(engine)
            else:
                logger.info(f"Table {table_name} already exists, skipping creation")
        
        # Verify final state of tables
        final_tables = inspector.get_table_names()
        logger.info(f"Final tables in database: {final_tables}")
            
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")
        raise

if __name__ == "__main__":
    create_tables() 