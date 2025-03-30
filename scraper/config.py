#import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

class Driver:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        self.chrome_options.add_argument("accept-language=en-US,en;q=0.9")
        self.chrome_options.add_argument("referer=https://www.google.com/")
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--window-size=1920,1080')
        self.chrome_options.add_argument('--disable-browser-side-navigation')
        self.chrome_options.add_argument('--disable-infobars')
        self.chrome_options.add_argument('--disable-setuid-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        #self.chrome_options.add_argument('--headless=new')
        self.service = Service('/usr/local/bin/chromedriver/chromedriver-linux64/chromedriver')
    
    def start_driver(self):
        driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        #driver = uc.Chrome(options=self.chrome_options)
        return driver
