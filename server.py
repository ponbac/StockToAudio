from random import randint
from gtts import gTTS
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, make_response


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
rand = 0

def text_to_audio(text):
    global rand
    tts = gTTS(text=text, lang='sv')
    # file_number = str(randint(0, 1000000))
    tts.save(savefile="static/stock" + str(rand) + ".mp3")
    print("File stock" + str(rand) + ".mp3 created")


# Testing/Playing around
# text_to_audio(
# "Storytel: " + get_stock_change('https://www.avanza.se/aktier/om-aktien.html/32576/storytel-b') + " procent")

# Flask web-server
app = Flask(__name__)


@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp


# @app.route('/updateStock/')
# def update_stock():
#     print('Updating stock audio file!')
#     text_to_audio(
#         "Storytel: " + get_stock_change('https://www.avanza.se/aktier/om-aktien.html/32576/storytel-b') + " procent")
#     return "Stock audio updated!"

@app.route('/updateStock/<rand_num>')
def update_stock(rand_num):
    global rand
    rand = rand_num
    text_to_audio(str(randint(0, 20)))
    return str(rand)


if __name__ == '__main__':
    # app.run(host='192.168.1.160')
    app.run(host='localhost')
