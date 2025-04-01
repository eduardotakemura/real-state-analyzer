from scraper import Scraper
from preprocessor import Preprocessor
from loader import Loader
from driver import Driver
import os

def pipeline(input):
    try:
        # Get operations list
        tasks = input['tasks']
        scraping_report = {}
        preprocessing_report = {}
        lat_lng_report = {}
        loading_report = {}


        # Run scraping pipeline
        if 'scrape' in tasks:
            scraping_report = run_scraping(input)
            print(f" [*] Scraping report: {scraping_report}")

        # Preprocess data
        if 'preprocess' in tasks:
            preprocessing_report = run_preprocessing(input['file_name'], input['date'])
            print(f" [*] Preprocessing report: {preprocessing_report}")


        # Fetch lat, lng from API and add to data
        if 'fetch_lat_lng' in tasks:
            lat_lng_report = fetch_lat_lng(input['file_name'], input['date'])
            print(f" [*] Lat, lng report: {lat_lng_report}")


        # Load data into db
        if 'load' in tasks:
            loading_report = load_data(input['file_name'], input['date'])
            print(f" [*] Loading report: {loading_report}")

        return {
            'scraping_report': scraping_report,
            'preprocessing_report': preprocessing_report,
            'lat_lng_report': lat_lng_report,
            'loading_report': loading_report
            }
    except Exception as e:
        print(f" [*] Error in pipeline: {e}")
        return {
            'message': 'Error in pipeline',
            'error': str(e)
            }

def run_scraping(input):
    # Check if file exists, if so skip scrapping
    if _check_if_file_exists(input['file_name'], input['date']):
        return {
            'message': 'File already exists, skipping scrapping',
            'file_name': f'data/{input["date"]}/{input["file_name"]}.csv'
            }
    
    # Initialize the webdriver
    config = Driver()
    driver = config.start_driver()
    
    scraper = Scraper(driver, input['date'])

    report = scraper.start(input['url'], input['pages'], input['file_name'], input['operation'])

    return report

def run_preprocessing(file_name, date):
    # Check if file exists, if so skip preprocessing
    file_check = f'{file_name}_preprocessed'
    if _check_if_file_exists(file_check, date):
        return {
            'message': 'File already exists, skipping preprocessing',
            'file_path': f'data/{date}/{file_check}.csv'
            }
    
    preprocessor = Preprocessor()

    # Preprocess data
    file_path = f'data/{date}/{file_name}.csv'
    saved_file_name = preprocessor.preprocess_data(file_path)

    return {
        'message': 'Preprocessing finished',
        'file_path': f'data/{date}/{saved_file_name}'
        }

def fetch_lat_lng(file_name, date):
    # Check if file exists, if so skip fetching
    file_check = f'{file_name}_preprocessed_with_lat_lng'
    if _check_if_file_exists(file_check, date):
        return {
            'message': 'File already exists, skipping fetching lat, lng',
            'file_path': f'data/{date}/{file_check}.csv'
            }

    preprocessor = Preprocessor()

    # Fetch lat, lng
    file_path = f'data/{date}/{file_name}_preprocessed.csv'
    saved_file_name = preprocessor.get_lat_lng(file_path)

    return {
        'message': 'Fetching lat, lng finished',
        'file_path': f'data/{date}/{saved_file_name}'
        }

def load_data(file_name, date):
    # Check which file to load
    file_preprocessed = f'{file_name}_preprocessed'
    file_with_lat_lng = f'{file_name}_preprocessed_with_lat_lng'

    # First try to load file with lat, lng
    if _check_if_file_exists(file_with_lat_lng, date):
        file_name = file_with_lat_lng

    # If not, try to load file preprocessed
    elif _check_if_file_exists(file_preprocessed, date):
        file_name = file_preprocessed

    # If not, return error
    else:
        return {
            'message': 'No file to load',
            'file_path': None
            }

    loader = Loader()
    file_path = f'data/{date}/{file_name}.csv'
    result = loader.load_data(file_path)

    if result:
        return {
            'message': 'Data loaded successfully',
            }
    else:
        return {
            'message': 'Data not loaded',
            }


def _check_if_file_exists(file_name, date):
    file_path = f'data/{date}/{file_name}.csv'
    if os.path.exists(file_path):
        return True
    else:
        return False


