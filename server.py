from random import randint
from gtts import gTTS
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template


# Returns the change in value for a stock in percent (Today/Most recent number)
# https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
def get_stock_change(avanza_stock_url):
    url = avanza_stock_url
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
    # file_number = str(randint(0, 1000000))
    tts.save(savefile="static/stock" + ".mp3")
    print("File stock" + ".mp3 created")


# Testing/Playing around
text_to_audio(
    "Storytel: " + get_stock_change('https://www.avanza.se/aktier/om-aktien.html/32576/storytel-b') + " procent")

# Flask web-server
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/updateStock/')
def update_stock():
    print('Updating stock audio file!')
    text_to_audio(
        "Storytel: " + get_stock_change('https://www.avanza.se/aktier/om-aktien.html/32576/storytel-b') + " procent")
    return "Stock audio updated!"


if __name__ == '__main__':
    app.run(host='192.168.1.160')
