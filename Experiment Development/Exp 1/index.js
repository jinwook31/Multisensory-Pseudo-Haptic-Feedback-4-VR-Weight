// BASE SETUP
// =============================================================================
var timestamp = require('console-timestamp');
var now = new Date();

//Logging
var winston = require('winston'); require('date-utils'); 
const fs = require('fs'); 
const logDir = 'log'; 

if (!fs.existsSync(logDir)) { 
	fs.mkdirSync(logDir); 
} 

const tsFormat = () => (new Date()).toLocaleTimeString(); 

var logger = new (winston.Logger)({ 
	transports: [ 
		new (winston.transports.Console)({ 
			timestamp: tsFormat, colorize: true, level: 'info' 
			}), 
		new (require('winston-daily-rotate-file'))({
			level: 'info', 
			timestamp: tsFormat,
			datePattern: 'YYYY-MM-DD', 
			filename: `${logDir}/logs.log`, 
			prepend: true, 
		}) 
	] 
});

// call the packages we need
var express    = require('express');        // call express
var app        = express();                 // define our app using express
var bodyParser = require('body-parser');

// configure app to use bodyParser()
// this will let us get the data from a POST
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var port = process.env.PORT || 3000;        // set our port

// ROUTES FOR OUR API
// =============================================================================
var router = express.Router();              // get an instance of the express Router

// test route to make sure everything is working (accessed at GET http://localhost:8080/api)
router.get('/', function(req, res) { });

app.post('/setEMS', function(req,res){  //0 or 1
  let data = JSON.stringify(req.body)
  fs.writeFileSync('EMSStatus.json', data);
  res.send('saved')
});

app.post('/getEMS', function(req,res){  
  fs.readFile('EMSStatus.json', (err, data) => {  
    if (err) throw err;
    let statusEMS = JSON.parse(data);
	res.send(JSON.stringify(statusEMS));
	console.log('YY:MM:DD hh:mm:ss'.timestamp + ' - Data Sent to RPI Zero');
  });
});


// REGISTER OUR ROUTES -------------------------------
// all of our routes will be prefixed with /api
app.use('/api', router);

// START THE SERVER
// =============================================================================
app.listen(port);
console.log('YY:MM:DD hh:mm:ss'.timestamp + '  REST API server on port ' + port);
logger.info('  REST API server on port ' + port);

