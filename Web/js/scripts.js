var game_loop;
var moving_parts_count;


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

        if (buttons[0].pressed){
            console.log("Left");
            MoveLeft(true);
            moving_parts_count++;
        } else {
            MoveLeft(false);
        }

        if (buttons[1].pressed){
            console.log("right");
            MoveRight(true);
            moving_parts_count++;
        } else {
            MoveRight(false);
        }
    } 
    var moving_parts = document.getElementById("moving-part");
    moving_parts.innerHTML = moving_parts_count.toString();
}

function MoveForward(isPressed){
    var part = document.getElementById("motor1");
    if (isPressed == true){
        part.style.backgroundColor = "#FC2E2E";
    } else {
        part.style.backgroundColor = "aliceblue";
    }
}

function MoveBack(isPressed){
    var part = document.getElementById("motor2");
    if (isPressed == true){
        part.style.backgroundColor = "#FC2E2E";
    } else {
        part.style.backgroundColor = "aliceblue";
    }
}

function MoveLeft(isPressed){
    var part = document.getElementById("excavator");
    if (isPressed == true){
        part.style.backgroundColor = "#FC2E2E";
    } else {
        part.style.backgroundColor = "aliceblue";
    }
}

function MoveRight(isPressed){
    var part = document.getElementById("bin");
    if (isPressed == true){
        part.style.backgroundColor = "#FC2E2E";
    } else {
        part.style.backgroundColor = "aliceblue";
    }
}
