import pandas as pd
import re
import requests
import time
import os
from geopy.distance import geodesic

class Preprocessor:
    def __init__(self):
        self.df = None
        self.api_url = "https://us1.locationiq.com/v1/search"
        self.API_KEY = os.getenv('LOCATION_IQ_API_KEY')

    def preprocess_data(self, file_name):
        self.df = pd.read_csv(file_name)
        self._extract_type()
        self._extract_address()
        self._clean_size()
        self._clean_price()
        self._clean_additional_costs()
        self._clean_details()
        self._clean_ids()
        self._clean_links()
        self._initiate_lat_lng()

        splitted_name = file_name.split('.csv')[0]
        self.save_to_csv(f'{splitted_name}_preprocessed.csv')

        return self.df

    def include_lat_lng(self, file_name):
        self.df = pd.read_csv(file_name)

        try:
            # Loop through each row
            for index, row in self.df.iterrows():
                # Check if lat, lng is already in df
                if self.df.at[index, 'latitude'] != 0.0 and self.df.at[index, 'longitude'] != 0.0:
                    continue

                # Extract full address for query
                address = f"{row['street']}, {row['neighborhood']}, {row['city']}"

                # Make request
                lat, lng = self._request_lat_lng(address)

                # Check if returned lat, lng, jump to next row
                if lat is None or lng is None:
                    continue

                # Include lat, lng
                self.df.at[index, 'latitude'] = float(lat)
                self.df.at[index, 'longitude'] = float(lng)

        except Exception as e:
            print(f"Error including lat, lng: {e}")

        # Handle outliers
        #self.handle_lat_lng_outliers()

        # Save to csv
        splitted_name = file_name.split('.csv')[0]
        self.save_to_csv(f'{splitted_name}_with_lat_lng.csv')

        return self.df

       
    def _request_lat_lng(self, address):
        try:
            # API limit
            time.sleep(0.75)

            url = f"{self.api_url}?key={self.API_KEY}&q={address}&format=json&limit=1"
            header = {"accept": "application/json"}
            response = requests.get(url, headers=header)
            response.raise_for_status()
            lat = response.json()[0]['lat']
            lng = response.json()[0]['lon']
            print(f"Lat, lng: {lat}, {lng}")
            return lat, lng
        
        except Exception as e:
            print(f"Error requesting lat, lng: {e}")
            return None
       
    def handle_lat_lng_outliers(self, max_distance_km=20):
        # Compute central point (mean latitude & longitude)
        center_lat = self.df["latitude"].mean()
        center_lng = self.df["longitude"].mean()
        center_point = (center_lat, center_lng)

        # Compute distances for each point
        def compute_distance(row):
            if row["latitude"] == 0.0 or row["longitude"] == 0.0:
                return 0.0
            point = (row["latitude"], row["longitude"])
            return geodesic(center_point, point).km

        self.df["distance_from_center"] = self.df.apply(compute_distance, axis=1)

        # Flag outliers (beyond 20km)
        self.df["is_outlier"] = self.df["distance_from_center"] > max_distance_km

        # Flag outliers
        self.df.loc[self.df["is_outlier"], ["latitude", "longitude"]] = 0.0

        # Drop helper columns
        self.df.drop(columns=["distance_from_center", "is_outlier"], inplace=True)


    def _extract_type(self):
        # Extract everything before 'para'
        pattern = r"^(.*?)\s+para"
        self.df['type'] = self.df['title'].apply(lambda x: re.search(pattern, x).group(1) if re.search(pattern, x) else None)
        
        # Drop title from df
        self.df.drop('title', axis=1, inplace=True)

    def _extract_address(self):
        def _split_address(address):
            # Pattern = street - neighborhood, city
            # 0 if null
            match = re.match(r"^(.*?)(?:\s*-\s*(.*?))?(?:,\s*(.*))?$", address)
            if match:
                street = match.group(1).strip() if match.group(1) else 0
                neighborhood = match.group(2).strip() if match.group(2) else 0
                city = match.group(3).strip() if match.group(3) else 0
                return pd.Series([street, neighborhood, city])
            return pd.Series([0,0,0])
        
        self.df[["street", "neighborhood", "city"]] = self.df["address"].apply(_split_address)

        # Ensure all cols are str
        self.df[["street", "neighborhood", "city"]] = self.df[["street", "neighborhood", "city"]].astype(str)
        self.df.drop("address", axis=1, inplace=True)
      
    def _clean_size(self):
      def _extract_size(size):
        # Look for digits
        match = re.search(r"(\d+)", str(size))
        return int(match.group(1)) if match else 0
      
      self.df["size"] = self.df["size"].apply(_extract_size)
    
    def _clean_price(self):
      def _extract_price(price):
        # Pattern R$ XXXX/mês
        match = re.search(r"R\$[\s]?([\d.,]+)", str(price))
        if match:
            return int(match.group(1).replace(".", "").replace(",", ""))
        return 0
      
      self.df["price"] = self.df["price"].apply(_extract_price)

    def _clean_additional_costs(self):
      def _extract_additional_costs(costs):
        if not costs or pd.isna(costs):
            return 0
        # Extract digits
        matches = re.findall(r"R\$[\s]?([\d.,]+)", costs)
        total = sum(int(amount.replace(".", "").replace(",", "")) for amount in matches)
        return total

      self.df["additional_costs"] = self.df["additional_costs"].apply(_extract_additional_costs)

    def _clean_details(self):
        def clean_numeric_field(value):
            if pd.isna(value):  
                return 0

            # If it's already an integer or float
            if isinstance(value, (int, float)):
                return int(value)

            # Convert to string and remove spaces
            value = str(value).strip()  
            
            # Match a single number (e.g., "3")
            if value.isdigit():
                return int(value)
            
            # Match range format (e.g., "3-4") and extract the larger number
            match = re.match(r"(\d+)-(\d+)", value)
            if match:
                return max(int(match.group(1)), int(match.group(2)))
            
            # If it's an unrecognized string, return 0
            return 0
        
        # Apply function to each column
        for col in ["dorms", "garage", "toilets"]:
            self.df[col] = self.df[col].apply(clean_numeric_field)

        # Ensure all columns are integers
        self.df[["dorms", "garage", "toilets"]] = self.df[["dorms", "garage", "toilets"]].astype(int)

    def _clean_ids(self):
        # Handle NaN
        self.df['id'] = self.df['id'].fillna(0)

        # Convert to int (getting rid of decimal part) and str
        self.df['id'] = self.df['id'].astype(int).astype(str)

    def _clean_links(self):
        # Handle NaN
        self.df['link'] = self.df['link'].fillna(0)

        # Convert to str
        self.df['link'] = self.df['link'].astype(str)

    def _initiate_lat_lng(self):
      # Initiate lat, lng
      self.df['latitude'] = 0.0
      self.df['longitude'] = 0.0

    def save_to_csv(self, file_name):
        self.df.to_csv(file_name, index=False)
