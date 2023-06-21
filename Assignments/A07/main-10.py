#  Author:           Jorge Santos
#  Title:            web scraping
#  Course:           4883
#  Semester:         Summer 2023
""" 
Description:
    This code will present the user with a GUI with multiple dropdown options.
    Based off the users input it will than build a url and get that sata under the summary table
    from the weather underground website. THan it will take this data and put it in a GUI table.
'.
"""
import PySimpleGUI as sg
import json
import functools
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service

# used to create a print function that flushes the buffer
flushprint = functools.partial(print, flush=True)


# create a print function that flushes the buffer immediately

def asyncGetWeather(url):
    """Returns the page source HTML from a URL rendered by ChromeDriver.
        Args:
            url (str): The URL to get the page source HTML from.
        Returns:
            str: The page source HTML from the URL.
            
        Help:
        https://stackoverflow.com/questions/76444501/typeerror-init-got-multiple-values-for-argument-options/76444544
        """

    # change '/usr/local/bin/chromedriver' to the path of your chromedriver executable
    service = Service(executable_path='/usr/local/bin/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome(service=service, options=options)  # run ChromeDriver
    flushprint("Getting page...")
    driver.get(url)  # load the web page from the URL
    flushprint("waiting 3 seconds for dynamic data to load...")
    time.sleep(3)  # wait for the web page to load
    flushprint("Done ... returning page source HTML")
    render = driver.page_source  # get the page source HTML
    driver.quit()  # quit ChromeDriver
    return render  # return the page source HTML


def currentDate(returnType='tuple'):
    """ Get the current date and return it as a tuple, list, or dictionary.
    Args:
        returnType (str): The type of object to return.  Valid values are 'tuple', 'list', or 'dict'.
    """
    from datetime import datetime
    if returnType == 'tuple':
        return (datetime.now().month, datetime.now().day, datetime.now().year)
    elif returnType == 'list':
        return [datetime.now().month, datetime.now().day, datetime.now().year]

    return {
        'day': datetime.now().day,
        'month': datetime.now().month,
        'year': datetime.now().year
    }


def buildWeatherURL(month=None, day=None, year=None, airport=None, filter=None):
    """ A gui to pass parameters to get the weather from the web.
    Args:
        month (int): The month to get the weather for.
        day (int): The day to get the weather for.
        year (int): The year to get the weather for.
    Returns:
        Should return a URL like this, but replace the month, day, and year, filter, and airport with the values passed in.
        https://www.wunderground.com/history/daily/KCHO/date/2020-12-31
    """
    current_month, current_day, current_year = currentDate('tuple')

    if not month:
        month = current_month
    if not day:
        day = current_day
    if not year:
        year = current_year
    # a list named cpdes will hold in the airport codes from the json file
    codes = []
    with open('data.json') as f:
        data = json.load(f)
        for airport in data:
            codes.append(airport['icao'])

    # Create the gui's layout using text boxes that allow for user input without checking for valid input
    layout = [
        [sg.Text('Month')], [sg.DropDown(list(range(1, 13)))],
        [sg.Text('Day')], [sg.DropDown(list(range(1, 32)))],
        [sg.Text('Year')], [sg.DropDown((list(range(1999, 2024))))],
        [sg.Text('Code')], [sg.DropDown(codes)],
        [sg.Text('Daily / Weekly / Monthly')], [sg.DropDown(['daily', 'weekly', 'monthly'])],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Get The Weather', layout)

    event, values = window.read()
    window.close()

    month = values[0]
    day = values[1]
    year = values[2]
    code = values[3]
    filter = values[4]

    sg.popup('You entered', f"Month: {month}, Day: {day}, Year: {year}, Code: {code}, Filter: {filter}")

    # return the URL to pass to wunderground to get appropriate weather data
    return f"https://www.wunderground.com/history/{filter}/{code}/date/{year}-{month}-{day}"

#will displat the data in a GUI table
def displayT(data):
    # Define the table headings
    headings = list(data[0].keys())
    data = [list(d.values()) for d in data]
    # Create the table layout
    layout = [
        [sg.Table(values=data, headings=headings, auto_size_columns=True, display_row_numbers=True)],
        [sg.Button('Close')]
    ]

    # Create the window
    window = sg.Window('Table View', layout)

    # Event loop
    while True:
        event, _ = window.read()
        if event == 'Close' or event == sg.WINDOW_CLOSED:
            break

    # Close the window
    window.close()

if __name__ == '__main__':
    url = buildWeatherURL()


    print(url)
    # get the page source HTML from the URL
    page = asyncGetWeather(url)
    with open('sourcecode.html') as f:
        table = f.read()
    # parse the HTML
    soup = BeautifulSoup(page, 'html.parser')

    # find the appropriate tag that contains the weather data
    history = soup.find('lib-city-history-observation')

    # print the parsed HTML
    #print(history.prettify())

    soup_data = history.find_all('tbody', class_='ng-star-inserted')
    tables = soup.find_all('table')

    rows = soup.find_all('tr')
    head = soup.find_all('th')

    allData = []

    keys = []
    for d in head:
        key = d.text.strip().replace(' ', '').replace('\n', '')
        keys.append(key)
    #take only the data that we need to populate the table
    for row in rows:
        row = row.find_all('td')
        data = []
        for td in row:
            # print(data.text.strip().replace(' ','').replace('\n',''))
            # print("====================================")
            data.append(td.text.strip().replace(' ', '').replace('\n', '').replace('Polygon', ''))
        dictionary = dict(zip(keys, data))
        allData.append(dictionary)
    #print(allData)
    displayT(allData)

