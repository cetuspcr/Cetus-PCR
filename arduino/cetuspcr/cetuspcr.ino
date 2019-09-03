#include "serialtools.h"

void setup(){
    Serial.begin(9600);
    startup();
}

void loop(){
    recieveCommand();
    splitData();
}
