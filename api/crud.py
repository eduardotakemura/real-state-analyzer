from sqlalchemy.orm import Session
from models import Properties
from fastapi import HTTPException
from utils import export_to_csv

def get_all_properties(db: Session):
    try:
        return db.query(Properties).all()
    except Exception as e:
        _error_handler(e)

def get_properties_with_filter(db: Session, filters: dict):
    try:
        query = db.query(Properties)
        
        # Apply exact match filters
        exact_filters = {k: v for k, v in filters.items() 
                        if not k.endswith('_gte') and not k.endswith('_lte')}
        if exact_filters:
            query = query.filter_by(**exact_filters)
        
        # Apply range filters
        if 'size_gte' in filters:
            query = query.filter(Properties.size >= filters['size_gte'])
        if 'size_lte' in filters:
            query = query.filter(Properties.size <= filters['size_lte'])
        if 'price_gte' in filters:
            query = query.filter(Properties.price >= filters['price_gte'])
        if 'price_lte' in filters:
            query = query.filter(Properties.price <= filters['price_lte'])
    
        return query.all()
    except Exception as e:
        _error_handler(e)

def get_properties_count(db: Session):
    try:
        return db.query(Properties).count()
    except Exception as e:
        _error_handler(e)

def get_property_by_id(db: Session, property_id: int):
    try:
        return db.query(Properties).filter(Properties.id == property_id).first()
    except Exception as e:
        _error_handler(e)

def get_export_to_csv(db: Session):
    try:
        properties = db.query(Properties).all()
        return export_to_csv(properties)
    except Exception as e:
        _error_handler(e)

def get_error():
    error = Exception('Error route is working!')
    _error_handler(error)

def load_data(db: Session, data: list):
    try:
        for record in data:
            # Check if property with this page_id already exists
            existing_property = db.query(Properties).filter(
                Properties.page_id == str(record['page_id'])
            ).first()

            if existing_property:
                # Update existing property
                for key, value in record.items():
                    setattr(existing_property, key, value)
            else:
                # Create new property
                new_property = Properties(**record)
                db.add(new_property)

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error loading data: {e}")
        return False

## ---------------- Utilities Methods ---------------- ##
def _error_handler(error: Exception):
    message = 'An error occurred while processing the request'
    error_details = str(error)
    raise HTTPException(status_code=500, detail={
        'message': message,
        'error': error_details
    })

