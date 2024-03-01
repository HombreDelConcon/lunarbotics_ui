var game_loop;
var moving_parts_count;
var c = 0;
var last_request_GET = new Date()
var last_request_POST = new Date().getMilliseconds();
console.log(last_request_GET);
console.log(last_request_POST);
var server = "http://127.0.0.1:5000/test";

function main() {
    window.addEventListener("gamepadconnected", (e) => {
        console.log(
            "Gamepad connected at index %d: %s. %d buttons, %d axes.",
            e.gamepad.index,
            e.gamepad.id,
            e.gamepad.buttons.length,
            e.gamepad.axes.length
        );
        game_loop = setInterval(GameLoop, 50);
    });
}

function GameLoop() {
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
        //If user presses RB, move forward
        if (buttons[5].pressed){
            console.log("forward");
            MoveForward(true);
            moving_parts_count++;
            getData();
        } else {
            MoveForward(false);
        }
        
        //If user presses LB, move back
        if (buttons[4].pressed){
            console.log("Back");
            MoveBack(true);
            moving_parts_count++;
        } else {
            MoveBack(false);
        }
        
        //If user presses A, activate excavator
        if (buttons[0].pressed){
            console.log("Left");
            ActivateExcavator(true);
            moving_parts_count++;
        } else {
            ActivateExcavator(false);
        }

        //If user presses B, activate bin
        if (buttons[1].pressed){
            console.log("right");
            ActivateBin(true);
            moving_parts_count++;
        } else {
            ActivateBin(false);
        }
    } 
    var moving_parts = document.getElementById("moving-part");
    moving_parts.innerHTML = moving_parts_count;
}

const pressed_color = "#ee8282";
const unpressed_color = "transparent";

function MoveForward(isPressed){
    var part = document.getElementById("motor1");
    if (isPressed == true){
        part.style.backgroundColor = pressed_color;
    } else {
        part.style.backgroundColor = unpressed_color;
    }
}

function MoveBack(isPressed){
    var part = document.getElementById("motor2");
    if (isPressed == true){
        part.style.backgroundColor = pressed_color;
    } else {
        part.style.backgroundColor = unpressed_color;
    }
}

function ActivateExcavator(isPressed){
    var part = document.getElementById("excavator");
    if (isPressed == true){
        part.style.backgroundColor = pressed_color;
    } else {
        part.style.backgroundColor = unpressed_color;
    }
}

function ActivateBin(isPressed){
    var part = document.getElementById("bin");
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
        xhr.send(JSON.stringify(data));
        console.log("request sent to python server");
        last_request_POST = new Date();
    }
}
