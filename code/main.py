# -*- coding: utf-8 -*-

from classes.holidays_calendar_scraper import HolidaysCalendarScraper

chrome_driver_path = '/Users/Suau/Desktop/ChromeDriver/chromedriver.exe'
scraper = HolidaysCalendarScraper(chrome_driver_path)

scraper.start_scraping()
scraper.get_scraped_data()
scraper.end_scraping()

csv_filename = "data"
scraper.create_csv_with_scraped_data(csv_filename)

scraper.print_scraping_info()
