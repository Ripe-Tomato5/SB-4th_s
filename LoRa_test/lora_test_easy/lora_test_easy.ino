//LoRaテストコード
void setup() {
  Serial.begin(115200);
  Serial2.begin(115200,SERIAL_8N1,5,17);//ESP:RX=5,TX=17,LoRa:RX=PA3,TX=PA2(RX,TXは互い違いに接続)
  // Serial.println("RESTARTED");
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    char c = (char)Serial.read();
    Serial2.write(c);
  }
  if (Serial2.available()) {
    char c = (char)Serial2.read();
    Serial.write(c);
  } 
}