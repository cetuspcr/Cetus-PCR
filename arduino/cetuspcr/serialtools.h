#include <DallasTemperature.h>
#include <OneWire.h>

#define sensorsPin 2
#define lidHeater 3
#define cooler 4
#define peltierHeat 5
#define peltierCool 6

const byte cmdSize = 20;
char receivedChars[cmdSize];
boolean newData = false;
const char startMarker = '<';
const char endMarker = '>';
char *splitMarker = " ";
char *newCommand;
char *commandTitle;
int arguments[10];

bool isToPrintTemperature = false;

OneWire bus(sensorsPin);
DallasTemperature temperatureSensor(&bus);

void startup()
{
    temperatureSensor.begin();
    temperatureSensor.setResolution(10);
    pinMode(peltierHeat, OUTPUT);
    pinMode(peltierCool, OUTPUT);
    Serial.println("Cetus is ready.");
}

void recieveCommand()
{
    static byte index = 0;
    static boolean isRecieving = false;
    char newChar;
    if (Serial.available() > 0 && newData == false)
    {
        newChar = Serial.read();
        if (isRecieving == true)
        {
            if (newChar != endMarker)
            {
                receivedChars[index] = newChar;
                index++;
            }
            else
            {
                receivedChars[cmdSize - 1] = '\0';
                isRecieving = false;
                index = 0;
                newData = true;
            }
        }
        else if (newChar == startMarker)
        {
            isRecieving = true;
        }
    }
}

void splitData()
{
    if (newData == true)
    {
        int idxArg = 0;
        for (int x = 0; x < sizeof(arguments) / sizeof(arguments[0]); x++)
        {
            arguments[x] = 0;
        }
        newCommand = strtok(receivedChars, splitMarker);
        String commandTitle(newCommand);
        while (newCommand != '\0')
        {
            newCommand = strtok(NULL, splitMarker);
            arguments[idxArg] = atoi(newCommand);
            idxArg += 2;
        }
        if (commandTitle == "peltier")
        {
            // <peltier state pwm_signal>
            if (arguments[0] == 0)
            { // if heat
                Serial.print("Heat: ");
                Serial.println(arguments[2]);
                analogWrite(peltierHeat, arguments[2]);
                analogWrite(peltierCool, 0);
                temperatureSensor.requestTemperatures();
                Serial.print("tempSample ");
                Serial.println(temperatureSensor.getTempCByIndex(0));
                Serial.print("tempLid ");
                Serial.println(temperatureSensor.getTempCByIndex(1));
            }
            else if (arguments[0] == 1)
            { // if cooling
                Serial.print("Cooling: ");
                Serial.println(arguments[2]);
                analogWrite(peltierCool, arguments[2]);
                analogWrite(peltierHeat, 0);
            }
        }
        else if (commandTitle == "printTemps")
        {
            isToPrintTemperature = arguments[0];
        }
        Serial.println("nextpls");
        newData = false;
    }
}
