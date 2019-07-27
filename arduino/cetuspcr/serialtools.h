const byte cmdSize = 20;
char receivedChars[cmdSize];

boolean newData = false;

const char startMarker = '<';
const char endMarker = '>';
const char splitMarker = ' ';
char* strtokIndx;

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


void showNewData() {
    if (newData == true) {
        Serial.print("Data: ");
        Serial.println(receivedChars);
        newData = false;
    }
}