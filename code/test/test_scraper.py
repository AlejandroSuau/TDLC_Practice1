# -*- coding: utf-8 -*-

import unittest

from classes.holidays_calendar_scraper import HolidaysCalendarScraper
from classes.holiday_row import HolidayType
from classes.holidays_calendar_constants import Constants

class TestHolidaysCalendarScraper(unittest.TestCase):
    
    def setUp(self):        
        chrome_driver_path = '/Users/Suau/Desktop/ChromeDriver/chromedriver.exe'
        self.scraper = HolidaysCalendarScraper(chrome_driver_path)
    
    def test_scrap_provinces_a_elements(self):
        self.scraper.navigate_to_url(self.scraper.get_starting_url())
        
        provinces_len = len(self.scraper.scrap_provinces_a_elements())
        self.assertEqual(provinces_len, 61)
    
    def test_scrap_previous_year(self):
        self.scraper.navigate_to_url(self.scraper.get_starting_url())
        
        (previous_year, url) = self.scraper.scrap_previous_year()
        self.assertEqual(previous_year, 2018)
        self.assertEqual(url, "https://www.calendarioslaborales.com/calendario-laboral-alava-2018.htm")
    
    def test_add_all_calendar_holidays_to_scraped_data(self):
        self.scraper.navigate_to_url(self.scraper.get_starting_url())
                
        self.scraper.add_all_calendar_holidays_to_scraped_data()
        
        holidays_len = len(self.scraper.get_scraped_data())
        self.assertEqual(holidays_len, 14)
    
    def test_scrap_month_divs_methods(self):
        self.scraper.navigate_to_url(self.scraper.get_starting_url())
        
        month_divs = self.scraper.scrap_month_divs()
        self.assertEqual(len(month_divs), 12)

        self.scraper.add_all_holidays_from_div_to_scraped_data(month_divs[3])
        self.assertEqual(len(self.scraper.get_scraped_data()), 4)        
    
    def test_create_HolidayRow_from_info(self):
        self.scraper.navigate_to_url(self.scraper.get_starting_url())

        holiday_info = (29, 28, 'San Prudencio', HolidayType.LOCAL)
        holiday_row = self.scraper.create_HolidayRow_from_info(holiday_info)
        self.assertEqual(str(holiday_row), '"San Prudencio",29-04-2019,"Álava",Local,28-04-2019')
        
    def test_scrap_previous_year_none(self):
        self.scraper.navigate_to_url('https://www.calendarioslaborales.com/calendario-laboral-alava-2006.htm')

        (previous_year, url) = self.scraper.scrap_previous_year()
        self.assertIsNone(previous_year)
        self.assertIsNone(url)
     
    def tearDown(self):
        self.scraper.end_scraping()