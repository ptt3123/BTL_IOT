#include "DHT.h"
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h> 

#define DHTPIN 14
#define DHTTYPE DHT11  

#define FAN_PIN 5
#define LED_PIN 4
#define AC_PIN 2
#define AO_PIN 0
#define B5_PIN 12

const char* subTopicFan = "sfan";
const char* subTopicLed = "sled";
const char* subTopicAC = "scon";

const char* pubSensorTopic = "psensor";



const char* pubHisFan = "pfan";
const char* pubHisLed = "pled";
const char* pubHisAC = "pcon";


// Wifi
const char* ssid = "vnpt.thanh";  
const char* password = "43211234";

const char* mqtt_server = "192.168.1.8";

WiFiClient espClient;
PubSubClient client(espClient);

DHT dht(DHTPIN, DHTTYPE);

void setup_wifi() {
  delay(2000);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);

  if (String(topic) == subTopicLed) {
    if (message == "on") {
      digitalWrite(LED_PIN, HIGH);
      Serial.println(" LED is ON");
      pub(pubHisLed, "led", "on");
    } else if (message == "off") {
      digitalWrite(LED_PIN, LOW);
      Serial.println("LED is OFF");
      pub(pubHisLed, "led", "off");
    }
  }

  if (String(topic) == subTopicFan) {
    if (message == "on") {
      Serial.println(message);
      digitalWrite(FAN_PIN, HIGH);
      Serial.println(" FAN is ON");
      pub(pubHisFan, "fan", "on");
    } else if (message == "off") {
      digitalWrite(FAN_PIN, LOW);
      Serial.println("FAN is OFF");
      pub(pubHisFan, "fan", "off");
    }
  }

  if (String(topic) == subTopicAC) {
    if (message == "on") {
      digitalWrite(AC_PIN, HIGH);
      Serial.println(" CON is ON");
      pub(pubHisAC, "con", "on");
    } else if (message == "off") {
      digitalWrite(AC_PIN, LOW);
      Serial.println("CON is OFF");
      pub(pubHisAC, "con", "off");
    }
  }  
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("tai")) {
      Serial.println("connected");
      client.subscribe(subTopicFan);
      client.subscribe(subTopicLed);
      client.subscribe(subTopicAC);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
      yield(); 
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();

  pinMode(LED_PIN, OUTPUT); 
  pinMode(AC_PIN, OUTPUT); 
  pinMode(FAN_PIN, OUTPUT); 

  pinMode(B5_PIN, OUTPUT); 

  digitalWrite(LED_PIN, LOW);
  digitalWrite(AC_PIN, LOW);
  digitalWrite(FAN_PIN, LOW);
  
  digitalWrite(B5_PIN, LOW);

  client.setServer(mqtt_server, 1883);  
  client.setCallback(callback);         
  dht.begin();
}

unsigned long lastDHTReadTime = 0;   
const long interval = 2000;

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();  

  unsigned long currentMillis = millis();

  if (currentMillis - lastDHTReadTime >= interval) {
    lastDHTReadTime = currentMillis;  

    float h = dht.readHumidity();
    float t = dht.readTemperature();

    int lightValue = analogRead(AO_PIN);
    if (isnan(h) || isnan(t)) {
      Serial.println(F("Failed to read from DHT sensor!"));
      return;
    }

    if(isnan(lightValue)) {
      Serial.println(F("Failed to read from Light sensor!"));
    }

    lightValue = 1000 - lightValue;
  
    //pub
    StaticJsonDocument<200> doc;
    doc["type"] = "data";
    doc["tem"] = t;
    doc["hum"] = h;
    doc["lig"] = lightValue;

    int randomValue = random(0, 101);
    doc["ws"] = randomValue;
    if (randomValue <= 60) {
      digitalWrite(B5_PIN, LOW);   // Nếu giá trị <= 60, tắt đèn LED
    } else {
      digitalWrite(B5_PIN, HIGH);  // Nếu giá trị > 60, bật đèn LED
    }

    char jsonBuffer[512];
    serializeJson(doc, jsonBuffer);
    client.publish(pubSensorTopic, jsonBuffer);

  }
}

void pub(const char* topic,const char* hw, const char* act) {
    StaticJsonDocument<200> doc;
    doc["type"] = "hw";
    doc["hw"] = hw;
    doc["act"] = act;

    char jsonBuffer[512];
    serializeJson(doc, jsonBuffer);
    client.publish(topic, jsonBuffer);
}