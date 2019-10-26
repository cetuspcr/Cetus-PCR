// #include "serialtools.h"

// void setup(){
//     Serial.begin(9600);
//     startup();
// }

// void loop(){
//     recieveCommand();
//     splitData();
// }


void setup(){
    pinMode(5, OUTPUT);
    pinMode(6, OUTPUT);
}

void loop(){
    digitalWrite(5, HIGH);
    digitalWrite(6, LOW);
}
