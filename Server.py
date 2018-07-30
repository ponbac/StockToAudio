from random import randint

from gtts import gTTS


def text_to_audio(text):
    tts = gTTS(text=text, lang='sv')
    file_number = str(randint(0, 1000000))
    tts.save(savefile="mp3/test" + file_number + ".mp3")
    print("File test" + file_number + ".mp3 created")


text_to_audio("Fingerprint: upp 3,23 procent")
