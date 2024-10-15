import os
from datetime import datetime
from etl.scrapper import Scrapper
from etl.preprocessor import Preprocessor
from etl.loader import Loader

SCRAPPER_PAGES = [
    {
        'url':'https://www.vivareal.com.br/venda/sp/sao-paulo/#onde=,S%C3%A3o%20Paulo,S%C3%A3o%20Paulo,,,,,city,BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo,,,',
        'pages': 3,
        'file_name':'sell',
        'operation':'selling'
    },
    {
        'url':'https://www.vivareal.com.br/aluguel/sp/sao-paulo/#onde=Brasil,S%C3%A3o%20Paulo,S%C3%A3o%20Paulo,,,,,,BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo,,,',
        'pages': 3,
        'file_name': 'rent',
        'operation': 'renting'
    }
]

def run_etl():
    # Initializing script ref date #
    script_date = datetime.now().strftime("%d-%m-%Y")

    # Extract (Scrapping) #
    script_scrap(SCRAPPER_PAGES, script_date)
    print('Scrapping concluded')

    # Transform (Preprocessing) #
    script_preprocess(script_date)
    print('Preprocessing concluded')

    # Load (Load to DB) #
    script_loader(script_date)

def script_scrap(pages, script_date):
    scrapper = Scrapper(script_date)
    for page in pages:
        scrapper.start(
            url=page['url'],
            pages=page['pages'],
            file_name=page['file_name'],
            operation=page['operation']
        )

def script_preprocess(script_date):
    # Initialize storage folder #
    output_dir = os.path.join('..', 'data', 'processed', script_date)
    os.makedirs(output_dir, exist_ok=True)

    # Read all scrapped files #
    files, input_path = _get_files(script_date, 'scrapped')

    # Preprocess each file #
    preprocessor = Preprocessor(output_dir)
    for file in files:
        file_path = os.path.join(input_path, file)
        if preprocessor.clean_scrapped_data(file_path):
            print(f'Preprocessing completed with success for: {file_path}')

def script_loader(script_date):
    loader = Loader(script_date)
    loader.load_to_db()

def _get_files(script_date, folder):
    # Get path to the current folder #
    base_dir = os.path.join('..', 'data', folder)
    dir_path = os.path.join(base_dir, script_date)

    # List all files #
    files = [file for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file))]
    return files, dir_path

if __name__ == '__main__':
    run_etl()
