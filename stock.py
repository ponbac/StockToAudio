import requests
from bs4 import BeautifulSoup


# https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe


class Stock:
    def __init__(self, avanza_url):
        # Parse variables
        self.url = avanza_url
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.content, "html.parser")

        # Stock data
        self.name = self.get_name()
        self.value_change = self.get_value_change()

    # Get the stocks name
    def get_name(self):
        name_box = self.soup.find('h1', attrs={'class': 'large marginBottom10px'})
        return str(name_box.text).replace('\r', '').replace('\n', '').replace('\t', '').strip()  # Returns cleaned name

    # Get the value change for today in percent
    def get_value_change(self):
        # TODO: NEED CHANGE! Band-aid fix to make function work regardless of positive/negative in html class name.
        try:
            change_box = self.soup.find('span', attrs={'class': 'changePercent SText bold positive'})
            return change_box.text[0:-2] + '%'  # Return example '+2,43%'
        except AttributeError:
            change_box = self.soup.find('span', attrs={'class': 'changePercent SText bold negative'})
            return change_box.text[0:-2] + '%'  # Return example '-1,37%'

    # Update values that change over time
    def update(self):
        # Refresh page
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        # Get new values
        self.value_change = self.get_value_change()
