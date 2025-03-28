def analyzer_callback(ch, method, properties, body):
    print(f" [x] Received Analyzer response: {body}")  # Log response

def price_prediction_callback(ch, method, properties, body):
    print(f" [x] Received Price Prediction response: {body}")  # Log response

def training_callback(ch, method, properties, body):
    print(f" [x] Received Training response: {body}")  # Log response
    
def features_cols_callback(ch, method, properties, body):
    print(f" [x] Received Features Columns response: {body}")  # Log response