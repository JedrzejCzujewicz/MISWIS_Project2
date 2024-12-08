#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp;

#define PWMpin 11

float pwm=0;

void setup() {
  Serial.begin(9600);
  while ( !Serial ) delay(100);
  unsigned status= bmp.begin(0x76);
}

void loop() {
    Serial.print(bmp.readTemperature());
    Serial.print('\t');
    Serial.println(pwm/255);
    pwm=255;
    analogWrite(PWMpin, pwm);
    delay(100);
}
