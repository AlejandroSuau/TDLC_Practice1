# Masters Degree in Data Science

- **Course**: Typology and Data Life Cicle.
- **Exercise name**: Practice1.
- **Creator**: Alejandro Suau Ruiz.
- **University**: Universitat Oberta de Catalunya (UOC).

## Team Members

- **Alejandro Suau Ruiz**

## Project Structure and File Descriptions

### /code/

- **main.py**: This file contains the main code which allows to scrape the web page.

### /code/classes

- **holiday_row.py**: This file contains the class _HolidayType_ which is used as an enum to identify the holidays's type. It also contains the class _HolidayRow_ which is used to represent a dataset row.
- **holidays_calendar_constants.py**: This file contains the class _Constans_ which is used to avoid _magic_ string in main calendar class.
- **holidays_calendar_scraper.py**: This file contains the main class, _HolidaysCalendarScraper_,which is used to scrap the entire page.

### /code/test

- **test_scraper.py**: This file contains the unittest methods used to test program's behaviour.

### /csv/

- **data.csv**: This file contains the scraped data.

## Resources

1. Subirats, L., Calvo, M. (2018). Web Scraping. Editorial UOC.
2. Masip, D. El lenguaje Python. Editorial UOC.
3. Lawson, R. (2015). Web Scraping with Python. Packt Publishing Ltd. Chapter 2.Scraping the Data.
4. Simon Munzert, Christian Rubba, Peter Meißner, Dominic Nyhuis. (2015). Automated Data Collection with R: A Practical Guide to Web Scraping and Text Mining. John Wiley & Sons.
