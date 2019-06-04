#include "temperaturesensors.h"

const int peltier = 3;

int experimentInfo[3];


int celsiusToPWM(int celsius){
    return (NULL);
}

void setTemperature(int c){
    analogWrite(peltier, celsiusToPWM(c));
}

