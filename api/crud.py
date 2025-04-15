from sqlalchemy.orm import Session
from models import Properties
from fastapi import HTTPException
from utils import export_to_csv
from sqlalchemy import func

def get_all_properties(db: Session):
    try:
        return db.query(Properties).all()
    except Exception as e:
        _error_handler(e)

def get_properties_with_filter(db: Session, filters: dict):
    try:
        query = db.query(Properties)
        
        # Apply exact match filters (excluding numeric fields that need range filtering)
        exact_filters = {k: v for k, v in filters.items() 
                        if not k.endswith('_gte') and not k.endswith('_lte') and
                        k not in ['dorms', 'garage', 'toilets']}
        if exact_filters:
            query = query.filter_by(**exact_filters)
        
        # Apply range filters for size and price
        if 'size_gte' in filters:
            query = query.filter(Properties.size >= filters['size_gte'])
        if 'size_lte' in filters:
            query = query.filter(Properties.size <= filters['size_lte'])
        if 'price_gte' in filters:
            query = query.filter(Properties.price >= filters['price_gte'])
        if 'price_lte' in filters:
            query = query.filter(Properties.price <= filters['price_lte'])
        
        # Apply minimum value filters for dorms, garage, and toilets
        if 'dorms' in filters:
            query = query.filter(Properties.dorms >= filters['dorms'])
        if 'garage' in filters:
            query = query.filter(Properties.garage >= filters['garage'])
        if 'toilets' in filters:
            query = query.filter(Properties.toilets >= filters['toilets'])
    
        return query.all()
    except Exception as e:
        _error_handler(e)

def get_initial_options(db: Session):
    try:
        # Get total number of entries
        total_entries = db.query(Properties).count()
        
        # Get distinct operations
        operations = [op[0] for op in db.query(Properties.operation).distinct().all()]
        
        return {
            "count": total_entries,
            "operations": operations
        }
    except Exception as e:
        _error_handler(e)

def get_properties_options(db: Session, operation: str):
    try:
        # Filter options by operation
        query = db.query(Properties).filter(Properties.operation == operation)

        total_entries = query.count()
        
        # Get distinct property types with counts
        types = db.query(Properties.type, func.count(Properties.type).label('count'))\
            .filter(Properties.operation == operation)\
            .group_by(Properties.type)\
            .order_by(func.count(Properties.type).desc())\
            .all()
        types = [t[0] for t in types]
        
        # Get distinct cities with counts
        cities = db.query(Properties.city, func.count(Properties.city).label('count'))\
            .filter(Properties.operation == operation)\
            .group_by(Properties.city)\
            .order_by(func.count(Properties.city).desc())\
            .all()
        cities = [c[0] for c in cities]
        
        # Get distinct neighborhoods, order alphabetically
        neighborhoods = db.query(Properties.neighborhood)\
            .filter(Properties.operation == operation)\
            .distinct()\
            .order_by(Properties.neighborhood.asc())\
            .all()
        neighborhoods = [n[0] for n in neighborhoods]
        
        # Get min and max size
        min_size = query.with_entities(Properties.size).order_by(Properties.size.asc()).first()[0]
        max_size = query.with_entities(Properties.size).order_by(Properties.size.desc()).first()[0]
        
        # Get min and max price
        min_price = query.with_entities(Properties.price).order_by(Properties.price.asc()).first()[0]
        max_price = query.with_entities(Properties.price).order_by(Properties.price.desc()).first()[0]
        
        return {
            "count": total_entries,
            "types": types,
            "cities": cities,
            "neighborhoods": neighborhoods,
            "min_size": min_size,
            "max_size": max_size,
            "min_price": min_price,
            "max_price": max_price
        }
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
        result = export_to_csv(properties)
        if not result:
            raise Exception('Error exporting to csv')
        return result
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

