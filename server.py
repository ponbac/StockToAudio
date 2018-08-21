from flask import Flask, render_template, make_response
from main import *


'''---FLASK PART---'''
app = Flask(__name__)  # create Flask-object


# Index
@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp


# TODO: Check if program works without random file endings!
# Called to create new stock audio file. File name = 'stock + random number from js + .mp3'
@app.route('/updateStock/<rand_num>')
def update_stock(rand_num):
    print('Updating stock audio file!')
    text_to_audio(generate_stock_list(stocks_to_follow), rand_num)
    return "Stock audio updated!" + str(rand_num)


# main
if __name__ == '__main__':
    # init (clear audio folder and get the stocks to follow)
    clear_audio_folder()
    stocks_to_follow = read_stocks_file()
    # start the flask server
    app.run(host='localhost')
