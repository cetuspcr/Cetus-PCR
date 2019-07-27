const byte cmdSize = 20;
char receivedChars[cmdSize];

boolean newData = false;

const char startMarker = '<';
const char endMarker = '>';
char* splitMarker = " ";
char* newCommand;
char* commandTitle;
int arguments[10];

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
                Serial.print("Full Data: ");
                Serial.println(receivedChars);
            }
        }
        else if (newChar == startMarker){
            isRecieving = true;
        }    
    }
}


void splitData() {
    int idxArg = 0;
    if (newData == true) {
        newCommand = strtok(receivedChars, splitMarker);
        commandTitle = newCommand;
        while (newCommand != '\0'){
            newCommand = strtok(NULL, splitMarker);
            arguments[idxArg] = atoi(newCommand);
            idxArg += 2;
        }

        Serial.print("Command: ");
        Serial.println(commandTitle);
        for (auto &i: arguments){
            if (i != 0){
                Serial.print("Argument: ");
                Serial.println(i);
            }
           
        }
        for (int x = 0; x < sizeof(arguments) / sizeof(arguments[0]); x++) {
            arguments[x] = 0;
        }
        newData = false;
        delay(500);
        Serial.println("nextpls");
    }
}