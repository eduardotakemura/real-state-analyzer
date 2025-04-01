import pandas as pd
import requests

class Loader:
    def __init__(self):
        self.df = None
        self.api_url = "http://api:8000/load-data"

    def load_data(self, file_name):
        self._load_df(file_name)
        result = self._make_request()
        return result

    def _load_df(self, file_name):
        self.df = pd.read_csv(file_name)

    def _make_request(self):
        try:
            response = requests.post(self.api_url, json=self.df.to_dict(orient="records"))
            response.raise_for_status()
            result = response.json()

            # Check if success (200)
            if result['success']:
                return True
            return False
        
        except Exception as e:
            print(f"Error loading data: {e}")
            return False


