console.log("main.js loaded!")

var randNum = 10;
var sound;

function loadAudio() {
    //Create the audio tag
    var soundFile = document.createElement("audio");
    soundFile.preload = "none";

    //Load the sound file (using a source element for expandability)
    var src = document.createElement("source");
    console.log('Going to read randNum');
    src.src = '/static/stock' + randNum + ".mp3";
    soundFile.appendChild(src);

    //Load the audio tag
    //It auto plays as a fallback
    soundFile.load();
    soundFile.volume = 0.1;
    soundFile.play();

    sound = soundFile;
}


//Plays the sound
function playAudio(audio, volume) {
    //Set the current time for the audio file to the beginning
    audio.currentTime = 0.01;
    audio.volume = volume;

    //Due to a bug in Firefox, the audio needs to be played after a delay
    setTimeout(function () {
        audio.play();
    }, 1);
}


function playSound() {
    console.log('Playing audio!');
    loadAudio();
    playAudio(sound, 0.1);
}


function refreshData() {
    x = 8;  // 5 Seconds

    $.getJSON('/updateStock/');

    console.log('At playSound()');
    playSound();

    setTimeout(refreshData, x * 1000);
}

refreshData();