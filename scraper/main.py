from config import Driver
from scraper import Scraper
from datetime import datetime

def main():
    # Initialize the webdriver
    config = Driver()
    driver = config.start_driver()
    
    script_date = datetime.now().strftime('%Y-%m-%d')
    scraper = Scraper(driver, script_date)
    url = 'https://www.vivareal.com.br/aluguel/sp/sao-paulo/#onde=Brasil,S%C3%A3o%20Paulo,S%C3%A3o%20Paulo,,,,,,BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo,,,'
    pages = 10
    file_name = 'rent'
    operation = 'renting'
    scraper.start(url, pages, file_name, operation)
    
  
if __name__ == '__main__':
    main()
