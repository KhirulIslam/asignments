const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

var mysql = require("mysql");

var con = mysql.createConnection({
  host: process.env.MYSQL_HOST_IP,
  user: process.env.MYSQL_USER,
  password: process.env.MYSQL_PASSWORD,
  database: process.env.MYSQL_DATABASE,
  port: process.env.PORT
});

con.connect(function(err) {
  if (err) throw err;
  console.log("Db Connected!");
});

const config = {
  name: "sample-express-app",
  port: 3000,
  host: "0.0.0.0"
};

const app = express();

app.use(bodyParser.json());
app.use(cors());

app.get("/", (req, res) => {
  con.query("SELECT id,name, LEFT(occupation, 1) as occupation FROM employees", function (err, result, fields) {
    if (err) throw err;
  res.json(result)
  });
});

app.get("/employee-details", (req, res) => {
  var id = req.query.id;
  con.query("SELECT * FROM employees where id=?",[id], function (err, result, fields) {
    if (err) throw err;
    res.status(200).send(result);
  });
});


//select count(occupation) as count, occupation FROM employees group by occupation

app.get("/occupation-summary", (req, res) => {
  con.query("select count(occupation) as count, occupation FROM employees group by occupation order by count desc", function (err, result, fields) {
    if (err) throw err;
    // console.log(result);

  res.status(200).send(result);
  });
});

app.listen(config.port, config.host, e => {
  if (e) {
    throw new Error("Internal Server Error");
  }
  console.log(`${config.name} running on ${config.host}:${config.port}`);
});
