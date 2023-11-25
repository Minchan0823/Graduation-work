// netlify/functions/app.js

const express = require('express');
const serverless = require('serverless-http');
const app = express();
const path = require('path');

// 정적 파일을 제공하기 위한 미들웨어
app.use(express.static(path.join(__dirname, '../../path/to/your/static/files')));

// 404 에러 핸들링
app.use((req, res, next) => {
  res.status(404).sendFile('404.html', { root: path.join(__dirname, '../../path/to/your/static/files') });
});

module.exports = app;
module.exports.handler = serverless(app);
