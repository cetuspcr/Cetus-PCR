#include "serialtools.h"


void setup(){
    Serial.begin(9600);
    initializePins();
}


void loop(){
    recieveCommand();
    splitData();
}
