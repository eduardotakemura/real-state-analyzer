from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

class Extractor:
    def __init__(self, driver):
        self.driver = driver

    def scrape_page(self, operation):
        """ Get all cards from the page,
         then extract individually data from each.\n
         Return all cards details. """

        scrapped_entries = 0
        errors = 0
        retries = 3
        
        for _ in range(retries):
            # Get page source and create BeautifulSoup object
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Find all property cards
            search = soup.select('div[data-cy="rp-property-cd"]')

            if len(search) > 0:
                break
            else:
                time.sleep(1)

        print(f'Cards found: {len(search)}.\nStarting page scrapping...')
        all_cards = []

        for card in search:
            try:
                card_retries = 3
                for _ in range(card_retries):
                    card_data = self._extract_card_data(card, operation)
                    #print(f"Card data: {card_data}")

                    if self._check_if_empty(card_data):
                        time.sleep(1)
                    break
                
                all_cards.append(card_data)
                scrapped_entries += 1
            except Exception as e:
                print(f"Error extracting data from a card: {e}")
                errors += 1

        return all_cards, scrapped_entries, errors
    
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

    def _check_if_empty(self, card):
        if card['id'] == '' or card['link'] == '' or card['title'] == '' or card['address'] == '' or card['price'] == '' or card['additional_costs'] == '':
            return True
        else:
            return False

    def _extract_link(self, card):
        try:
            link_element = card.select_one('div > a[itemprop="url"]')
            return link_element['href'] if link_element else ''
        except:
            return ''

    def _extract_id(self, card):
        try:
            id_element = card.select_one('div > a[itemprop="url"]')
            return id_element['data-id'] if id_element else ''
        except:
            return ''

    def _extract_title(self, card):
        try:
            section = card.select_one('[itemprop="address"]')
            spans = section.select('span')
            return spans[0].text if spans else ''
        except:
            return ''

    def _extract_address(self, card):
        try:
            neighborhood = card.select_one('span[data-cy="rp-cardProperty-location-txt"]')
            neighborhood = neighborhood.text if neighborhood else ''
        except:
            neighborhood = ''
        
        try:
            street = card.select_one('p[data-cy="rp-cardProperty-street-txt"]')
            street = street.text if street else ''
        except:
            street = ''
        
        address = f"{street} - {neighborhood}"
        return address

    def _extract_price(self, card):
        try:
            price_element = card.select_one('div[data-cy="rp-cardProperty-price-txt"] > p:first-of-type')
            return price_element.text if price_element else ''
        except:
            return ''

    def _extract_costs(self, card):
        try:
            costs_element = card.select_one('div[data-cy="rp-cardProperty-price-txt"] > p:last-of-type')
            return costs_element.text if costs_element else ''
        except:
            return ''

    def _extract_details(self, card):
        def _get_element_text(selector):
            try:
                element = card.select_one(selector)
                return element.text if element else ''
            except:
                return ''

        size = _get_element_text('[data-cy="rp-cardProperty-propertyArea-txt"]')
        dorms = _get_element_text('[data-cy="rp-cardProperty-bedroomQuantity-txt"]')
        toilets = _get_element_text('[data-cy="rp-cardProperty-bathroomQuantity-txt"]')
        garage = _get_element_text('[data-cy="rp-cardProperty-parkingSpacesQuantity-txt"]')

        return {
            "size": size,
            "dorms": dorms,
            "toilets": toilets,
            "garage": garage
        }
