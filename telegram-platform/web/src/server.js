require('dotenv').config({ path: '../.env' });
const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const rateLimit = require('express-rate-limit');
const routes = require('../routes');

const app = express();
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '..', 'views'));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cookieParser());
app.use('/ui', express.static(path.join(__dirname, '..', 'ui')));
app.use(rateLimit({ windowMs: 60 * 1000, max: Number(process.env.RATE_LIMIT_PER_MINUTE || 120) }));
app.use('/', routes);

const host = process.env.WEB_HOST || '127.0.0.1';
const port = Number(process.env.WEB_PORT || 3000);
app.listen(port, host, () => console.log(`Web panel listening on ${host}:${port}`));
