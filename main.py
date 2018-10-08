import os
from gtts import gTTS
from stock import Stock


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


# Read stocks.txt and return array with all the stocks as Stock-objects
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
def text_to_audio(text, random_file_ending):
    tts = gTTS(text=text, lang='sv')
    tts.save(savefile="static/audio/stock" + str(random_file_ending) + ".mp3")
    print("File stock" + str(random_file_ending) + ".mp3 created")