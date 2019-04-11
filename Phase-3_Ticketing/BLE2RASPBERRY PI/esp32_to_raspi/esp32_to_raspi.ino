#include <WiFi.h>
#include <HTTPClient.h> 

const char* ssid = "hurrr";
const char* password =  "321321321";

void setup() {

  Serial.begin(115200);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }

  Serial.println("Connected to the WiFi network");

}

void loop() {

 if(WiFi.status()== WL_CONNECTED){   //Check WiFi connection status

   HTTPClient http;   

   http.begin("http://192.168.43.156:8090/post");
   http.addHeader("Content-Type", "text/plain");             

   int httpResponseCode = http.POST("ABCD");   //Send the actual POST request

   if(httpResponseCode>0){

    Serial.println("SETN!");

   }else{

    Serial.println("Error on sending POST");
    
   }

   http.end();  //Free resources

 }else{

    Serial.println("Error in WiFi connection");   

 }

  delay(5000);  //Send a request every 10 seconds

}
