import time
from selenium import webdriver
from bs4 import BeautifulSoup


class News:

    @staticmethod
    def check_forex_day(site):
        # Instantiate the Selenium webdriver
        driver = webdriver.Chrome()
        driver.get(site)
        time.sleep(4)
        # Continue with your existing code
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        news_elements = soup.find_all('tr', class_='calendar__row')
        high_impact_count = 0
        fomc_flag = False
        for element in news_elements:
            currency_element = element.find('td', class_='calendar__cell calendar__currency')
            impact_element = element.find('td', class_='calendar__cell calendar__impact')
            event_element = element.find('td', class_='calendar__cell calendar__event event')
            time_element = element.find('td', class_='calendar__cell calendar__time')
            if currency_element and impact_element and time_element:
                currency = currency_element.text.strip()
                impact = impact_element.find('span', title='High Impact Expected')
                event_time_str = time_element.text.strip()

                if currency == 'USD' and impact_element.find('span', title='Non-Economic') and 'Bank Holiday' in event_element.text.strip():
                    return "Bad day, USD Bank Holiday"

                if currency == 'USD' and impact:
                    high_impact_count += 1
                    if event_element and 'FOMC' in event_element.text.strip():
                        fomc_flag = True
                if event_time_str == '12:30pm' and currency == 'USD' and impact:
                    return "Bad day, 12:30pm event, USD currency, and high impact"

        if high_impact_count > 3:
            return "Bad day, high impact news over 3, sleeping until tomorrow"
        elif high_impact_count >= 1 and fomc_flag:
            return "Bad day, FOMC speaking USD, sleeping until tomorrow"
        else:
            return "Good day"
        driver.quit()


