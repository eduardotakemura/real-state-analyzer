from sqlalchemy.orm import Session
from models import Properties
from fastapi import HTTPException

def get_all_properties(db: Session):
    try:
        return db.query(Properties).all()
    except Exception as e:
        _error_handler(e)

def get_properties_with_filter(db: Session, filters: dict):
    try:
        processed_filters = _extract_filters(filters)
        query = db.query(Properties)
        
        # Apply exact match filters
        exact_filters = {k: v for k, v in processed_filters.items() 
                        if not k.endswith('_gte') and not k.endswith('_lte')}
        if exact_filters:
            query = query.filter_by(**exact_filters)
        
        # Apply range filters
        if 'size_gte' in processed_filters:
            query = query.filter(Properties.size >= processed_filters['size_gte'])
        if 'size_lte' in processed_filters:
            query = query.filter(Properties.size <= processed_filters['size_lte'])
        if 'price_gte' in processed_filters:
            query = query.filter(Properties.price >= processed_filters['price_gte'])
        if 'price_lte' in processed_filters:
            query = query.filter(Properties.price <= processed_filters['price_lte'])
    
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

def get_error():
    error = Exception('Error route is working!')
    _error_handler(error)

## ---------------- Utilities Methods ---------------- ##
def _error_handler(error: Exception):
    message = 'An error occurred while processing the request'
    error_details = str(error)
    raise HTTPException(status_code=500, detail={
        'message': message,
        'error': error_details
    })

def _extract_filters(requested_filters: dict):
    # Initiate filters list #
    filters = {}

    # Helper function to safely get integer values
    def safe_int(value):
        try:
            return int(value) if value not in (None, '', 'All') else None
        except (ValueError, TypeError):
            return None

    # Process each filter only if it exists and has a valid value
    if 'operation' in requested_filters and requested_filters['operation']:
        filters['operation'] = requested_filters['operation']
    
    if 'type' in requested_filters and requested_filters['type'] not in (None, '', 'All'):
        filters['type'] = requested_filters['type']
    
    if 'state' in requested_filters and requested_filters['state']:
        filters['state'] = requested_filters['state']
    
    if 'city' in requested_filters and requested_filters['city']:
        filters['city'] = requested_filters['city']
    
    if 'neighborhood' in requested_filters and requested_filters['neighborhood'] not in (None, '', 'All'):
        filters['neighborhood'] = requested_filters['neighborhood']

    # Handle numeric filters
    dorms = safe_int(requested_filters.get('dorms'))
    if dorms is not None:
        filters['dorms'] = dorms

    toilets = safe_int(requested_filters.get('toilets'))
    if toilets is not None:
        filters['toilets'] = toilets

    garages = safe_int(requested_filters.get('garage'))
    if garages is not None:
        filters['garage'] = garages

    min_size = safe_int(requested_filters.get('min_size'))
    if min_size is not None:
        filters['size_gte'] = min_size

    max_size = safe_int(requested_filters.get('max_size'))
    if max_size is not None:
        filters['size_lte'] = max_size

    min_price = safe_int(requested_filters.get('min_price'))
    if min_price is not None:
        filters['price_gte'] = min_price

    max_price = safe_int(requested_filters.get('max_price'))
    if max_price is not None:
        filters['price_lte'] = max_price

    return filters
