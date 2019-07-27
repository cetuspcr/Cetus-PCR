const int peltier = 3;
int value;

void setup(){
    Serial.begin(9600);
    Serial.println("Cetus is ready.");
    pinMode(peltier, OUTPUT);
}

void loop(){
    delay(500);
    if (Serial.available() > 0){
        Serial.println("Reading.");
        value = Serial.read();
        Serial.print("Valor: ");
        Serial.println(value);
        analogWrite(peltier, value);
    }
}
