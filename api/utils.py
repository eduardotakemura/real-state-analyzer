from models import Properties
from io import StringIO
import csv
from fastapi import Request

def extract_filters(requested_filters: dict):
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

def export_to_csv(properties: list):
     # Get all column names from the Properties model
    columns = [column.name for column in Properties.__table__.columns]
    
    # Create CSV content
    csv_content = []
    csv_content.append(columns)  # Add header row
    
    # Add data rows
    for property in properties:
        row = [getattr(property, column) for column in columns]
        csv_content.append(row)
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write all rows to the CSV
    writer.writerows(csv_content)
    
    # Get the CSV string
    csv_string = output.getvalue()
    
    # Save locally
    with open('properties.csv', 'w') as file:
        file.write(csv_string)
    
    # Return length of the csv file
    return len(csv_string)
    
def get_scraping_input(input: dict):
    """Get the scraping input from the filters"""
    # Check if all fields are present
    if 'url' not in input or 'pages' not in input or 'file_name' not in input or 'operation' not in input or 'date' not in input or 'tasks' not in input:
        raise ValueError("Missing required fields in input")

    task = {
        'url': input['url'],
        'pages': input['pages'],
        'file_name': input['file_name'],
        'operation': input['operation'],
        'date': input['date'],
        'tasks': input['tasks']
    }

    return task

async def get_data(request: Request):
    """Get data from the request and convert it to a list of dictionaries"""
    data = await request.json()
    
    if not isinstance(data, list):
        raise ValueError("Data must be a list of records")
    
    # Validate that each record has the required fields based on Properties model
    required_fields = [column.name for column in Properties.__table__.columns if column.name != 'id']
    
    for record in data:
        missing_fields = [field for field in required_fields if field not in record]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
    
    return data
