from random import randint
from gtts import gTTS
import requests
from bs4 import BeautifulSoup


# Returns the change in value for a stock in percent (Today/Most recent number)
# https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
def get_stock_change(stock_url):
    url = stock_url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # TODO: NEED CHANGE! Band-aid fix to make function work regardless of positive/negative in html class name.
    try:
        change_box = soup.find('span', attrs={'class': 'changePercent SText bold positive'})
        change = change_box.text
    except AttributeError:
        change_box = soup.find('span', attrs={'class': 'changePercent SText bold negative'})
        change = change_box.text

    return change[0:-2]


# Creates mp3-file with given text
def text_to_audio(text):
    tts = gTTS(text=text, lang='sv')
    file_number = str(randint(0, 1000000))
    tts.save(savefile="mp3/test" + file_number + ".mp3")
    print("File test" + file_number + ".mp3 created")


# Testing/Playing around
text_to_audio(
    "Testaktie: " + get_stock_change('https://www.avanza.se/aktier/om-aktien.html/32576/storytel-b') + " procent")
