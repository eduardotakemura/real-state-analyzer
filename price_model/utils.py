import requests
import pandas as pd
from preprocessor import Preprocessor
from model import PriceModel

def run_training(filters: dict):
    try:
        if 'operation' not in filters:
            print(" [!] Operation not found in the request body")
            return False
        
        operation = filters['operation']

        # Fetch data
        df = _fetch_data(operation)

        if not df:
            print(" [!] No data found for the operation")
            return False

        # Preprocess data
        preprocessor = Preprocessor()
        df_preprocessed = preprocessor.process_df(df)
        
        # Train model
        price_model = PriceModel()
        price_model.models_training(df_preprocessed, operation)
        
        return True
        
    except Exception as e:
        print(f"Error in training loop: {e}")
        return e

def make_prediction(input_data):
    try:
        price_model = PriceModel()
        prediction = price_model.make_prediction(input_data)
        return prediction 

    except Exception as e:
        print(f"Error during prediction: {e}")
        return e

def _fetch_data(operation: str):
    try:
        print(f" [*] Fetching data from API")
        response = requests.post(f"http://api:8000/properties/filter", json={"operation": operation}, timeout=10)
        response.raise_for_status() 
        data = response.json()

        # Convert to dataframe
        print(f" [*] Converting to dataframe")
        df = pd.DataFrame(data)
        
        # Return dataframe
        print(f" [*] Returning dataframe")
        return df
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return False
    
    
    


