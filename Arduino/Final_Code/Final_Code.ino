#include <Servo.h>

Servo servo0;  // create servo object to control servo 0 Rotator
Servo servo1;  // create servo object to control servo 1 (Quadrant 1/3) (7-11) pin 7
Servo servo2;  // create servo object to control servo 2 (Quadrant 1/3 Refractor) pin 6
Servo servo3;  // create servo object to control servo 3 (Quadrant 2/4 Refractor) pin 5
Servo servo4;  // create servo object to control servo 4 (Quadrant 2/4) (1-5) pin 4

const int enablePin = 3;  // L293D Pin 1 (PWM for speed control)
const int inputPin1 = 2;  // L293D Pin 2 (Motor direction control 1)

int loopNumber = 1;

// Buffer for incoming data
String incomingData = "";

bool isQ1GoodEgg = false;
bool isQ2GoodEgg = false;
bool isQ3GoodEgg = false;
bool isQ4GoodEgg = false;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // DC Motor setup
  pinMode(enablePin, OUTPUT);
  pinMode(inputPin1, OUTPUT);

  // Servo setup
  servo0.attach(8);
  servo1.attach(4);
  servo2.attach(5);
  servo3.attach(6);
  servo4.attach(7);
  
  // Set initial positions for the servos
  servo1.write(170);
  servo4.write(10);
  servo2.write(175);
  servo3.write(0);
  delay(1000);
  servo0.write(0);
}

void loop() {
  // Check if data is available to read
  if (Serial.available()>0) {
    // Read the incoming data
    String inputString = Serial.readString(); 
    
    // Reset boolean values
    isQ1GoodEgg = false;
    isQ2GoodEgg = false;
    isQ3GoodEgg = false;
    isQ4GoodEgg = false;

    // Parse the received data
    // Parse the received data for Quadrant 1
    if (inputString.indexOf("Quadrant 1: Segar Retak") >= 0) {
      isQ1GoodEgg = false;  // Good egg
    } else if (inputString.indexOf("Quadrant 1: Segar") >= 0) {
      isQ1GoodEgg = true;  // Bad egg
    } else if (inputString.indexOf("Quadrant 1: Buruk") >= 0) {
      isQ1GoodEgg = false;  // Bad egg
    } else if (inputString.indexOf("Quadrant 1: Busuk Retak") >= 0) {
      isQ1GoodEgg = false;  // Bad egg
    }

    // Parse the received data for Quadrant 2
    if (inputString.indexOf("Quadrant 2: Segar Retak") >= 0) {
      isQ2GoodEgg = false;
    } else if (inputString.indexOf("Quadrant 2: Segar") >= 0) {
      isQ2GoodEgg = true;
    } else if (inputString.indexOf("Quadrant 2: Buruk") >= 0) {
      isQ2GoodEgg = false;
    } else if (inputString.indexOf("Quadrant 2: Busuk Retak") >= 0) {
      isQ2GoodEgg = false;
    }

    // Parse the received data for Quadrant 3
    if (inputString.indexOf("Quadrant 3: Segar Retak") >= 0) {
      isQ3GoodEgg = false;
    } else if (inputString.indexOf("Quadrant 3: Segar") >= 0) {
      isQ3GoodEgg = true;
    } else if (inputString.indexOf("Quadrant 3: Buruk") >= 0) {
      isQ3GoodEgg = false;
    } else if (inputString.indexOf("Quadrant 3: Busuk Retak") >= 0) {
      isQ3GoodEgg = false;
    }

    // Parse the received data for Quadrant 4
    if (inputString.indexOf("Quadrant 4: Segar Retak") >= 0) {
      isQ4GoodEgg = false;
    } else if (inputString.indexOf("Quadrant 4: Segar") >= 0) {
      isQ4GoodEgg = true;
    } else if (inputString.indexOf("Quadrant 4: Buruk") >= 0) {
      isQ4GoodEgg = false;
    } else if (inputString.indexOf("Quadrant 4: Busuk Retak") >= 0) {
      isQ4GoodEgg = false;
    }

    if (loopNumber == 1) {
      delay(2000);
      runMotorFunction(1);
      classifyEggServo1(isQ3GoodEgg, true);
      delay(2000);
      resetServosAfterClassify1();
      delay(1000);  // Delay before next classification
      classifyEggServo4(isQ4GoodEgg, true);
      delay(2000);
      resetServosAfterClassify4();
      runMotorFunction(0);
      loopNumber = 2;
    } if (loopNumber == 2) {
      delay(2000);
      runMotorFunction(1);
      rotateServo0Function(true);
      classifyEggServo1(isQ2GoodEgg, true);
      delay(2000);
      resetServosAfterClassify1();
      delay(1000);  // Delay before next classification
      classifyEggServo4(isQ1GoodEgg, true);
      delay(2000);
      resetServosAfterClassify4();
      runMotorFunction(0);
      rotateServo0Function(false);
      loopNumber = 0;
    }
  }
}

