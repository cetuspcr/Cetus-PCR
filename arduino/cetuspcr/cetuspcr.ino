#include "serialtools.h"

void setup(){
    Serial.begin(19200);
    Serial.println("Cetus is ready.");
    temperatureSensor.begin();
    temperatureSensor.setResolution(10);
}

void loop(){
    recieveCommand();
    splitData();

    // runCommand();
    if (isToPrintTemperature == true){
        printTemperature();
    }
}
