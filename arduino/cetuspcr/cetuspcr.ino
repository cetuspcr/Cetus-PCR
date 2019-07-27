#include "functions.h"
#include "serialtools.h"


void setup(){
    Serial.begin(9600);
    Serial.println("Cetus is ready.");
}


void loop(){
        recieveCommand();
        showNewData();
    }
