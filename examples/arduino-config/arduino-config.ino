#include "../../cpp/core.hpp"
using namespace embedded_env;
// Demo values only. Never embed production credentials in firmware.
const char* baudSetting="115200";
const char* endpoint="https://example.org";
const char* enabled="true";
bool configurationOk=false;
void setup(){
 pinMode(LED_BUILTIN,OUTPUT);digitalWrite(LED_BUILTIN,LOW);
 Serial.begin(115200);
 configurationOk=check(baudSetting,Integer)==Valid &&
                 check(endpoint,HttpUrl)==Valid &&
                 check(enabled,Boolean)==Valid;
 // Fail closed: do not start networking or actuators on invalid settings.
 Serial.println(configurationOk?F("Configuration valid (format only)"):F("Configuration rejected"));
}
void loop(){digitalWrite(LED_BUILTIN,configurationOk?HIGH:LOW);delay(500);}