// Function definitions remain unchanged

void resetServosAfterClassify1() {
  // Reset all servos to their initial positions after classifying Servo1
  servo1.write(180);  // Reset Servo1
  servo2.write(175);  // Reset Servo2
  servo3.write(0);    // Reset Servo3
  delay(1000);        // Add delay to allow servos to return to position
}

void resetServosAfterClassify4() {
  // Reset all servos to their initial positions after classifying Servo4
  servo4.write(10);   // Reset Servo4
  servo2.write(175);  // Reset Servo2
  servo3.write(0);    // Reset Servo3
  delay(1000);        // Add delay to allow servos to return to position
}

void classifyEggServo1(bool isServo1GoodEgg, bool servo1Triggered) {
  if (servo1Triggered) {
    if (isServo1GoodEgg == true) {
      rotateServo3Function(true);  // Activate Servo3 for good egg
    } else if (isServo1GoodEgg == false) {
    rotateServo2Function(true);
    }
    rotateServo1Function(true);  // Now run Servo1 after classification
    delay(1000);  // Wait before moving to the next step
    
  }
}


void classifyEggServo4(bool isServo4GoodEgg, bool servo4Triggered) {
  if (servo4Triggered) {
    if (isServo4GoodEgg == true) {
      rotateServo3Function(true);  // Activate Servo3 for good egg
    } else if (isServo4GoodEgg == false) {
    rotateServo2Function(true);
    }
    rotateServo4Function(true);  // Now run Servo1 after classification
    delay(1000);  // Wait before moving to the next step
    
  }
}


void runMotorFunction(bool condition) {
  if (condition) {
    digitalWrite(inputPin1, HIGH);
    analogWrite(enablePin, 150);  // Set motor speed up to 255
  } else {
    digitalWrite(inputPin1, LOW);
    analogWrite(enablePin, 0);    // Stop motor
  }
}

void rotateServo0Function(bool condition) { 
  if (condition) {
    servo0.write(180); // Rotate to 180 degrees if condition is true
  } else {
    servo0.write(0);   // Rotate to 0 degrees if condition is false
  }
  delay(2000); // Wait for 2 seconds to allow servo to reach position
}

void rotateServo1Function(bool condition) {
  if (condition) {
    servo1.write(80);
    delay(2000);
  }
}

void rotateServo2Function(bool condition) {
  if (condition) {
    servo2.write(70);
    delay(2000);
  }
}

void rotateServo3Function(bool condition) {
  if (condition) {
    servo3.write(110);
    delay(2000);
  }
}

void rotateServo4Function(bool condition) {
  if (condition) {
    servo4.write(110);
    delay(2000);
  }
}

void rotateServo0FunctionSlow() {
  for (int pos = 0; pos <= 180; pos += 1) {
    servo0.write(pos);
    delay(15);
  }
  delay(3000);
}

void rotateServo1FunctionSlow() {
  for (int pos = 180; pos >= 60; pos -= 1) {
    servo1.write(pos);
    delay(10);
  }
  delay(2000);
}

void rotateServo4FunctionSlow() {
  for (int pos = 0; pos <= 120; pos += 1) {
    servo4.write(pos);
    delay(10);
  }
  delay(2000);
}
