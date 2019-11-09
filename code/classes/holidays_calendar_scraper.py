# -*- coding: utf-8 -*-
import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
from numpy import random

from classes.holiday_row import HolidayRow
from classes.holidays_calendar_constants import Constants

class HolidaysCalendarScraper:
    """
    
        HolidaysCalendarScraper is a class which allows to obtain all the 
        holidays of every province of every year (from 2006-2019 inclusive). 
    
        Args:
            chrome_driver_path (string): chromes driver path.
        
        Attributes:
            chrome_driver_path (string): chromes driver path.
            starting_url (string): the url where the browser will start to scrap.
            browser (webdriver.Chrome): the current browser.
            current_scraping_province (string): the province which is currently scraping.
            current_scraping_year (int): the year which is currently scraping.
            current_scraping_month (int): the month which is currently scraping.
            time_sleep_delays (array[int]): sleep seconds between page navigation.
            num_executed_urls (int): number of executed urls.
            scraped_data (array): the list of strings parsed from HolidayRow 
                objects with its __str__ method.
                
    """
    
    def __init__(self, chrome_driver_path):
        self.chrome_driver_path = chrome_driver_path
        self.starting_url = 'https://www.calendarioslaborales.com/calendario-laboral-alava-2019.htm'
        
        self.browser = webdriver.Chrome(self.chrome_driver_path)
        
        self.starting_year = 2019
        self.current_scraping_province = 'Álava'
        self.current_scraping_year = self.starting_year
        self.current_scraping_month = 1
        
        self.time_sleep_delays = [7, 4, 6, 2, 10, 19]
        self.num_executed_urls = 0
        self.waited_seconds = 0
        self.execution_time = 0
        
        self.csv_header = ['Name', 'Date', 'Province', 'Type', 'Moved Date From']
        self.scraped_data = []
    
    def start_scraping(self):
        """
        
        Starts the scraping process. It scrapes all the holidays of every year 
        of every province.
        
        """
        self.execution_time = time.time()
        
        self.browser.get(self.starting_url)
        self.num_executed_urls += 1
        
        i = 0
        provinces = self.scrap_provinces_a_elements()
        while (i < len(provinces)):
            self.current_scraping_year = self.starting_year
            self.current_scraping_province, next_url = self.scrap_text_and_href_from_link(provinces[i])
            
            while (next_url is not None):
                self.make_random_sleep()
                self.browser.get(next_url)
                
                self.add_all_calendar_holidays_to_scraped_data()
                
                self.current_scraping_year, next_url = self.scrap_previous_year()
                self.num_executed_urls += 1
            
            provinces = self.scrap_provinces_a_elements()
            i += 1
 
    def scrap_provinces_a_elements(self):
        """
        
        It scrapes the provinces a elements from the Main Page (starting_url)
        
        Returns:
            array: array of selenium WebElement objects.
            
        """
        left_provinces_div = self.browser.find_element(By.ID,
                                                       Constants.LEFT_PROVINCES_DIV_ID)
        left_provinces_a = left_provinces_div.find_elements(By.TAG_NAME,
                                                            Constants.LEFT_PROVINCES_TAG_NAME)
        
        return left_provinces_a
    
    
    def make_random_sleep(self):
        """
        
        It makes a random sleep in the execution.
        
        """
        delay = random.choice(self.time_sleep_delays)
        self.waited_seconds += delay
        time.sleep(delay)

    def scrap_text_and_href_from_link(self, element):
        """
        
        It returns text and href from 'a' tag element.
        
        Args:
            element (WebElement): 'a' tag element, selenium WebElement.
        
        Returns:
            tuple (string, string): (text, href)
        
        """
        return (element.text, element.get_property(Constants.HREF_PROPERTY))  
    
    def add_all_calendar_holidays_to_scraped_data(self):
        """
        
        It collects all the holidays of the calendar and add them to the variable
        scraped data.
        
        """
        for i, div in enumerate(self.scrap_month_divs()):
            self.current_scraping_month = i+1
            self.add_all_holidays_from_div_to_scraped_data(div)

    def scrap_month_divs(self):
        """
        
        It scrapes the months divs from the provinces own page.
    
        Returns:
            array(WebElements): Array of 'div' tag elements, selenium WebElement objects.

        """
        months_container = self.browser.find_element(By.ID,
                                                     Constants.MONTHS_CONTAINER_ID)
        month_divs = months_container.find_elements(By.CLASS_NAME,
                                                    Constants.MONTHS_DIV_CLASS_NAME)
        
        return month_divs

    def add_all_holidays_from_div_to_scraped_data(self, div):
        """
            It scrapes all holiday info from a month div.
        """
        for holiday_type in Constants.HOLIDAYS_REFS.keys():
            self.add_holidays_by_type_from_div_to_scraped_data(div, holiday_type)
        

    def add_holidays_by_type_from_div_to_scraped_data(self, div, holiday_type):
        """
        
        It scrapes all holidays info from a div where it's type is holiday_type
    
        Args:
            div (WebElement): month div which contains date elements.
            holiday_type (string): HolidayType value.

        Returns:
            array (tuples (int, int/None, string, string)): Array of tuples. 
                Each tuple contains (holiday day number, holiday day 
                moved from if it has, holiday title and, holiday type)
                
        """    
        colored_boxes = div.find_elements(By.CLASS_NAME,
                                          Constants.HOLIDAYS_REFS[holiday_type][Constants.BOX_DAY_REF])        
        colored_spans = div.find_elements(By.CLASS_NAME,
                                          Constants.HOLIDAYS_REFS[holiday_type][Constants.STRING_DAY_REF])
        
        for i, box in enumerate(colored_boxes):            
            string_line = colored_spans[i].find_element_by_xpath('..').text
            string_line_parts = string_line.split('.')
            string_line_left_part = string_line_parts[0]
            string_line_right_part = string_line_parts[1]
            
            if string_line_right_part.find(Constants.MOVED_STRING_INDICATOR) != -1:
                holiday_day_moved_from = int(string_line_left_part.split(' ')[0])
                holiday_name = string_line_right_part.split('(')[0]
            else:
                holiday_day_moved_from = None
                holiday_name = string_line_right_part
            
            holiday_day = int(box.text)
            holiday_info = (holiday_day, holiday_day_moved_from, holiday_name, holiday_type)
            
            holiday_row = self.create_HolidayRow_from_info(holiday_info)
            
            self.scraped_data.append(holiday_row.__repr__())

        
    def create_HolidayRow_from_info(self, holiday_info):
        """

        It creates every HolidayRow element and appends it as an string to the
        scraped_data variable.

        Args:
            holiday_info (tuple): tuple according with the 
                scrap_holidays_days_info_from_div method. Every element is
                a tuple of 4 values (int, int/None, string, string).
                
        Returns:
            HolidayRow: object transformed with the holiday_info.
        """
        holiday_day = holiday_info[0]
        holiday_day_moved_from = holiday_info[1]
        holiday_name = holiday_info[2]
        holiday_type = holiday_info[3]
        
        holiday_date = date(self.current_scraping_year, self.current_scraping_month,
                            holiday_day).strftime(Constants.DATES_FORMAT)
        
        if holiday_day_moved_from is None:
            holiday_date_moved_from = None
        else:
            holiday_date_moved_from = date(self.current_scraping_year, self.current_scraping_month,
                                           holiday_day_moved_from).strftime(Constants.DATES_FORMAT)
        
        holiday_row = HolidayRow(holiday_name, holiday_date, self.current_scraping_province,
                                 holiday_type, holiday_date_moved_from)
        
        return holiday_row
    
    def scrap_previous_year(self):
        """
        
        It scrapes the previous year from the current one and it's url. It will
        return a tuple (None, None) if no previous year is found.
        
        Returns:
            tuple(int/None, string/None): a tuple with (previous year, previous years url).
        
        """
        years_div = self.browser.find_element(By.CLASS_NAME, Constants.YEARS_DIV_CLASS_NAME)
        years_tag_a = years_div.find_elements(By.TAG_NAME, Constants.YEARS_TAG_NAME)
        
        if len(years_tag_a) > 1:
            (text, url) = self.scrap_text_and_href_from_link(years_tag_a[0])
            year = int(text.split(' ')[1])
            return (year, url)
        else:
            return (None, None)

    def end_scraping(self):
        """
        
        Ends the scraping by closing the browser.
        
        """
        self.execution_time = time.time() - self.execution_time
        self.browser.quit()
    
    def create_csv_with_scraped_data(self, csv_name):
        """
        
        It creates a csv with the scraped data.
        
        Args:
            csv_name (string): new csv files name.
        
        """
        file_path = '../csv/' + csv_name + '.csv'
        with open(file_path, 'w+', newline = '') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(self.csv_header)
            writer.writerows(self.scraped_data)
            
        f.close()
    
    def print_scraping_info(self):
        """
        
        It prints info about the scraping done.
        
        """
        print("\n**** SCRAPING INFO ****\n")
        print("- Execution time: {0:0.1f} seconds.".format(self.execution_time))
        print("- Num of executed URLs: {}.".format(self.num_executed_urls))
        print("- Seconds waited between navigations: {}.".format(self.waited_seconds))
        print("- Num of holidays: {}.".format(len(self.scraped_data)))
        print("- Data: \n")
        print(*self.scraped_data, sep="\n")
        print("\n**** END SCRAPING INFO ****\n")
    
    def navigate_to_url(self, url):
        self.browser.get(url)
    
    def get_starting_url(self):
        return self.starting_url
    
    def get_scraped_data(self):
        return self.scraped_data
    
    def set_current_scraping_province(self, s):
        self.current_scraping_province = s
    
    def set_current_scraping_year(self, x):
        self.current_scraping_year = x
    
    def set_current_scraping_month(self, x):
        self.current_scraping_month = x
