#include <DallasTemperature.h>
#include <OneWire.h>


float temp;

OneWire pinWire(3);
DallasTemperature pinSensors(&pinWire);

DeviceAddress pcr_sensor;  // Sensor do Bloco de aquecimento
DeviceAddress lid_sensor;  // Sensor da Tampa aquecida

void setupSensors()
{
    pinSensors.begin();  // Start pinSensors

    Serial.print("Devices in this bus: ");
    Serial.println(pinSensors.getDeviceCount());
    pinSensors.getAddress(pcr_sensor, 0);
    pinSensors.getAddress(lid_sensor, 1);
}

float readTemperature(int index)
{
	pinSensors.requestTemperatures();
    temp = pinSensors.getTempCByIndex(index);
    return (temp);
}
