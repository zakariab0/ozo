import time
from selenium import webdriver
from bs4 import BeautifulSoup

# Class for checking forex news events
class News:

    # Static method to check the forex calendar for high-impact events
    @staticmethod
    def check_forex_day(site):
        # Instantiate the Selenium webdriver (using Chrome in this case)
        driver = webdriver.Chrome()
        driver.get(site)  # Navigate to the specified website
        time.sleep(4)  # Wait for the page to load (adjust sleep time as needed)

        # Get the page source after it has loaded
        html_content = driver.page_source

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all rows in the forex calendar table
        news_elements = soup.find_all('tr', class_='calendar__row')

        # Initialize counters and flags
        high_impact_count = 0  # Count of high-impact news events
        fomc_flag = False  # Flag to track if FOMC news is present

        # Iterate through each row in the calendar
        for element in news_elements:
            # Extract currency, impact, event, and time elements
            currency_element = element.find('td', class_='calendar__cell calendar__currency')
            impact_element = element.find('td', class_='calendar__cell calendar__impact')
            event_element = element.find('td', class_='calendar__cell calendar__event event')
            time_element = element.find('td', class_='calendar__cell calendar__time')

            # Check if all required elements are present
            if currency_element and impact_element and time_element:
                currency = currency_element.text.strip()  # Extract currency (e.g., USD)
                impact = impact_element.find('span', title='High Impact Expected')  # Check for high-impact news
                event_time_str = time_element.text.strip()  # Extract event time (e.g., '12:30pm')

                # Check for USD bank holidays
                if currency == 'USD' and impact_element.find('span', title='Non-Economic') and 'Bank Holiday' in event_element.text.strip():
                    driver.quit()  # Close the browser
                    return "Bad day, USD Bank Holiday"  # Return if it's a bank holiday

                # Check for high-impact USD news
                if currency == 'USD' and impact:
                    high_impact_count += 1  # Increment high-impact counter
                    if event_element and 'FOMC' in event_element.text.strip():
                        fomc_flag = True  # Set FOMC flag if FOMC news is found

                # Check for specific high-impact events at 12:30pm
                if event_time_str == '12:30pm' and currency == 'USD' and impact:
                    driver.quit()  # Close the browser
                    return "Bad day, 12:30pm event, USD currency, and high impact"

        # Determine the overall trading day quality based on the news events
        if high_impact_count > 3:
            driver.quit()  # Close the browser
            return "Bad day, high impact news over 3, sleeping until tomorrow"
        elif high_impact_count >= 1 and fomc_flag:
            driver.quit()  # Close the browser
            return "Bad day, FOMC speaking USD, sleeping until tomorrow"
        else:
            driver.quit()  # Close the browser
            return "Good day"  # Return if no bad conditions are met