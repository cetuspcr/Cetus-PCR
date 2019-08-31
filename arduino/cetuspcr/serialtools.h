#include <DallasTemperature.h>
#include <OneWire.h>

#define peltierHeat 5
#define peltierCool 6

const byte cmdSize = 20;
char receivedChars[cmdSize];
boolean newData = false;
const char startMarker = '<';
const char endMarker = '>';
char* splitMarker = " ";
char* newCommand;
char* commandTitle;

bool isToPrintTemperature = false;

// bool runStep = false;
// unsigned long startTime;
// int duration;

int arguments[10];

OneWire bus(2);
DallasTemperature temperatureSensor (&bus);


void printTemperature(){
    temperatureSensor.requestTemperatures();
    Serial.print("tempSample ");
    Serial.println(temperatureSensor.getTempCByIndex(0));
    Serial.print("tempLid ");
    Serial.println(temperatureSensor.getTempCByIndex(1));
}

// void pcrStep(int temperature, int time){
//     static bool isStarted = false;
//     if (isStarted == false){
//         startTime = millis();
//         duration = time * 1000;
//         int temp = temperature;
//         isStarted = true;
//         Serial.print("Setting Peltier high at: ");
//         Serial.println(temp);
//         digitalWrite(5, HIGH);
//         Serial.print("Started time: ");
//         Serial.println(startTime);
//     }

//     else {
//         Serial.print("startTime: ");
//         Serial.println(startTime);
//         Serial.print("newtime: ");
//         Serial.println(millis());
//         if ((millis() - startTime) >= duration){
//             Serial.println("Setting Peltier low.");
//             digitalWrite(5, LOW);
//             Serial.println("nextpls");
//             isStarted = false;
//             runStep = false;
//         }
//     }
// }


void recieveCommand() {
    static byte index = 0;
    static boolean isRecieving = false;
    char newChar;
    if (Serial.available() > 0 && newData == false) {
        newChar = Serial.read();
        if (isRecieving == true){
            if (newChar != endMarker){
                receivedChars[index] = newChar;
                index++;
            }
            else {
                receivedChars[cmdSize - 1] = '\0';
                isRecieving = false;
                index = 0;
                newData = true;
            }
        }
        else if (newChar == startMarker){
            isRecieving = true;
        }    
    }
}


void splitData() {
    if (newData == true) {
        int idxArg = 0;
        for (int x = 0; x < sizeof(arguments) / sizeof(arguments[0]); x++) {
                arguments[x] = 0;
        }
        newCommand = strtok(receivedChars, splitMarker);
        String commandTitle(newCommand);
        while (newCommand != '\0'){
            newCommand = strtok(NULL, splitMarker);
            arguments[idxArg] = atoi(newCommand);
            idxArg += 2;
        }
        if (commandTitle == "peltier"){
            // <peltier state pwm_signal>
            if (arguments[0] == 0){ // if heat
                Serial.print("Heat: ");
                Serial.println(arguments[2]);
                digitalWrite(peltierHeat, arguments[2]);
                digitalWrite(peltierCool, LOW);
            }
            else if (arguments[0] == 1){ // if cooling
                Serial.print("Cooling: ");
                Serial.println(arguments[2]);
                digitalWrite(peltierCool, arguments[2]);
                digitalWrite(peltierHeat, LOW);
            }
            
            
        }
        else if (commandTitle == "printTemps"){
            isToPrintTemperature = arguments[0];
        }
        for (int x = 0; x < sizeof(arguments) / sizeof(arguments[0]); x++)
        {
            arguments[x] = 0;
        }
        newData = false;
    }
}


// void runCommand(){
//     if (runStep == true){
//         pcrStep(arguments[0], arguments[2]);
//     }
// }