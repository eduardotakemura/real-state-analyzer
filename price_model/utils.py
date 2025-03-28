import requests
import pandas as pd
from preprocessor import Preprocessor
from model import PriceModel

def run_training():
    try:
        # Fetch data
        df = _fetch_data()

        # Preprocess data
        preprocessor = Preprocessor()
        preprocessor.drop_outliers = False
        df_preprocessed = preprocessor.process_df(df)
        
        # Train model
        price_model = PriceModel()
        price_model.models_training(df_preprocessed)
        
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

def retrieve_features_cols():
    try:
        price_model = PriceModel()
        price_model.load_models()
        features_cols = price_model.extra_features_cols
        return features_cols
    except Exception as e:
        print(f"Error in retrieving features columns: {e}")
        return e

def _fetch_data():
    try:
        print(f" [*] Fetching data from API")
        response = requests.get(f"http://api:8000/properties", timeout=10)
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
    
    
    


