/** 
 * Filename: mainREST.ts
 * Version: V1.0
 * Author: JJ Goschen
 * Project name: A-Recognition (Advance)
 * Organization: Singularity
 * Funtional description: Provides an api to access main.ts functions
*/
//npm install express --save
//pip3 install firebase-admin
//pip3 install firebase
import * as Main from "./main";

var express = require("express");
var fs = require('fs');
var cors = require('cors');
var multer = require('multer');
var upload = multer({ dest: '../Facial_Recogntion/' })
var app = express();

app.use(express.json());       // to support JSON-encoded bodies
app.use(express.urlencoded()); // to support URL-encoded bodies
app.use(cors());

app.listen(3000, () => {
 console.log("Server running on port 3000");
});

app.get("/getUsersFromDaysEvents", (req, res, next) => {
    Main.getUsersFromDaysEvents().then( users => res.json(users)).catch( err => res.send(err));
});

app.post("/getUsersFromDaysEvents", (req, res) => { 
    Main.getUsersFromDaysEvents().then( users => res.json(users)).catch( err => res.send(err));
});


app.get("/validateUserHasBooking", (req, res, next) => {

    let email;
    let room;

    if(req.query.hasOwnProperty("email") && req.query.hasOwnProperty("room")){
        
        email = JSON.parse(req.query.email);
        room = JSON.parse(req.query.room);

        Main.validateUserHasBooking(email,room).then(msg=> {res.send(msg);console.log(msg)}).catch( err => res.send(err));
    }else{
        res.send("Please send email and room name");
    }    
});

app.post("/validateUserHasBooking", (req, res, next) => {

    let email;
    let room;

    console.log(req.query);
    
    if(req.query.hasOwnProperty("email") && req.query.hasOwnProperty("room")){
        
        email = req.query.email;
        room = req.query.room;

        Main.validateUserHasBooking(email,room).then( msg => {res.send(msg);console.log(msg)}).catch( err => res.send(err));
    }else{
        res.send("Please send email and room name");
    }    
});

app.post("/richardsResponse", (req, res, next) => {

    //console.log(req.body);
    let answer = req.body;

    console.log(answer);
    
    res.send(answer);
});

app.get('/getEmails', (req, res) => {

    Main.getEmployeeEmails().then( employees =>{
        res.json(employees);
    }).catch( err => res.send(err));
});

app.get('/isEmployee', (req, res) => {

    let email = req.query.email;

    if(email == undefined)
        res.send("Please send a valid email");
    else
        Main.isEmployee(JSON.parse(email) ).then( result =>{
            res.send(result);
        }).catch( result=>{
            res.send(result);
        });
    
});
/** 
 * Function Name:addEmployee
 * Version: V1.0
 * Author: Richard McFadden
 * Funtional description: takes in formdata which contains everything
 * needed to add a new user.
*/
app.post('/addEmployee',upload.single('image'), async(req, res) => {

    // doTheThingWithTheObject();
    // passItToRichard();
    await delay(6000);
    res.json(Main.addEmplpoyee(req)); 
});
/** 
 * Function Name:addEmployeeTaken
 * Version: V1.0
 * Author: Richard McFadden
 * Funtional description: first tranforms the base64 to be usable
*/
app.get('/addEmployeeTaken', async(req, res) => 
{
    //console.log(req.query.image);
    // Grab the extension to resolve any image error
    var ext = (req.query.image).split(';')[0].match(/jpeg|png|gif/)[0];
    var data = (req.query.image).replace(/^data:image\/\w+;base64,/, "");
    console.log(data);
    fs.writeFile('../Facial_Recogntion/image.'+ext, data,'base64', (err,res)=>
    {
        if(err) 
        {
            console.log("error",err);
        }
    });
    await delay(6000);
    res.json(Main.addEmplpoyeeTaken(req)); 
});

app.get('/generateToken', (req, res) => {
    res.json(Main.generateToken());
});

function delay(ms: number) {
    return new Promise( resolve => setTimeout(resolve, ms) );
}
  