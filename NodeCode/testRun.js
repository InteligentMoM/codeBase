var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var cors = require('cors');
const fileUpload = require('express-fileupload');
const { exec } = require('child_process');

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');
var intelimomRouter = require('./routes/intelimom');
var mongodb = require('./config/mongoConnection');
var app = express();

function callpython() {
  var pypath = `Main_Run.py`;
  var fullpath = `wavs/new2.wav`;
  var spawn = require('child_process').spawn;
  var process = spawn('python', [`Main_Run.py`, '-a', fullpath]);

  process.stdout.on('data', function (data) {
    console.log(data.toString());
  });

  //   exec(`python ${pypath} --audio_name ${fullpath}`, function (
  //     error,
  //     stdout,
  //     stderr
  //   ) {
  //     if (error !== null) {
  //       console.log(error);
  //     } else {
  //       console.log('stdout: ' + stdout);
  //       console.log('stderr: ' + stderr);
  //     }
  //   });
}

callpython();
