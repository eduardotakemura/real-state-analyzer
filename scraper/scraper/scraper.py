from scraper.navigator import Navigator
from scraper.extractor import Extractor
import pandas as pd
import time
import os

class Scraper:
    def __init__(self, driver, script_date):
        self.script_date = script_date
        self.driver = driver
        self.scrapped_entries = 0
        self.errors = 0
        self.new_page_delay = 10
        self.ref_cols = [
            'id', 'link', 'title', 'operation', 'address', 'size',
            'dorms', 'toilets', 'garage', 'price', 'additional_costs', 'scraping_date'
        ]

    def start(self, url, pages, file_name, operation):
        """ Main scrapping method.\n
            Save the output file in data folder, return nothing.\n
            URL: URL address to scrap.\n
            pages: number of pages to process.\n
            file_name: provide a name to the output file.\n
            operation: provide a name to the current operation, such as Selling or Renting,
            which will fill the 'operation' feature in the output file."""

        # Initialize extractor
        extractor = Extractor(self.driver)
        navigator = Navigator(self.driver)

        # Used to track the processing time #
        start_time = time.time()

        # Access url #
        self.driver.get(url)
        
        # Initialize file 
        full_file_name = self._initialize_file(file_name)

        # Scrap each page at once, saving it at the end of each iteration #
        for page in range(1, pages + 1):
            print(f'Scraping page {page} of {pages}')
            

            # Page load time
            time.sleep(self.new_page_delay) 

            # Scroll to bottom loop
            scroll_result = navigator.scroll_down()

            # Run Scrap
            if scroll_result:
                data, scrapped_entries, errors = extractor.scrape_page(operation)
                self.scrapped_entries += scrapped_entries
                self.errors += errors
                print(f'Scraped {len(data)} entries from this page')
                self._save_data(full_file_name, data)

            # Move to next page
            if not navigator.next_page():
                break
            print("Moving to next page")

        # Close driver
        self.driver.quit()

        # Get summary   
        report = self._get_summary(start_time, full_file_name)

        # Reset counters
        self.scrapped_entries = 0
        self.errors = 0
        return report
        
    ## ------------------ FILE MANAGEMENT FUNCTIONS ------------------ ##
    def _initialize_file(self, file_name):
        """ Initialize the output CSV file in the /data \n
            Return full path to the file. """

        base_dir = './data'
        data_dir = os.path.join(base_dir, self.script_date)
        os.makedirs(data_dir, exist_ok=True)

        full_file_name = os.path.join(data_dir, f'{file_name}.csv')

        df = pd.DataFrame(columns=self.ref_cols)
        df.to_csv(full_file_name, index=False)
        print(f'File initialized at {full_file_name}')
        return full_file_name
   
    def _get_summary(self, start_time, file_name):
        total_time = round((time.time() - start_time) / 60, 2)
        report = {
            'file_name': file_name,
            'entries_scraped': self.scrapped_entries,
            'errors': self.errors,
            'total_time': total_time
        }
        print(f'Scraping Finished.\n'
        f'Entries Scraped: {self.scrapped_entries}\n'
        f'Errors: {self.errors}\n'
        f'File saved at {file_name}\n'
        f'Total time: {total_time} minutes'
        )
        return report

    def _save_data(self, file_name, data):
        # Initialize data as df #
        new_data_df = pd.DataFrame(data)

        # Append scraping date
        new_data_df['scraping_date'] = self.script_date

        # Open existent file #
        existing_df = pd.read_csv(file_name)

        # Append new data to existent one #
        updated_df = pd.concat([existing_df, new_data_df], ignore_index=True)

        # Overwrite existent file #
        updated_df.to_csv(file_name, index=False)



