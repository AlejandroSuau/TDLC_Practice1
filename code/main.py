# -*- coding: utf-8 -*-

from classes.holidays_calendar_scraper import HolidaysCalendarScraper

chrome_driver_path = '/Users/Suau/Desktop/ChromeDriver/chromedriver.exe'
starting_url = 'https://www.calendarioslaborales.com/'
scraper = HolidaysCalendarScraper(chrome_driver_path, starting_url)

scraper.start_scraping()
scraped_data = scraper.get_scraped_data()
scraper.end_scraping()

print(*scraped_data, sep="\n\n")