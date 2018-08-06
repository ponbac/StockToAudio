from gtts import gTTS
from flask import Flask, render_template, make_response
import os
from stock import Stock

# TODO: Test if application works without random file names
rand = 0  # Stores random number from main.js


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
    for url in stocks_file.readlines():
        stocks.append(Stock(url))

    return stocks


# Generate string that holds all the stock names + value changes
def generate_stock_list(stocks):
    stock_list = ''  # String to hold all the data

    # Update every stock and add it to the string (stock_list)
    for stock in stocks:
        stock.update()
        stock_list += stock.name + ' ' + stock.value_change + ' '

    return stock_list


# Creates mp3-file with given text
def text_to_audio(text):
    global rand
    tts = gTTS(text=text, lang='sv')
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
    text_to_audio(generate_stock_list(stocks_to_follow))
    return "Stock audio updated!" + str(rand)


# main
if __name__ == '__main__':
    # init (clear audio folder and get the stocks to follow)
    clear_audio_folder()
    stocks_to_follow = read_stocks_file()
    # start the flask server
    app.run(host='localhost')
