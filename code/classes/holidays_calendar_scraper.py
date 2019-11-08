# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date

from classes.holiday_row import HolidayType, HolidayRow
from classes.holidays_calendar_constants import Constants

class HolidaysCalendarScraper:
    """
    
        HolidaysCalendarScraper is a class which allows to obtain all the 
        holidays of every province of every year (from 2006-2019 inclusive). 
    
        Args:
            chrome_driver_path (string): chromes driver path.
            starting_url (string): url
        
        Attributes:
            chrome_driver_path (string): chromes driver path.
            starting_url (string): the url where the browser will start to scrap.
            browser (webdriver.Chrome): the current browser.
            current_scraping_province (string): the province which is currently scraping.
            current_scraping_year (int): the year which is currently scraping.
            current_scraping_month (int): the month which is currently scraping.
            scraped_data (array): the list of strings parsed from HolidayRow 
                objects with its __str__ method.
                
    """
    
    def __init__(self, chrome_driver_path, starting_url):
        self.chrome_driver_path = chrome_driver_path
        self.starting_url = starting_url
        
        self.browser = webdriver.Chrome(self.chrome_driver_path)
        
        self.current_scraping_province = None
        self.current_scraping_year = None
        self.current_scraping_month = None
        
        self.scraped_data = []
    
    def start_scraping(self):
        """
        
        Starts the scraping process. It scrapes all the holidays of every year 
        of every province.
        
        """
        self.browser.get(self.starting_url)
        
        starting_year = 2019
        for element in self.scrap_provinces_a_elements():
            self.current_scraping_year = starting_year
            self.current_scraping_province, next_url = self.scrap_text_and_href_from_link(element)
            
            while (next_url is not None):
                self.browser.get(next_url)   
                self.add_all_calendar_holidays_to_scraped_data()
                self.current_scraping_year, next_url = self.scrap_previous_year()
            
 
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
            self.scrap_all_holidays_info_from_div(div)

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

    def scrap_all_holidays_info_from_div(self, div):
        """
            It scrapes all holiday info from a month div.
        """
        for holiday_type in Constants.HOLIDAYS_REFS.keys():
            self.scrap_holidays_info_from_div_by_type(div, holiday_type)
        

    def scrap_holidays_info_from_div_by_type(self, div, holiday_type):
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
            
            self.scraped_data.append(str(holiday_row))

        
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
        self.browser.quit()
    
    def navigate_to_url(self, url):
        self.browser.get(url)
    
    def get_scraped_data(self):
        return self.scraped_data
    
    def set_current_scraping_province(self, s):
        self.current_scraping_province = s
    
    def set_current_scraping_year(self, x):
        self.current_scraping_year = x
    
    def set_current_scraping_month(self, x):
        self.current_scraping_month = x
