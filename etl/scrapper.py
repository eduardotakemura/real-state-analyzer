from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import re
import time
import os

class Scrapper:
    def __init__(self, script_date):
        self.config = Options()
        # self.chrome_options.add_argument("--headless")
        # self.chrome_options.add_argument("--disable-gpu")
        # self.chrome_options.add_argument("--no-sandbox")
        # self.chrome_options.add_argument("--disable-dev-shm-usage")
        # self.chrome_options.add_argument("--window-size=1920x1080")
        # self.service = Service(r"path-to-driver")
        self.service = ''
        self.page_delay = 5
        self.script_date = script_date
        self.driver = None
        self.scrapped_entries = 0
        self.errors = 0

    def start(self, url, pages, file_name, operation):
        """ Main scrapping method.\n
            Save the output file in data/scrapped, return nothing.\n
            URL: URL address to scrap.\n
            pages: number of pages to process.\n
            file_name: provide a name to the output file.\n
            operation: provide a name to the current operation, such as Selling or Renting,
            which will fill the 'operation' feature in the output file."""

        # Used to track the processing time #
        start_time = time.time()

        # Initialize driver and access url #
        self._initialize_driver()
        self.driver.get(url)
        full_file_name = self._initialize_file(file_name)

        # Scrap each page at once, saving it at the end of each iteration #
        for page in range(1, pages + 1):
            print(f'Scrapping page {page} of {pages}')
            time.sleep(self.page_delay)
            data = self._scrape_page(operation)
            self._save_data(full_file_name, data)

            if not self._go_to_next_page():
                break

        self.driver.quit()
        self._print_summary(start_time, full_file_name)
        self.scrapped_entries = 0
        self.errors = 0

    def _initialize_driver(self):
        """ Retrieve driver configs """
        self.driver = webdriver.Chrome(options=self.config, service=self.service)

    def _initialize_file(self, file_name):
        """ Initialize the output CSV file in the /data/scrapped/<current_date> directory. \n
            Return full path to the file. """

        # Get the absolute path to the directory where the file will be saved
        base_dir = './../data/scrapped'
        data_dir = os.path.join(base_dir, self.script_date)
        os.makedirs(data_dir, exist_ok=True)
        full_file_name = os.path.join(data_dir, f'{file_name}.csv')

        # Initialize empty file #
        df = pd.DataFrame(columns=[
            'id', 'link', 'title', 'operation', 'address', 'size',
            'dorms', 'toilets', 'garage', 'price', 'additional_costs', 'features'
        ])
        df.to_csv(full_file_name, index=False)
        return full_file_name

    def _scrape_page(self, operation):
        """ Get all cards from the page,
         then extract individually data from each.\n
         Return all cards details. """

        search = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-type="property"]')
        all_cards = []

        for card in search:
            try:
                card_data = self._extract_card_data(card, operation)
                all_cards.append(card_data)
                self.scrapped_entries += 1
            except Exception as e:
                print(f"Error extracting data from a card: {e}")
                self.errors += 1

        return all_cards

    def _extract_card_data(self, card, operation):
        link = card.find_element(By.CLASS_NAME, 'property-card__content-link').get_attribute('href')
        real_state_id = self._extract_id_from_link(link)
        title = card.find_element(By.CLASS_NAME, 'property-card__title').text
        address = card.find_element(By.CLASS_NAME, 'property-card__address').text
        details = self._extract_card_details(card)
        features = self._extract_card_features(card)
        price, additional_costs = self._extract_prices(card)

        return {
            'id': real_state_id,
            'link': link,
            'title': title,
            'operation': operation,
            'address': address,
            'size': details.get('size', ''),
            'dorms': details.get('dorms', ''),
            'toilets': details.get('toilets', ''),
            'garage': details.get('garage', ''),
            'price': price,
            'additional_costs': additional_costs,
            'features': features
        }

    def _extract_id_from_link(self, link):
        match = re.search(r"-(\d+)/$", link)
        return match.group(1) if match else ''

    def _extract_card_details(self, card):
        details = card.find_elements(By.CSS_SELECTOR, "li.property-card__detail-item")
        return {
            'size': details[0].find_element(By.CSS_SELECTOR, "span.property-card__detail-value").text if len(
                details) > 0 else '',
            'dorms': details[1].find_element(By.CSS_SELECTOR, "span.property-card__detail-value").text if len(
                details) > 1 else '',
            'toilets': details[2].find_element(By.CSS_SELECTOR, "span.property-card__detail-value").text if len(
                details) > 2 else '',
            'garage': details[3].find_element(By.CSS_SELECTOR, "span.property-card__detail-value").text if len(
                details) > 3 else ''
        }

    def _extract_card_features(self, card):
        features = card.find_elements(By.CSS_SELECTOR, "li.amenities__item")
        return ', '.join([feature.text for feature in features]) if features else 'None'

    def _extract_prices(self, card):
        price_text = card.find_element(By.CLASS_NAME, 'property-card__price').text
        price = self._clean_price(price_text)
        additional_costs = self._extract_additional_costs(card)
        return price, additional_costs

    def _clean_price(self, price_text):
        cleaned_price = price_text.replace("R$", "").strip().replace(".", "")
        match = re.search(r"\d+\.\d+", cleaned_price)
        return match.group(0) if match else cleaned_price

    def _extract_additional_costs(self, card):
        try:
            additional_costs_text = card.find_element(By.CLASS_NAME, 'js-condo-price').text
            return self._clean_price(additional_costs_text)
        except:
            return 0

    def _save_data(self, file_name, data):
        # Initialize data as df #
        new_data_df = pd.DataFrame(data)

        # Open existent file #
        existing_df = pd.read_csv(file_name)

        # Append new data to existent one #
        updated_df = pd.concat([existing_df, new_data_df], ignore_index=True)

        # Overwrite existent file #
        updated_df.to_csv(file_name, index=False)

    def _go_to_next_page(self):
        """ Find and click the next page button """

        try:
            pagination_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.pagination__item button[title="Próxima página"]'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", pagination_button)
            pagination_button.click()
            return True

        except Exception as e:
            print(f"Error navigating to the next page: {e}")
            return False

    def _print_summary(self, start_time, file_name):
        total_time = round((time.time() - start_time) / 60, 2)
        print(f'Scraping Finished.\n'
              f'Entries Scraped: {self.scrapped_entries}\n'
              f'Errors: {self.errors}\n'
              f'File saved at {file_name}\n'
              f'Total time: {total_time} minutes')