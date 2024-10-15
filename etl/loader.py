import os
import pandas as pd
from api.extensions import Session
from api.models import Properties


class Loader:
    def __init__(self, script_date):
        self.script_date = script_date
        self.base_dir = os.path.join('..', 'data', 'processed')
        self.input_dir = os.path.join(self.base_dir, script_date)
        self.session = Session()

    def load_to_db(self):
        # List all processed files for the date
        files = self._get_files(self.input_dir)
        print(f'Loading data from: {self.input_dir}')
        print(f'Files to load: {files}')

        # Clean previous data
        self._clean_db()

        for file in files:
            full_file_path = os.path.join(self.input_dir, file)
            data = pd.read_csv(full_file_path)
            if self._load_data_from_csv(data):
                print(f'File successfully loaded into the db: {full_file_path}')

    def _load_data_from_csv(self, data):
        try:
            for index, row in data.iterrows():
                property = Properties(
                    page_id=row['id'],
                    link=row['link'],
                    scrapping_date=self.script_date,
                    title=row['title'],
                    operation=row['operation'],
                    address=row['address'],
                    size=row['size'],
                    dorms=row['dorms'],
                    toilets=row['toilets'],
                    garage=row['garage'],
                    price=row['price'],
                    additional_costs=row['additional_costs'] if not pd.isna(row['additional_costs']) else None,
                    features=row['features'] if not pd.isna(row['features']) else None,
                    type=row['type'],
                    street=row['street'],
                    neighborhood=row['neighborhood'],
                    city=row['city'],
                    state=row['state'],
                    latitude=row['latitude'],
                    longitude=row['longitude']
                )
                self.session.add(property)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f'Error loading file into db: {e}')
            return False
        finally:
            self.session.close()

    def _clean_db(self):
        self.session.query(Properties).delete()
        self.session.commit()

    @staticmethod
    def _get_files(input_dir):
        return [file for file in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, file))]
