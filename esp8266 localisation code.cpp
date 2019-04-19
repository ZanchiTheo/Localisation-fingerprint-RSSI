#include <Arduino.h>
#include "ESP8266WiFi.h"

void setup() {
  Serial.begin(9600);

  // Met le wifi en attente (en mode station) et le déconnecte de tout réseau auquel il auurait pu être connecté
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

  //Serial.println("Parametrage effectue");
}

void loop() {
  //Serial.println("Debut du scan");
  
  

  // WiFi.scanNetworks renvoie le nombre de réseau wifi trouvé
  int n = WiFi.scanNetworks();
  //Serial.println("Scan termine");
  //if (n == 0) {
    //Serial.println("Aucun reseau trouve");
  //}
  //else
  //{
    //Serial.print(n);
    //Serial.println(" reseaux trouvee");
    for (int i = 0; i < n; ++i)
    {
      // renvoie sur le moniteur le SSID et le RSSI (force du réseau) pour chaque réseau trouvé
      Serial.print("/");
      Serial.print(WiFi.SSID(i));
      Serial.print(",");
      //imprimer le RSSI mesuré
      Serial.print(WiFi.RSSI(i));
      // imprimer l'adresse MAC de l'AP entendue
      
      //Serial.println((WiFi.encryptionType(i) == ENC_TYPE_NONE)?" ":"*");
      delay(10);
    }
  //}
  Serial.println("");

  // attend 5 secondes et scanne à nouveau
  delay(3000);

  //serial interaction
  if (Serial.available())
  {
    String str = Serial.readString();
    if(str.equals("mac")){
      //Serial.println(WiFi.macAddress());     
    }
     if(str.startsWith("lon")){
            
     }
  }
}