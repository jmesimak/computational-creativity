var fs = require('fs');

var length = 500;

fs.readFile('bachnotes', 'utf-8', function(err, notes) {

  var occurrences = constructOccurrences(notes);
  var pO = occurrences.pitchOccurrences;
  var dO = occurrences.durationOccurrences;
  var startP = Object.keys(pO)[getRandomInt(0, Object.keys(pO).length)];
  var startD = Object.keys(dO)[getRandomInt(0, Object.keys(dO).length)];
  var construct = '';
  for (var i = 0; i < length; i++) {
    construct += startP + startD + ' ';
    startP = pO[startP][getRandomInt(0, pO[startP].length)];
    startD = dO[startD][getRandomInt(0, dO[startD].length)];
  }
  smoothOccurrences(occurrences.pitchOccurrences);
  smoothOccurrences(occurrences.durationOccurrences);
  fs.writeFile('musicchain_2_smooth', construct);

});

function smoothOccurrences(occurrences) {

  var keys = Object.keys(occurrences);
  var arrays = keys.map(function(key) {
    return occurrences[key];
  });
  arrays.forEach((arr, i) => {

    var map = new Map();
    var ctr = 0;
    var note = keys[i];

    arr.forEach((item) => {
      if (!map.get(item)) {
        map.set(item, 1);
      } else {
        map.set(item, map.get(item) + 1);
      }
      ctr++;
    });

    var inc = Math.floor((ctr / map.size) * 1.2);

    map.forEach((val, k) => {
      if (val < inc) {
        map.set(k, val + inc);
      } else {
        map.set(k, val - inc);
      }
    });

    var newArr = [];

    map.forEach((val, k) => {
      for (var i = 0; i < val; i++) {
        newArr.push(k);
      }
    });
    occurrences[note] = newArr;
  });

}

function constructOccurrences(notes) {
  var tokens = notes.replace(/\W+/g, " ").split(' ');
  var pitchOccurrences = {};
  var durationOccurrences = {};
  var currentDuration;
  var nextDuration;

  for (var i = 0; i < tokens.length - 1; i++) {
    var current = tokens[i];
    var next = tokens[i+1];
    var currentPitch = current.replace(/(\d+)/g, '');
    var nextPitch = next.replace(/(\d+)/g, '');
    var tryDuration = current.replace(/[a-zA-Z]+/g, '');
    var nextDuration = next.replace(/[a-zA-Z]+/g, '');
    if (tryDuration) {
      currentDuration = tryDuration;
    }

    if (currentPitch && nextPitch) {
      if (!nextDuration) {
        nextDuration = currentDuration;
      }

      if (!pitchOccurrences.hasOwnProperty(currentPitch)) {
        pitchOccurrences[currentPitch] = [];
      }

      if (!durationOccurrences.hasOwnProperty(currentDuration)) {
        durationOccurrences[currentDuration] = [];
      }

      pitchOccurrences[currentPitch].push(nextPitch);
      durationOccurrences[currentDuration].push(nextDuration);
    }
  }

  return {
    pitchOccurrences: pitchOccurrences,
    durationOccurrences: durationOccurrences
  };
}

function getRandomInt(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}
