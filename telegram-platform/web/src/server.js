const path = require('path');
const express = require('express');

const app = express();
const PORT = Number(process.env.PORT || 3000);

app.use(express.static(path.join(__dirname, '..', 'public')));

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'frontend-only-nodejs' });
});

app.get('*', (_req, res) => {
  res.sendFile(path.join(__dirname, '..', 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Frontend server running at http://127.0.0.1:${PORT}`);
});
