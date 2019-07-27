#include <DallasTemperature.h>
#include <OneWire.h>

#define pcr_sensor 0
#define lid_sensor 1
#define peltier 3

float temp;

OneWire pinWire(2);
DallasTemperature pinSensors(&pinWire);

DeviceAddress pcr_sensor_pin;  // Sensor do Bloco de aquecimento
DeviceAddress lid_sensor_pin;  // Sensor da Tampa aquecida

void setupDevices(){
    pinSensors.begin();  // Start pinSensors

    Serial.print("Devices in this bus: ");
    Serial.println(pinSensors.getDeviceCount());
    pinSensors.getAddress(pcr_sensor_pin, pcr_sensor);
    pinSensors.getAddress(lid_sensor_pin, lid_sensor);
}
