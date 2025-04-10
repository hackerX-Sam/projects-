const express = require ('express');
const cors = require('cors');
const bodyparser = require('bodyparser');
const app = express();
const port = 3000;

app.use(cors());
app.use(bodyparser.json());


let alerts=[];
let helpRequests=[];


app.post('/api/alert', (req, res) => {
    const alert = req.body;
    alerts.push(alert);
    res.status(201).send({ message: 'Alert received!' });
  });
  

  app.get('/api/alerts', (req, res) => {
    res.send(alerts);
  });
  

  app.post('/api/help', (req, res) => {
    const help = req.body;
    helpRequests.push(help);
    res.status(201).send({ message: 'Help request received!' });
  });
  

  app.get('/api/help', (req, res) => {
    res.send(helpRequests);
  });
  
  app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
  });
