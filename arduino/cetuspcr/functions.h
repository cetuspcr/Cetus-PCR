#include "devices.h"

int hey[20];
// byte size = Serial.readBytes(input, INPUT_SIZE);
// Add the final 0 to end the C string

void setTemperature(char pwm_width){
    analogWrite(peltier, pwm_width);
    Serial.print("setting_peltier::");
    Serial.println(pwm_width);
}


float readTemperature(int index){
	pinSensors.requestTemperatures();
    temp = pinSensors.getTempCByIndex(index);
    return (temp);
}
