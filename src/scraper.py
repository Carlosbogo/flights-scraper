import logging
from dataclasses import dataclass
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ChromeFlightScraper:
    """Scraper class for Google Flights on Chrome"""
    def __init__(self):
        self.driver: webdriver.Chrome = webdriver.Chrome()
        self._origin: str = None
        self._destination: str = None
        self._departure_date: str = None
        self._return_date: str = None
        self._one_way: bool = False
        self.logger: logging.Logger = logging.getLogger(__name__)       
    
    @property
    def departure_date(self) -> str:
        return self._departure_date
    
    @property
    @departure_date.setter
    def departure_date(self, departure_date: str) -> None:
        if self.return_date:
            if departure_date > self.return_date:
                raise ValueError("Departure date cannot be after return date.")
            if departure_date < datetime.now().strftime("%Y-%m-%d"):
                raise ValueError("Departure date cannot be in the past.")
        self._departure_date = departure_date

    @property
    def return_date(self) -> str:
        return self._return_date
    
    @property
    @return_date.setter
    def return_date(self, return_date: str) -> None:
        if self.departure_date:
            if return_date < self.departure_date:
                raise ValueError("Return date cannot be before departure date.")
            if return_date < datetime.now().strftime("%Y-%m-%d"):
                raise ValueError("Return date cannot be in the past.")
        self._return_date = return_date
    

    def __str__(self) -> str:
        return f"""
        Flight Scraper:
        \tOrigin: {self.config.origin}
        \tDestination: {self.config.destination}
        \tDeparture Date: {self.config.departure_date}
        \tReturn Date: {self.config.return_date}
        \tOne Way: {self.config.one_way}
        """
    
    def __repr__(self) -> str:
        return "FlightScraper({self.driver}, \
            {self.origin}, \
            {self.destination}, \
            {self.departure_date}, \
            {self.return_date}, \
            {self.one_way})"

    def handle_google_privacy_popup(self) -> None:
        deny_cookies_button = self.driver.find_element(
            By.XPATH, '//span[contains(text(), "Reject all")]'
        )
        WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable(deny_cookies_button)
        ).click()
        self.logger.info("Google Privacy Popup rejected.")
        
repr(ChromeFlightScraper())