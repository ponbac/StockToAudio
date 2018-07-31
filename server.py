from random import randint
from gtts import gTTS
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, make_response
import os


# Clear audio folder or create one if it doesnt exist
def clear_audio_folder():
    folder = os.getcwd() + '/static/audio'

    if os.path.isdir(folder):
        print('Clearing /static/audio folder!')

        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
    else:
        print('Creating /static/audio folder!')
        os.makedirs(folder)


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
rand = 0  # Stores random number from main.js


def text_to_audio(text):
    global rand
    tts = gTTS(text=text, lang='sv')
    # file_number = str(randint(0, 1000000))
    tts.save(savefile="static/audio/stock" + str(rand) + ".mp3")
    print("File stock" + str(rand) + ".mp3 created")


# Testing/Playing around
# text_to_audio(
# "Storytel: " + get_stock_change('https://www.avanza.se/aktier/om-aktien.html/32576/storytel-b') + " procent")

# Flask web-server
app = Flask(__name__)


# Index
@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp


# Called to create new stock audio file. File name = 'stock + random number from js + .mp3'
@app.route('/updateStock/<rand_num>')
def update_stock(rand_num):
    global rand
    rand = rand_num
    print('Updating stock audio file!')
    text_to_audio(
        "Storytel: " + get_stock_change('https://www.avanza.se/aktier/om-aktien.html/32576/storytel-b') + " procent")
    return "Stock audio updated!" + str(rand)


# Start server
if __name__ == '__main__':
    clear_audio_folder()
    app.run(host='192.168.1.160')
    # app.run(host='localhost')
