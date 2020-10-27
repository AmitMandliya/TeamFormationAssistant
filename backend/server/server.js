const express= require('express');
const bodyParser=require('body-parser');
const cors=require('cors');
const fetch = require("node-fetch");

const app=express();
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cors());

var mysql = require('mysql');
 
// create a connection variable
var con = mysql.createConnection({
  host: "database", // server ip address
  port: "3306",
  user: "dbuser", // user name
  password: "dbuserpwd", // password
  database: "teamformationassistant" // database name
});

// connect to the database.
con.connect(function(err) {
  if (err) throw err;
  // if connection successful
  console.log('connection successful!!!');
});

app.get('/',(req,res)=>{
  res.json('Server is Up... OK');
})

app.get('/getResults', (req, res) => {
    con.query('SELECT * from Team', function(err, rows, fields) {
        if (!err) {
            res.send(rows);
        } else {
            console.log('Error while performing Query.');
        }	
	});
});

app.post('/Signup',(req,res)=>{
	var records = [[req.body.name,req.body.hourlyrate,req.body.dob,req.body.languages,0,req.body.memberrole,req.body.experience,req.body.skillscore,req.body.availablehoursperweek]];
	if(records[0][0]!=null)
	{
		con.query("INSERT INTO Member (MemberName,HourlyRate,DOB,Languages,IsAssigned,MemberRole,Experience,SkillScore,AvailableHoursPerWeek) VALUES ?",[records],function(err,res,fields){

		if(err) throw err;

		console.log(res);
		});
	}
	//res.json('Form received...Thank You for signing up :D');
	return res.redirect('http://localhost:3000/TeamFormationAssistant/Signup/Success');
})

app.post('/ProjectDetails',(req,res)=>{
	console.log(req.body);
	var records = [[req.body.name,req.body.enddate,req.body.teamsize,req.body.budget,req.body.tools,req.body.priority,0]];
	console.log(records);
	if(records[0][0]!=null)
	{
		con.query("INSERT INTO Project (ProjectName,ProjectEndDate,ProjectTeamSize,Budget,Tools,Priority,IsAssignmentComplete) VALUES ?",[records],function(err,res,fields){

			if(err) throw err;

			console.log(res);
		});
		
		var i=0;
		var colname = 'languagepreferred'+i;
		
		while(colname in req.body){
			var records = [[req.body.languagepreferred0,Number(req.body.skill0),req.body.memberrole0,Number(req.body.availablehoursperweek0),Number(req.body.skillweight[i]),Number(req.body.experienceweight[i]),Number(req.body.hoursweight[i]),Number(req.body.languageweight[i]),Number(req.body.budgetweight[i])]];
			console.log(records);
			con.query("CALL populateRequirements ?",[records],function(err,res,fields){

				if(err) throw err;

				console.log(res);
			});
			i += 1;
			colname = 'languagepreferred'+i;
		}
	}
	
	//res.json('Form received...Thank You for signing up :D');
	
    //execute the algorithm from here
	fetch('http://localhost:5000/executeAlgo');
	
	return res.redirect('http://localhost:3000/TeamFormationAssistant/ProjectDetails/Success');
})

app.listen(8080, ()=>{
  console.log("Port 8080");
})


