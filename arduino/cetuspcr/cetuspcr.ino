// #include "serialfunctions.h"

// float pcr_temp, lid_temp;

// void setup(){
//     Serial.begin(9600);

//     setupSensors();
// }

// void loop(){
//     // pcr_temp = readTemperature(0);
//     // lid_temp = readTemperature(1);

//     readExperiment();

//     if (newData == true){
//         Serial.println(experimentInfo[0]);
//         Serial.println(experimentInfo[1]);
//         Serial.println(experimentInfo[2]);
//         newData == false;
//     }
// }


const int peltier = 3;

void setup(){
    Serial.begin(9600);
    pinMode(peltier, OUTPUT);

    analogWrite(peltier, 0);
    digitalWrite(8, HIGH);
}

void loop(){
    digitalWrite(8, HIGH);
    if (Serial.available() > 0){
        int value = Serial.parseInt();
        Serial.println(value);
        if (value >= 0 && value <= 255){
            analogWrite(peltier, value);
        }
    }
}
