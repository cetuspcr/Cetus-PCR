#include <Arduino.h>

// Pin definitions
#define SENSOR_LID A0
#define SENSOR_PELTIER A2
#define LID_PIN 3
// #define COOLER_PIN 4

// H - Bridge pins
#define SIDE_A_PIN 4 // Cooling
#define SIDE_B_PIN 2 // Heat
#define PWM_PIN 3

// Variables to processing incoming data
const byte cmdSize = 20;
char receivedChars[cmdSize];
boolean newData = false;
const char startMarker = '<';
const char endMarker = '>';
char *splitMarker = " ";
char *newCommand;
char *commandTitle;
int arguments[10];

// Control variables
bool isCooling = false;
int coolingTemperature;

float readTemperature(int sensor_pin)
{
    // Temperature sensor tested: LM35
    int reading = analogRead(sensor_pin);
    float temperature = ((reading / 1024.0) * 5000) / 10;
    return (temperature);
}

void heatPeltier(int pwm_signal)
{
    digitalWrite(SIDE_A_PIN, LOW);
    digitalWrite(SIDE_B_PIN, HIGH);
    analogWrite(PWM_PIN, pwm_signal);
}

void coolPeltier(int pwm_signal)
{
    digitalWrite(SIDE_A_PIN, HIGH);
    digitalWrite(SIDE_B_PIN, LOW);
    analogWrite(PWM_PIN, pwm_signal);
}

void initializePins()
{
    pinMode(SIDE_A_PIN, OUTPUT);
    pinMode(SIDE_B_PIN, OUTPUT);
    pinMode(PWM_PIN, OUTPUT);
    pinMode(LID_PIN, OUTPUT);

    digitalWrite(SIDE_A_PIN, LOW);
    digitalWrite(SIDE_B_PIN, LOW);
    analogWrite(PWM_PIN, 0);
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
/*
An string command must have this generic structure:
  <commandTitle argument argument argument ...> (up to 10 arguments) 

The data is processed as follow:
  - *char commandTitle: A string of characters with the command to be executed
  - int arguments[10]: The arguments of the command to be executed

  The code is structed that way to be maintainable and easy to expand.
  Every new command is going to be processed in a new if as necessary.  
 
*/
{
    // --------------------------------------------------- Pre-processing data
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

        // ----------------------------------------- Execute the command as needed
        if (commandTitle == "peltier") // <peltier state pwm_signal>
        {
            if (arguments[0] == 0) // if heat
            {
                heatPeltier(arguments[2]);
                Serial.print("Heat: ");
                Serial.println(arguments[2]);
            }
            else if (arguments[0] == 1) // if cooling
            {
                coolPeltier(arguments[2]);
                Serial.print("Cooling: ");
                Serial.println(arguments[2]);
            }

            Serial.print("tempSample ");
            Serial.println(readTemperature(SENSOR_PELTIER));
            // Serial.print("tempLid ");
            // Serial.println(readTemperature(SENSOR_LID));
        }
        else if (commandTitle == "cooling")
        { // <cooling temperature_target>
            isCooling = true;
            coolingTemperature = arguments[0];
            Serial.print("cooling started at: ");
            Serial.println(coolingTemperature);
        }
        else if (commandTitle == "printTemps"){
            Serial.print("tempSample ");
            Serial.println(readTemperature(SENSOR_PELTIER));
        }

        if (isCooling == true)
        {
            if (readTemperature(SENSOR_PELTIER) >= coolingTemperature)
            {
                coolPeltier(255);
                Serial.print("tempSample ");
                Serial.println(readTemperature(SENSOR_PELTIER));
            }
            else
            {
                isCooling = false;
                coolPeltier(0);
                Serial.println("Cooling finished");
            }

            Serial.println(commandTitle);
        }
        // Request new data
        Serial.println("nextpls");
        newData = false;
    }
    // else
    // {
    //     // Always send temperature data
    //     Serial.print("tempSample ");
    //     Serial.println(readTemperature(SENSOR_PELTIER));
    // }
}