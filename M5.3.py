#include "M5StickCPlus.h"
#include <PubSubClient.h>
#include <WiFi.h>

// Update these with values suitable for your network.
const char* ssid = "";
const char* password = "";
const char* mqtt_server = "test.mosquitto.org";

WiFiClient espClient;
PubSubClient * client;

unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (500)
char msg[MSG_BUFFER_SIZE];
int value = 0;

// We start by connecting to a WiFi network
void setup_wifi() {
  delay(10);

  //Set text color and size
  M5.Lcd.setTextColor(TFT_BLUE);
  M5.Lcd.setTextSize(2);
  M5.Lcd.println();
  M5.Lcd.print("Connecting to ");
  M5.Lcd.println(ssid);

  //Attempt connection
  WiFi.begin(ssid, password);

//While not connected print dots
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    M5.Lcd.print(".");
  }

  randomSeed(micros());

  M5.Lcd.println("");
  M5.Lcd.println("WiFi connected");
  M5.Lcd.println("IP address: ");
  M5.Lcd.println(WiFi.localIP());

}

//Function to print messages from subscribed topic
void callback(char* topic, byte* payload, unsigned int length) {
  M5.Lcd.print("Message arrived [");
  M5.Lcd.print(topic);
  M5.Lcd.print("] ");
  for (int i = 0; i < length; i++) {
    M5.Lcd.print((char)payload[i]);
  }
}

//Function to reconnect client
void reconnect() {
  // Loop until we’re reconnected
  while (!client->connected()) {
    M5.Lcd.print("Attempting MQTT connection...");
    String clientId = "ESP8266Client - Alex-Client";
    // Attempt to connect
    if (client->connect(clientId.c_str(), "msitm2022", "msitm2022")) {
      M5.Lcd.println("connected");
      //Subscribe to topic here
      client->subscribe("testTopic2");
    } else {
      M5.Lcd.print("failed, rc = ");
      M5.Lcd.print(client->state());
      M5.Lcd.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

//Function for setup
void setup() {
  delay(500);
  M5.begin();
  delay(500);
  setup_wifi();

  client = new PubSubClient(espClient);

  client->setServer(mqtt_server, 1883);
  client->setCallback(callback);
}

void loop() {
  //Attempt reconnection if not connected
  if (!client->connected()) {
    reconnect();
  }
  client->loop();

  //If the screen is filled up, clear the screen
  int Y = M5.Lcd.getCursorY();
  if (Y > 223){  //224 Max Y
    M5.Lcd.fillScreen(BLACK);
    M5.Lcd.setCursor(0, 0);
    M5.Lcd.println("Waiting for messages\n");
  }

  // Read the press state of the key.
  M5.update();  

  // If the button A is pressed, publish to topic
  if (M5.BtnA.wasReleased()) { 
        snprintf (msg, MSG_BUFFER_SIZE, "Button A from Alex\n");
        client->publish("testTopic3", msg);
    } 
  // If the button B is pressed, publish to topic  
  else if (M5.BtnB.wasReleased()) {  
        snprintf (msg, MSG_BUFFER_SIZE, "Button B from Alex\n");
        client->publish("testTopic3", msg);
    } 
 }