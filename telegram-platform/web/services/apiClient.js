const axios = require('axios');
const api = axios.create({ baseURL: process.env.BACKEND_URL || 'http://127.0.0.1:8000/api', timeout: 10000 });
module.exports = api;
