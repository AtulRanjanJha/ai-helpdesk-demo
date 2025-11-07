const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');

const db = new sqlite3.Database('../helpdesk.db');
const app = express();
app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname)));

// Get all pending requests
app.get('/requests', (req, res) => {
  db.all("SELECT * FROM help_requests WHERE status='pending'", [], (err, rows) => {
    if (err) return res.status(500).send(err.toString());
    res.json(rows);
  });
});

// Answer a help request
app.post('/answer', (req, res) => {
  const { id, answer } = req.body;
  db.run(`UPDATE help_requests SET answer=?, status='resolved' WHERE id=?`, [answer, id], function(err) {
    if (err) return res.status(500).send(err.toString());
    res.json({ message: "Answered!", changes: this.changes });
  });
});

// See full history (any status)
app.get('/history', (req, res) => {
  db.all("SELECT * FROM help_requests ORDER BY created_at DESC", [], (err, rows) => {
    if (err) return res.status(500).send(err.toString());
    res.json(rows);
  });
});

// Timeout: Mark unresolved requests if pending >5 min (runs every 1 min)
setInterval(() => {
  db.run(`UPDATE help_requests 
    SET status = 'unresolved'
    WHERE status = 'pending' AND 
      (strftime('%s','now') - strftime('%s',created_at)) > 300`);
}, 60 * 1000);

const port = 3001;
app.listen(port, () => {
  console.log(`Supervisor UI backend running on http://localhost:${port}`);
  console.log(`Open http://localhost:${port}/requests.html in your browser`);
});
