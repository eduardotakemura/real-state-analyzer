from selenium.webdriver.common.by import By
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
        self.scroll_delay = 8
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
            self._scroll_down()

            # Run Scrap
            data = self._scrape_page(operation)
            print(f'Scraped {len(data)} entries from this page')
            self._save_data(full_file_name, data)

            # Move to next page
            if not self._go_to_next_page():
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

    def _scrape_page(self, operation):
        """ Get all cards from the page,
         then extract individually data from each.\n
         Return all cards details. """

        search = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-cy="rp-property-cd"]')
        print(f'Cards found: {len(search)}.\nStarting page scrapping...')
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

    def _scroll_down(self):
        print("Scrolling down...")
        try:
            for i in range(5):
                navbar = self.driver.find_elements(By.CSS_SELECTOR, 'nav[data-testid="l-pagination"].l-pagination')
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", navbar[0])
                time.sleep(self.scroll_delay)
        except:
            print("Error scrolling down.\nMove on...")

    def _extract_card_data(self, card, operation):
        link = self._extract_link(card)
        real_state_id = self._extract_id(card)
        title = self._extract_title(card)
        address = self._extract_address(card)
        price = self._extract_price(card)
        additional_costs = self._extract_costs(card)
        details = self._extract_details(card)
  
        return {
            'id': real_state_id,
            'link': link,
            'title': title,
            'operation': operation,
            'address': address,
            'size': details['size'],
            'dorms': details['dorms'],
            'toilets': details['toilets'],
            'garage': details['garage'],
            'price': price,
            'additional_costs': additional_costs,
        } 

    def _extract_link(self, card):
        try:
            return card.find_element(By.CSS_SELECTOR, 'a[itemprop="url"]').get_attribute('href')
        except:
            return ''

    def _extract_id(self, card):
        try:
            return card.find_element(By.CSS_SELECTOR, 'a[itemprop="url"]').get_attribute('data-id')
        except:
            return ''

    def _extract_title(self, card):
        try:
            return card.find_element(By.CSS_SELECTOR, '.card__location h2 span:first-of-type').text
        except:
            return ''

    def _extract_address(self, card):
        neighborhood = card.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-location-txt"]').text
        street = card.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-street-txt"]').text
        address =  f"{street} - {neighborhood}"
        return address

    def _extract_price(self, card):
        return card.find_element(By.CSS_SELECTOR, 'div[data-cy="rp-cardProperty-price-txt"] > p.l-text--variant-heading-small').text

    def _extract_costs(self, card):
        try:
            return card.find_element(By.CSS_SELECTOR, 'div[data-cy="rp-cardProperty-price-txt"] > p.l-text--variant-body-small').text
        except:
            return ''

    def _extract_details(self, card):
        def _get_element_text(selector):
            try:
                return card.find_element(By.CSS_SELECTOR, selector).text
            except:
                return ''

        size = _get_element_text('[data-cy="rp-cardProperty-propertyArea-txt"]')
        dorms = _get_element_text('[data-cy="rp-cardProperty-bedroomQuantity-txt"]')
        toilets = _get_element_text('[data-cy="rp-cardProperty-bathroomQuantity-txt"]')
        garage = _get_element_text('[data-cy="rp-cardProperty-parkingSpacesQuantity-txt"]')

        return {
            "size":size,
            "dorms":dorms,
            "toilets":toilets,
            "garage":garage
        }

    def _go_to_next_page(self):
        """ Find and click the next page button with retry logic """
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                pagination_button = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="next-page"]')
                if not pagination_button:
                    print("No next page button found")
                    return False
                
                # Try different clicking methods
                try:
                    # Method 1: Regular click
                    pagination_button[0].click()
                except:
                    try:
                        # Method 2: JavaScript click
                        self.driver.execute_script("arguments[0].click();", pagination_button[0])
                    except:
                        # Method 3: Scroll into view and click
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", pagination_button[0])
                        time.sleep(1)  # Give it a moment to scroll
                        pagination_button[0].click()
                
                return True

            except Exception as e:
                time.sleep(2)  # Wait before retry
                
        print("Failed to navigate to next page after all attempts")
        return False


