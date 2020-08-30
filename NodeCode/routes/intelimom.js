var express = require('express');
var db = require('../config/mongoConnection');
var router = express.Router();
var emailValidator = require('email-validator');
var uniqid = require('uniqid');
const fs = require('fs');
var path = require('path');

router.post('/intervalCheck', function (req, res, next) {
  let filename = req.body.file.split('.');
  //let path1 = `../public/python/output_audio_files/${filename[0]}_summary.wav`;
  let path1 = path.join(
    __dirname,
    '../public/python/output_audio_files',
    `${filename[0]}_summary.wav`
  );
  let path2 = path.join(
    __dirname,
    '../summary',
    `${filename[0]}_summary_extracted_keyword.txt`
  );
  let path3 = path.join(
    __dirname,
    '../transcripts',
    `${filename[0]}transcript_with_keyword.json`
  );
  try {
    if (fs.existsSync(path1)) {
      try {
        if (fs.existsSync(path1)) {
          try {
            if (fs.existsSync(path1)) {
              res.send({ message: 'file_exist' });
            } else {
              res.send({ message: 'file_not_found' });
            }
          } catch (err) {
            console.error(err);
          }
        } else {
          res.send({ message: 'file_not_found' });
        }
      } catch (err) {
        console.error(err);
      }
    } else {
      res.send({ message: 'file_not_found' });
    }
  } catch (err) {
    console.error(err);
  }

  //res.send({ message: 'file not found' });
});

router.post('/getReport', function (req, res, next) {
  console.log('getReport');
  console.log(req.body.file);
  let filename = req.body.file.split('.');
  console.log(filename);
  //let path1 = `../public/python/output_audio_files/${filename[0]}_summary.wav`;
  let path1 = path.join(
    __dirname,
    '../public/python/output_audio_files',
    `${filename[0]}_summary.wav`
  );
  let path2 = path.join(
    __dirname,
    '../summary',
    `${filename[0]}_summary_extracted_keyword.txt`
  );
  let path3 = path.join(
    __dirname,
    '../transcripts',
    `${filename[0]}transcript_with_keyword.json`
  );

  let rawdata = fs.readFileSync(path3);
  let transcript = JSON.parse(rawdata);

  let conSummar = fs.readFileSync(path2, 'utf8');
  //console.log(rawdata);

  res.send({
    messages: transcript,
    soundUrl: `http://10.176.113.7:5000/public/python/output_audio_files/${filename[0]}_summary.wav`,
    summary: conSummar,
  });
});

//api for login
router.post('/imom_login', function (req, res, next) {
  const database = db.getDatabase();
  var userEmail = req.body.userId;
  //console.log(req.body);
  try {
    if (emailValidator.validate(userEmail)) {
      var userId = userEmail.split('@')[0];
      //console.log(userId);
      var results = database
        .collection('user_collection')
        .find({ username: new RegExp(userId, 'i') })
        .toArray(function (err, result) {
          if (result.length > 0) {
            res.send({
              status: 'success',
              message: 'valid user',
              userId: result[0].username,
            });
          } else {
            res.send({ status: 'error', message: 'invalid user' });
          }
        });
    } else {
      res.send({ status: 'error', message: 'invalid user id' });
    }
  } catch (e) {
    res.send(e);
  }
});

module.exports = router;
