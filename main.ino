#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp;

#define PWMpin 11

//deklaracja zmiennych
float temp_zadana=30;
int time=0;
float calka=0.0;
float uchyb=0.0;
float prev_uchyb=0.0;

//deklaracja stalych
float Kp=892.44; //<-Tutaj wstaw wartosci
float Ki=61.97; //<-Tutaj wstaw wartosci
float Kd=3212.78; //<-Tutaj wstaw wartosci
float T=0.1; //czas probkowania //<-Tutaj wstaw wartosci
float czlon_p=0.0;
float czlon_i=0.0;
float czlon_d=0.0;
int min_limit=0; //minimalna wartosc PWM
int max_limit=255; //maksymalna wartosc PWM

void setup() {
  Serial.begin(9600);
  while ( !Serial ) delay(100);
  unsigned status = bmp.begin(0x76);
  pinMode(PWMpin, OUTPUT);
}

void loop() {
  if (Serial.available()) 
  {
    String input = Serial.readStringUntil('\n');
    if (input.startsWith("T")) 
    {
      temp_zadana = input.substring(1).toFloat();
    }
  }
  float temp_aktualna=bmp.readTemperature();
  int syg_ster=PID(temp_zadana, temp_aktualna);
  time++;
  analogWrite(PWMpin, syg_ster);
  Serial.print(time);
  Serial.print(",");
  Serial.print(temp_aktualna);
  Serial.print(",");
  Serial.println(syg_ster);
  delay(100);
}

float PID(float zadana, float zmierzona) {
  float uchyb = zadana - zmierzona;
  float czlon_p = Kp * uchyb;
  float potencjalna_calka = calka + uchyb * T;
  float potencjalny_czlon_i = Ki * potencjalna_calka;
  float czlon_d = Kd * (uchyb - prev_uchyb) / T;
  float PIDoutput = czlon_p + potencjalny_czlon_i + czlon_d;
  // prosty anty-windup
  if (PIDoutput >= 0 && PIDoutput <= 255) {
    calka = potencjalna_calka;
    czlon_i = potencjalny_czlon_i;
  }
  if (PIDoutput > 255) PIDoutput = 255;
  if (PIDoutput < 0) PIDoutput = 0;
  prev_uchyb = uchyb;
  return PIDoutput;
}
