//Keep track of how many parts are moving. As more buttons are pressed on the controller, 
//  this number increases. If you release them, it decreases. 
var moving_parts_count;

//This is just some workaround to an issue with the UI. As time went, the interface go slower
//  until it was unusable. The issue got fixed as soon as you clicked on the screen. To fix
//  this, a random click onto the screen was implemented to keep focus on the UI and prevent it
//  from slowing down. Each iteration of the loop, this number increases by 1. When c % 100 == 0,
//  then click on the screen. 
var c = 0;

//Keep track of last time a GET or POST request was made
var last_request_GET = new Date()
var last_request_POST = new Date();

//Server URL
var server = "http://127.0.0.1:5000/test";

//Map wchich will be jsonified and sent the server. When a button is pressed, a corresponding
//  key's value is changed. 
var json = {'lmotors': 0, 
            'rmotors': 0, 
            'le_motors': 0, 
            'bin_motors': 0, 
            'le_speed': 1, 
            'lr_speed': 1, 
            'back_act': 0, 
            'front_act': 0
        };

function main() {
    window.addEventListener("gamepadconnected", (e) => {
        console.log(
            "Gamepad connected at index %d: %s. %d buttons, %d axes.",
            e.gamepad.index,
            e.gamepad.id,
            e.gamepad.buttons.length,
            e.gamepad.axes.length
        );
        setInterval(loop, 50);
    });
}

function loop() {
    if (c%100 == 0){
        RandomClick();
    }
    var gp = navigator.getGamepads()[0];
    //Detect button presses. Decided to leave thumbsticks out to avoid problems with stick drift
    //A: 0          RB: 5           L3: 10              D-right: 15
    //B: 1          LT: 6           R3: 11
    //X: 2          RT: 7           D-up: 12
    //Y: 3          select: 8       D-down: 13
    //LB: 4         pause: 9        D-left: 14
    if (gp && gp.connected) {
        var buttons = gp.buttons;
        for (var i in buttons) {
            if (buttons[i].pressed == true) { console.log("buttons[%s] pressed", i); };
        };
        var moving_parts_count = 0;
        
        //If user presses A, retract front linear actuator. If user pressed X, retract 
        //  front linear actuator
        if (buttons[0].pressed || buttons[2].pressed){
            buttons[0].pressed 
                ? ActivateFrontLinActs(true, -1)
                : ActivateFrontLinActs(true, 1);
            moving_parts_count++;
        } else {
            ActivateFrontLinActs(false, 0);
        }

        //If user presses B, retract back linear actuator. If user presses Y, extend
        //  back linear actuator
        if (buttons[1].pressed || buttons[3].pressed){
            buttons[1].pressed
                ? ActivateBackLinActs(true, -1)
                : ActivateBackLinActs(true, 1);
            moving_parts_count++;
        } else {
            ActivateBackLinActs(false, 0);
        }
    } 
    var moving_parts = document.getElementById("moving-part");
    moving_parts.innerHTML = moving_parts_count;
    c++;
    
}

const pressed_color = "#ee8282";
const unpressed_color = "transparent";

function ActivateLeftMotors(isPressed, direction){
    if (direction > 1 || direction < -1){
        throw Error("The value for the direction of the motor cannot be greater than 1 or less than -1");
    }
    var part = document.getElementById("motor1");
    json["lmotors"] = direction;
    if (isPressed == true){
        part.style.backgroundColor = pressed_color;
    } else {
        part.style.backgroundColor = unpressed_color;
    }
}

function ActivateRightMotors(isPressed, direction){
    if (direction > 1 || direction < -1){
        throw Error("The value for the direction of the motor cannot be greater than 1 or less than -1");
    }
    var part = document.getElementById("motor2");
    json["rmotors"] = direction;
    if (isPressed == true){
        part.style.backgroundColor = pressed_color;
    } else {
        part.style.backgroundColor = unpressed_color;
    }
}

function ActivateFrontLinActs(isPressed, direction){
    if (direction > 1 || direction < -1){
        throw Error("The value for the direction of the motor cannot be greater than 1 or less than -1");
    }
    var part = document.getElementById("front-act");
    json["front_act"] = direction;
    if (isPressed == true){
        part.style.backgroundColor = pressed_color;
    } else {
        part.style.backgroundColor = unpressed_color;
    }
}

function ActivateBackLinActs(isPressed, direction){
    if (direction > 1 || direction < -1){
        throw Error("The value for the direction of the motor cannot be greater than 1 or less than -1");
    }
    var part = document.getElementById("back-act");
    json["back_act"] = direction;
    if (isPressed == true){
        part.style.backgroundColor = pressed_color;
    } else {
        part.style.backgroundColor = unpressed_color;
    }
}

function RandomClick(){
    let element_click = document.getElementById("bin");
    element_click.click();
    console.log("random clik");
}

function getData(){

    let req_time = new Date();

    if (last_request_GET - req_time > 500){
        const xhr = new XMLHttpRequest();
        xhr.open("GET", "https://regres.in/api/users");
        xhr.send();
        console.log("request send");
    }
}

//Sedn the dummy request. If the time since the last request is less than 500 ms,
//  it will not send the request
function buttonOnclickGet() {
    console.log("GET");
    let req_time = new Date();
    console.log(req_time - last_request_GET);

    if (req_time - last_request_GET > 500){
        const xhr = new XMLHttpRequest();
        xhr.open("GET", server, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // Request was successful, handle response here
                    console.log(xhr.responseText);
                    var toJson = JSON.parse(xhr.responseText);
                    console.log(toJson["stat"]);
                } else {
                    // Request failed
                    console.error('Request failed with status:', xhr.status);
                }
            }
        };
        xhr.send();
        console.log("request sent to python server");
        last_request_GET = new Date();
    }
}

function buttonOnclickPost() {
    console.log("POST");
    let req_time = new Date();
    console.log(req_time - last_request_POST);

    if (req_time - last_request_POST > 500){
        const xhr = new XMLHttpRequest();
        var data = {"forward/back": 0,"right/left": 1,};
        xhr.open("POST", server, true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify(json));
        console.log("request sent to python server");
        last_request_POST = new Date();
    }
}
