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


# Read stocks.txt to get what stocks to read
def read_stocks_file():
    # Create default stocks.txt if none exists
    if not os.path.isfile(os.getcwd() + '/stocks.txt'):
        print('Creating stocks.txt')
        stocks_file_new = open('stocks.txt', 'w+')
        stocks_file_new.write('https://www.avanza.se/aktier/om-aktien.html/3986/amazon-com-inc\n')  # Amazon
        stocks_file_new.write('https://www.avanza.se/aktier/om-aktien.html/185896/netflix-inc\n')  # Netflix
        stocks_file_new.write('https://www.avanza.se/aktier/om-aktien.html/350795/facebook-inc')  # Facebook

    stocks_file = open('stocks.txt', 'rt')
    stocks = []
    for line in stocks_file.readlines():
        stocks.append(line)

    return stocks


# Returns the change in value for a stock in percent (Today/Most recent number)
# https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
def get_stock_change(avanza_stocks):
    clean_stock_data = ""
    for stock in avanza_stocks:
        url = stock
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        # TODO: NEED CHANGE! Band-aid fix to make function work regardless of positive/negative in html class name.
        try:
            change_box = soup.find('span', attrs={'class': 'changePercent SText bold positive'})
            change = change_box.text
            name_box = soup.find('h1', attrs={'class': 'large marginBottom10px'})
            name = name_box.text
        except AttributeError:
            change_box = soup.find('span', attrs={'class': 'changePercent SText bold negative'})
            change = change_box.text
            name_box = soup.find('h1', attrs={'class': 'large marginBottom10px'})
            name = name_box.text

        clean_stock_data += name + " " + change[0:-2] + " procent "

    return clean_stock_data


# Creates mp3-file with given text
rand = 0  # Stores random number from main.js


def text_to_audio(text):
    global rand
    tts = gTTS(text=text, lang='sv')
    # file_number = str(randint(0, 1000000))
    tts.save(savefile="static/audio/stock" + str(rand) + ".mp3")
    print("File stock" + str(rand) + ".mp3 created")


'''---FLASK PART---'''
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
    text_to_audio(get_stock_change(read_stocks_file()))
    return "Stock audio updated!" + str(rand)


# Start server
if __name__ == '__main__':
    clear_audio_folder()
    app.run(host='192.168.1.160')
    # app.run(host='localhost')
