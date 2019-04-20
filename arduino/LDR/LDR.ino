// Script para teste de comunicação serial
// O programa deve ler uma porta analógica (A0) e enviar a leitura para a
// porta serial, juntamente com o tempo.

const int LDR = A0;
int value;
int cycletime = 10;

bool is_running = false;

void setup() {
  Serial.begin(9600);
  Serial.println("Ready");
  
  for (int i = 1; i <= cycletime; i++){
    delay(1000);
    value = analogRead(LDR);
    Serial.print(i);
    Serial.println(" x:");
    Serial.print(value);
    Serial.println(" y:");
  }
  Serial.println("&&");
}

void loop(){
  Serial.read();
}
