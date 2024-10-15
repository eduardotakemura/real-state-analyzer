import pandas as pd
import re
import requests
import time
import os

class Preprocessor:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.API_KEY = os.getenv('OPENCAGE_KEY')

    def clean_scrapped_data(self, input_file_path):
        # Read scrapped file #
        data = pd.read_csv(input_file_path)

        # Extract and process features
        data = self.extract_type(data)
        data = self.extract_addresses(data)
        data = self.clean_details(data)
        data = self.clean_prices(data)
        data = self.clean_ids(data)
        data = self.clean_features(data)

        data.reset_index(drop=True, inplace=True)

        # Append latitude and longitude
        data = self.append_lat_lng(data)

        # Save the cleaned data to a CSV file without an index
        if self._save_file(data, input_file_path, self.output_dir):
            return True

        return False

    def extract_type(self, data):
        types = pd.Series(["Casa", "Apartamento", "Cobertura", "Flat"])
        data['type'] = data['title'].apply(lambda x: self._match_type(x, types))
        data['type'].replace({"Cobertura": "Apartamento", "Flat": "Apartamento"}, inplace=True)
        return data.dropna(subset=['type'])

    def extract_addresses(self, data):
        data[['street', 'neighborhood', 'city', 'state']] = data['address'].apply(self._split_address)
        return data

    def clean_details(self, data):
        data[['size', 'dorms', 'toilets', 'garage']] = data[['size', 'dorms', 'toilets', 'garage']].astype(str)
        mask = ~(data[['size', 'dorms', 'toilets', 'garage']].apply(lambda col: col.str.contains('-')).any(axis=1))
        data = data[mask]
        data[['size', 'dorms', 'toilets', 'garage']] = data[['size', 'dorms', 'toilets', 'garage']].astype(int)
        return data

    def clean_prices(self, data):
        data['price'] = pd.to_numeric(data['price'].str.extract('(\d+)')[0], errors='coerce')
        data['additional_costs'] = pd.to_numeric(data['additional_costs'], errors='coerce')
        return data.dropna(subset=['price', 'additional_costs'])

    def clean_ids(self, data):
        return data.drop_duplicates(subset=['id'])

    def clean_features(self, data):
        data['features'] = data['features'].fillna('').astype(str)
        data = data[~data['features'].str.strip().str.endswith('...')]
        return data

    def append_lat_lng(self, data):
        unique_locations = (data['neighborhood'] + ', ' + data['city'] + ', ' + data['state']).unique()
        proximity = self._get_proximity(unique_locations[0])

        location_lat_lng = {loc: self.get_lat_lng(loc, proximity=proximity) for loc in unique_locations}
        time.sleep(1)  # Respect API delay

        data['latitude'] = data.apply(
            lambda row: location_lat_lng.get(f"{row['neighborhood']}, {row['city']}, {row['state']}", (None, None))[0],
            axis=1)
        data['longitude'] = data.apply(
            lambda row: location_lat_lng.get(f"{row['neighborhood']}, {row['city']}, {row['state']}", (None, None))[1],
            axis=1)

        # Convert latitude and longitude to float and reorder columns
        data['latitude'] = data['latitude'].astype(float)
        data['longitude'] = data['longitude'].astype(float)
        return data

    def _match_type(self, title, types):
        matches = types[types.str.lower().apply(lambda x: x in title.lower())]
        return matches.iloc[0] if not matches.empty else None

    def _split_address(self, address):
        parts = [part.strip() for part in re.split(r',|-', address)]
        street = parts[0] if len(parts) > 0 else None
        neighborhood = parts[-3] if len(parts) >= 3 else (parts[0] if len(parts) == 2 else None)
        city, state = parts[-2], parts[-1] if len(parts) > 1 else (None, None)
        return pd.Series([street, neighborhood, city, state])

    def _get_proximity(self, location):
        lat, lng = self.get_lat_lng(location, countrycode='br')
        return f"{lat},{lng}" if lat and lng else None

    def get_lat_lng(self, location, countrycode=None, proximity=None):
        params = {'q': location, 'key': self.API_KEY, 'countrycode': countrycode, 'proximity': proximity}
        try:
            response = requests.get('https://api.opencagedata.com/geocode/v1/json', params=params)
            response.raise_for_status()
            data = response.json()
            if data['results']:
                return data['results'][0]['geometry']['lat'], data['results'][0]['geometry']['lng']
        except (requests.RequestException, KeyError, IndexError):
            pass
        return None, None

    def _save_file(self, data, input_file_path, output_path):
        try:
            # Extract file name #
            file_name = os.path.basename(input_file_path)

            # Join and get path to output folder #
            output_path = os.path.join(output_path, file_name)

            # Save data #
            data.to_csv(output_path, index=False)
            return True

        except Exception as e:
            print(f'An error occur during saving: {e}')
            return False
