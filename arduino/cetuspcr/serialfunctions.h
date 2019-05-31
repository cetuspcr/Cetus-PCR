#include "thermocycler.h"

String incomingCommand;

boolean newData = false;

void readExperiment(){
    boolean receiving = false;

    int currentExperimentData = 0;
    char splitChar = '&';
    char startChar = '<';
    char endChar = '>';
    char newByte;

    while (Serial.available() > 0 && newData == false){
        newByte = Serial.read();
        if (receiving == true){
            if (newByte != endChar){
                if (newByte != splitChar){
                    incomingCommand.concat(newByte);
                }
                else{
                    experimentInfo[currentExperimentData] = incomingCommand.toInt();
                    incomingCommand = "";
                    currentExperimentData++;
                }
            }
            else {
                experimentInfo[currentExperimentData] = incomingCommand.toInt();
                incomingCommand = "";
                receiving = false;
                newData == true;
                Serial.println("Reading finished.");
            }
            
        }
        else if (newByte == startChar){
            Serial.println("Start reading.");
            receiving == true;
        }
    }
}
