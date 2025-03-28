from fastapi import Depends, Request, Path
from sqlalchemy.orm import Session
import crud
from extensions import get_db, app
from messages.requests import send_analysis_request, send_price_prediction_request, send_training_request, send_features_cols_request
from messages.messages import start_listener
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

## ---------------- Requests ---------------- ##
# Request analysis
@app.post("/request-analysis")
def request_analysis(filters: dict = Depends(get_filters)):
    print(f" [*] Requesting analysis for filters: {filters}")
    request = send_analysis_request(filters)
    return {"message": f"{request}"}

# Request price prediction
@app.post("/request-price-prediction")
def request_price_prediction(input: dict = Depends(get_input)):
    input["features"] = [0 for _ in range(21)]
    print(f" [*] Requesting price prediction for input: {input}")
    request = send_price_prediction_request(input)
    return {"message": f"{request}"}

# Request training
@app.get("/request-training")
def request_training():
    print(f" [*] Requesting training")
    request = send_training_request()
    return {"message": f"{request}"}

# Request features columns
@app.get("/request-features-cols")
def request_features_cols():
    print(f" [*] Requesting features columns")
    request = send_features_cols_request()
    return {"message": f"{request}"}

## ---------------- Properties Routes ---------------- ##
# Get all properties
@app.get("/properties")
def all_properties(db: Session = Depends(get_db)):
    return crud.get_all_properties(db)

# Get properties with filter
@app.post("/properties/filter")
def properties_with_filter(db: Session = Depends(get_db), filters: dict = Depends(get_filters)):
    return crud.get_properties_with_filter(db, filters)

# Get properties count
@app.get("/properties/count")
def properties_count(db: Session = Depends(get_db)):
    return crud.get_properties_count(db)

# Get properties by id
@app.get("/properties/{property_id}")
def property_by_id(db: Session = Depends(get_db), property_id: int = Path(..., description="Property ID")):
    return crud.get_property_by_id(db, property_id)

@app.get("/export-properties")
def export_properties(db: Session = Depends(get_db)):
    return crud.get_export_to_csv(db)

