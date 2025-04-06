from selenium.webdriver.common.by import By
import time

class Navigator:
    def __init__(self, driver):
        self.driver = driver
        self.scroll_delay = 8
        self.scroll_already_refreshed = False
    
    def scroll_down(self):
        print("Scrolling down...")
        try:
            scrolls = 5
            for _ in range(scrolls):
                try:
                    # First try to get the bottom navbar
                    navbar = self.driver.find_elements(By.CSS_SELECTOR, 'nav[data-testid="l-pagination"].l-pagination')
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", navbar[0])
                except:
                    try:
                        # Then try to the end of the cards div
                        cards_ending = self.driver.find_elements(By.CSS_SELECTOR, 'div.listings-wrapper')
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", cards_ending[0])
                    except:
                        try:
                            # Finally, try recommendations at the bottom
                            page_bottom = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="recommendations-list"]')
                            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", page_bottom[0])
                        except:
                            # Otherside trigger exception
                            raise Exception("No scrollable element found")
                
                time.sleep(self.scroll_delay)
            self.scroll_already_refreshed = False
            return True
        except:
            if not self.scroll_already_refreshed:
                print("Error scrolling down.\nRefreshing page..")
                self._refresh_page()
                self.scroll_down()
            else:
                print("Error scrolling down.\nSkipping page..")
                self.scroll_already_refreshed = False
                return False

    def _refresh_page(self):
        self.scroll_already_refreshed = True
        self.driver.refresh()
        time.sleep(10)

    def next_page(self):
        """ Find and click the next page button with retry logic """
        pagination_button = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="next-page"]')
        if not pagination_button:
            print("No next page button found")
            # Try next page through URL
            return self._url_next_page()

        # Try to click next page
        click_result = self._click_next_page(pagination_button)

        if click_result:
            return True
        else:
            return self._url_next_page()

    def _click_next_page(self, pagination_button):
        try:
            # Method 1: Regular click
            pagination_button[0].click()
        except:
            try:
                # Method 2: JavaScript click
                self.driver.execute_script("arguments[0].click();", pagination_button[0])
            except:
                try:
                    # Method 3: Scroll into view and click
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", pagination_button[0])
                    time.sleep(1)  # Give it a moment to scroll
                    pagination_button[0].click()
                except:
                    print("Failed to click next page")
                    return False
        return True
        
    def _url_next_page(self):
        try:
            # Get current URL
            current_url = self.driver.current_url
            print(f"Current URL: {current_url}")

            if 'pagina=' in current_url:
                # Extract current page number and increment it
                current_page = int(current_url.split('pagina=')[1])
                new_url = current_url.replace(f'pagina={current_page}', f'pagina={current_page + 1}')
            else:
                # Add page parameter if it doesn't exist
                new_url = f'{current_url}&pagina={current_page + 1}'
            
            print(f"Attempting to move to this URL: {new_url}")
            self.driver.get(new_url)
            time.sleep(10)
            return True
        except Exception as e:
            print(f"URL fallback failed: {e}")
            return False
