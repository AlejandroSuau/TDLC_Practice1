# -*- coding: utf-8 -*-

import unittest

from classes.holidays_calendar_scraper import HolidaysCalendarScraper

class TestHolidaysCalendarScraper(unittest.TestCase):
    
    def setUp(self):
        chrome_driver_path = '/Users/Suau/Desktop/ChromeDriver/chromedriver.exe'
        starting_url = 'https://www.calendarioslaborales.com/'
        self.holidays_calendar_scraper = HolidaysCalendarScraper(chrome_driver_path, starting_url)
    
    def test_previous_year(self):
        current_url = "https://www.calendarioslaborales.com/calendario-laboral-alava-2019.htm"
        self.holidays_calendar_scraper.get_browser().get(current_url)
        expected_previous_year = 2018
        expected_url = "https://www.calendarioslaborales.com/calendario-laboral-alava-2018.htm"
        (previous_year, url) = self.holidays_calendar_scraper.scrap_previous_year()
        self.assertEqual(expected_previous_year, previous_year)
        self.assertEqual(expected_url, url)
    
    def test_none_previous_year(self):
        current_url = "https://www.calendarioslaborales.com/calendario-laboral-alava-2006.htm"
        self.holidays_calendar_scraper.get_browser().get(current_url)
        (previous_year, url) = self.holidays_calendar_scraper.scrap_previous_year()
        self.assertIsNone(previous_year)
        self.assertIsNone(url)
        
    def tearDown(self):
        self.holidays_calendar_scraper.end_scraping()
    
if __name__ == '__main__':
    unittest.main()