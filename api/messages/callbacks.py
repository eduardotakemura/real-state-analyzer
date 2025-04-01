def analyzer_callback(ch, method, properties, body):
    print(f" [x] Received Analyzer response: {body}")

def price_prediction_callback(ch, method, properties, body):
    print(f" [x] Received Price Prediction response: {body}")

def training_callback(ch, method, properties, body):
    print(f" [x] Received Training response: {body}")
    
def features_cols_callback(ch, method, properties, body):
    print(f" [x] Received Features Columns response: {body}")

def scraper_callback(ch, method, properties, body):
    print(f" [x] Received Scraping response: {body}")
