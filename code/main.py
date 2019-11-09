# -*- coding: utf-8 -*-

from classes.holidays_calendar_scraper import HolidaysCalendarScraper

chrome_driver_path = '/Users/Suau/Desktop/ChromeDriver/chromedriver.exe'
scraper = HolidaysCalendarScraper(chrome_driver_path)

scraper.start_scraping()

scraped_data = scraper.get_scraped_data()

scraper.create_csv_with_scraped_data()

print("Urls ejecutadas: {} \n".format(scraper.num_executed_urls))
print("Tiempo total esperado: {}\n".format(scraper.waited_seconds))
print(*scraped_data, sep="\n")

scraper.end_scraping()
