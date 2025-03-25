from fastapi import Depends, Request, Path
from sqlalchemy.orm import Session
from crud import get_all_properties, get_properties_with_filter, get_properties_count, get_property_by_id, get_error
from extensions import get_db, app
from messages import send_analysis_request, send_price_prediction_request, start_listener
from utils import extract_filters

## ---------------- Dependencies Methods ---------------- ##
async def get_filters(request: Request):
    filter_data = await request.json()
    return extract_filters(filter_data)

async def get_input(request: Request):
    input_data = await request.json()
    return input_data

## ---------------- Routes ---------------- ##
# Start RabbitMQ listener when FastAPI starts
@app.on_event("startup")
def startup_event():
    start_listener()
    
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/request-analysis")
def request_analysis(filters: dict = Depends(get_filters)):
    print(f" [*] Requesting analysis for filters: {filters}")
    request = send_analysis_request(filters)
    return {"message": f"{request}"}

@app.post("/request-price-prediction")
def request_price_prediction(input: dict = Depends(get_input)):
    print(f" [*] Requesting price prediction for input: {input}")
    request = send_price_prediction_request(input)
    return {"message": f"{request}"}

@app.get("/error")
def error_route():
    return get_error()

# Get all properties
@app.get("/properties")
def all_properties(db: Session = Depends(get_db)):
    return get_all_properties(db)

# Get properties with filter
@app.post("/properties/filter")
def properties_with_filter(db: Session = Depends(get_db), filters: dict = Depends(get_filters)):
    return get_properties_with_filter(db, filters)

# Get properties count
@app.get("/properties/count")
def properties_count(db: Session = Depends(get_db)):
    return get_properties_count(db)

# Get properties by id
@app.get("/properties/{property_id}")
def property_by_id(db: Session = Depends(get_db), property_id: int = Path(..., description="Property ID")):
    return get_property_by_id(db, property_id)

