console.log("main.js loaded!")

var randNum = Math.floor((Math.random() * 10000) + 1);
var sound;

function loadAudio() {
    //Create the audio tag
    var soundFile = document.createElement("audio");
    soundFile.preload = "none";

    //Load the sound file (using a source element for expandability)
    var src = document.createElement("source");
    console.log('Going to read randNum! randNum = ' + randNum);
    src.src = '/static/audio/stock' + randNum + ".mp3";
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

    console.log('Playing audio!, randNum = ' + randNum);

    //Due to a bug in Firefox, the audio needs to be played after a delay
    setTimeout(function () {
        audio.play();
    }, 1);
}


function playSound() {
    console.log('Playing sound!, randNum = ' + randNum);
    loadAudio();
    playAudio(sound, 0.1);
}


function refreshData() {
    x = 8;  // 8 Seconds

    console.log('At playSound(), randNum = ' + randNum);
    playSound();
    randNum = Math.floor((Math.random() * 10000) + 1);
    console.log('Set new randNum = ' + randNum);
    $.getJSON('/updateStock/' + randNum);

    setTimeout(refreshData, x * 1000);
}

refreshData();