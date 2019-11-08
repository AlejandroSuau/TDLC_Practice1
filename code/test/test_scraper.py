# -*- coding: utf-8 -*-

import unittest

from classes.holidays_calendar_scraper import HolidaysCalendarScraper
from classes.holiday_row import HolidayType

class TestHolidaysCalendarScraper(unittest.TestCase):
    
    def setUp(self):
        self.url_alava_2019 = 'https://www.calendarioslaborales.com/calendario-laboral-alava-2019.htm'
        self.url_alava_2006 = 'https://www.calendarioslaborales.com/calendario-laboral-alava-2006.htm'
        
        chrome_driver_path = '/Users/Suau/Desktop/ChromeDriver/chromedriver.exe'
        self.starting_url = 'https://www.calendarioslaborales.com/'
        self.scraper = HolidaysCalendarScraper(chrome_driver_path, self.starting_url)
    
    def test_scrap_provinces_a_elements(self):
        self.scraper.navigate_to_url(self.starting_url)
        
        provinces_len = len(self.scraper.scrap_provinces_a_elements())
        self.assertEqual(provinces_len, 61)
    
    def test_scrap_previous_year(self):
        self.scraper.navigate_to_url(self.url_alava_2019)
        
        (previous_year, url) = self.scraper.scrap_previous_year()
        self.assertEqual(previous_year, 2018)
        self.assertEqual(url, "https://www.calendarioslaborales.com/calendario-laboral-alava-2018.htm")
    
    def test_add_all_calendar_holidays_to_scraped_data(self):
        self.scraper.navigate_to_url(self.url_alava_2019)
        
        self.scraper.set_current_scraping_year(2019)
        
        self.scraper.add_all_calendar_holidays_to_scraped_data()
        
        holidays_len = len(self.scraper.get_scraped_data())
        self.assertEqual(holidays_len, 14)
    
    def test_scrap_month_divs_methods(self):
        self.scraper.navigate_to_url(self.url_alava_2019)

        self.scraper.set_current_scraping_province('Álava')
        self.scraper.set_current_scraping_year(2019)
        
        month_divs = self.scraper.scrap_month_divs()
        self.assertEqual(len(month_divs), 12)
        
        april_div = month_divs[4]
        days_info = self.scraper.scrap_all_holidays_info_from_div(
                april_div)
        self.assertEqual(len(days_info), 4)
    
    def test_create_HolidayRow_from_info(self):
        self.scraper.navigate_to_url(self.url_alava_2019)
        
        self.scraper.set_current_scraping_province('Álava')
        self.scraper.set_current_scraping_year(2019)
        self.scraper.set_current_scraping_month(4)

        holiday_info = (29, 28, 'San Prudencio', HolidayType.LOCAL)
        holiday_row = self.scraper.create_HolidayRow_from_info(holiday_info)
        self.assertEqual(str(holiday_row), '"San Prudencio",29-04-2019,"Álava",Local,28-04-2019')
        
    def test_scrap_previous_year_none(self):
        self.scraper.navigate_to_url(self.url_alava_2006)

        (previous_year, url) = self.scraper.scrap_previous_year()
        self.assertIsNone(previous_year)
        self.assertIsNone(url)
      
    def tearDown(self):
        self.scraper.end_scraping()