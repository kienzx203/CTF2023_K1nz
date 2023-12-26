const express = require('express');
const crypto = require('crypto');
const path = require('node:path');
const app = express();
const bot = require('./bot.js');
const origin = 'https://biohazard-web.2023.ctfcompetition.com';
const mysql = require('mysql');


// Instantiate clients, defaults to create if not existing.
const db = mysql.createPool({
  connectionLimit: 8,
  host: process.env.DB_HOST,
  user: 'forge',
  password: process.env.DB_PASSWORD,
  database: 'forge'
});

db.query(`CREATE TABLE IF NOT EXISTS bioTable (id varchar(100) PRIMARY KEY, bio TEXT)`, (err) => console.log(err));

app.set('view engine', 'ejs');

app.use('/static/', express.static('js/static', {
  setHeaders: (res) => {
    res.setHeader('Cache-Control', 'public, max-age=600');
  }
}));
app.use(express.json()) // for parsing application/json
app.use(express.urlencoded({ extended: true })) // for parsing application/x-www-form-urlencoded

const setHeaders = (res) => {
  const nonce = crypto.randomBytes(16).toString('base64');
  res.setHeader('Content-Security-Policy', `base-uri 'none'; script-src 'nonce-${nonce}' 'strict-dynamic' 'unsafe-eval'; require-trusted-types-for 'script';`);
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  return nonce;
}


const loadBio = async (id) => {
  let sql = `SELECT * FROM bioTable where id = ?`;
  return new Promise((resolve, reject) => {
    return db.query(sql, [id], (err, results) => {
      if (err) {
        return reject(err.message);
      }
      return resolve(results.length ? results[0].bio : null);
    });
  });
}

const publishBio = async (bio) => {
  return new Promise((resolve, reject) => {
    return db.query(`INSERT INTO bioTable(id, bio) VALUES(?,?)`, [bio.id, JSON.stringify(bio.json)], (err) => {
      if (err) {
        return reject(err.message);
      }
      return resolve();
    });
  });
};

app.get('/bio/:id', async (req, res, next) => {
  try {
    setHeaders(res);
    res.setHeader('Content-Type', 'application/json');
    const bio = await loadBio(req.params.id);
    if (!bio) {
      return res.status(404).send("That bio does not exist!").end();
    }

    res.json(JSON.parse(bio));

  } catch (error) {
    next(error);
  }
});

app.post('/report', async (req, res, next) => {
  setHeaders(res);
  const url = req.body.url || '';
  if (!url.startsWith(`${origin}/view/`)) {
    return res.status(400).send('Invalid bio URL.').end();
  }

  bot.visit(url);
  res.send('Done!').end();
});

app.post('/create', async (req, res, next) => {
  // Gather data submitted.
  id = crypto.randomUUID();
  name = req.body.name || "";

  // Validate any requirements
  if (name == "") {
    return res.status(400).send('No name provided.').end();
  }

  // Build DB object.
  const bio = {
    id: id,
    json: req.body,
  };

  setHeaders(res);
  try {
    // Save and respond with ID.
    await publishBio(bio);
    res.json({ id: id });
  } catch (error) {
    next(error);
  }
});

app.get('*', (req, res, next) => {
  res.set('Cache-control', 'public, max-age=600');
  setHeaders(res);
  res.render('main', {
    title: 'Bio+',
    nonce: setHeaders(res)
  });
});

const PORT = process.env.PORT || 1337;

app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`);
  console.log('Press Ctrl+C to quit.');
});

module.exports = app;
