var game_loop;
var moving_parts_count;
var c = 0;

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
<<<<<<< HEAD
    moving_parts.innerHTML = moving_parts_count.toString();
    c++;
=======
    moving_parts.innerHTML = moving_parts_count;
>>>>>>> cc8d1bbc23c62f7029b322cd5215a2b54900d50a
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

<<<<<<< HEAD

function MoveLeft(isPressed){
=======
function ActivateExcavator(isPressed){
>>>>>>> cc8d1bbc23c62f7029b322cd5215a2b54900d50a
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
