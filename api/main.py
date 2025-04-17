from fastapi import Depends, Request, Path, WebSocket
from sqlalchemy.orm import Session
import crud
from extensions import get_db, app
import messages.requests as req
from messages.messages import start_listener
from utils import extract_filters, get_scraping_input, get_data
from messages.callbacks import connected_clients

## ---------------- WebSocket ---------------- ##
@app.websocket("/ws-insights")
async def insights_websocket(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except:
        connected_clients.remove(websocket)
    finally:
        # Ensure client is removed from list
        if websocket in connected_clients:
            connected_clients.remove(websocket)

@app.websocket("/ws-price")
async def price_websocket(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except:
        connected_clients.remove(websocket)
    finally:
        # Ensure client is removed from list
        if websocket in connected_clients:
            connected_clients.remove(websocket)

## ---------------- Dependencies Methods ---------------- ##
async def get_filters(request: Request):
    filter_data = await request.json()
    return extract_filters(filter_data)

async def get_input(request: Request):
    input_data = await request.json()
    return input_data

## ---------------- RabbitMQ Listener ---------------- ##
@app.on_event("startup")
def startup_event():
    start_listener()

## ---------------- Requests ---------------- ##
# Request analysis
@app.post("/request-analysis")
def request_analysis(filters: dict = Depends(get_filters)):
    print(f" [*] Requesting analysis for filters: {filters}")
    request = req.send_analysis_request(filters)
    return {"message": f"{request}"}

# Request price prediction
@app.post("/request-price-prediction")
def request_price_prediction(input: dict = Depends(get_input)):
    print(f" [*] Requesting price prediction for input: {input}")
    request = req.send_price_prediction_request(input)
    return {"message": f"{request}"}

# Request training
@app.post("/request-training")
def request_training(input: dict):
    print(f" [*] Requesting training for input: {input}")
    request = req.send_training_request(input['operation'])
    return {"message": f"{request}"}

# Request scraping
@app.post("/request-scraping")
def request_scraping(input: dict = Depends(get_scraping_input)):
    print(f" [*] Requesting scraping for input: {input}")
    request = req.send_scraping_request(input)
    return {"message": f"{request}"}

## ---------------- Frontend Routes ---------------- ##
# Get initial options
@app.get("/properties/initial-options")
def initial_options(db: Session = Depends(get_db)):
    return crud.get_initial_options(db)

# Get properties options
@app.get("/properties/options/{operation}")
def properties_options(db: Session = Depends(get_db), operation: str = Path(..., description="Operation")):
    return crud.get_properties_options(db, operation)

# Get price models
@app.get("/price-models")
def get_price_models(db: Session = Depends(get_db)):
    return crud.get_all_price_models(db)

## ---------------- Properties Routes ---------------- ##
# Get all properties
@app.get("/properties")
def all_properties(db: Session = Depends(get_db)):
    return crud.get_all_properties(db)

# Get properties with filter
@app.post("/properties/filter")
def properties_with_filter(db: Session = Depends(get_db), filters: dict = Depends(get_filters)):
    return crud.get_properties_with_filter(db, filters)

## ---------------- Data Routes ---------------- ##
@app.get("/export-properties")
def export_properties(db: Session = Depends(get_db)):
    return crud.get_export_to_csv(db)

@app.post("/load-data")
def load_data(db: Session = Depends(get_db), data: list = Depends(get_data)):
    print(f" [*] Loading data: {len(data)} records")
    result = crud.load_data(db, data)
    return {"success": result, "message": f"Loaded {len(data)} records"}

