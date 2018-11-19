// LIBs - BAŞLANGIÇ
#include <TinyGPS++.h>
#include <EEPROM.h>
#include <ArduinoJson.h>
// LIBs  - BİTİŞ

// SABİTLER - BAŞLANGIÇ

#define TIMEOUT 15000 
#define CRASH_TIMEOUT 30000
#define ESP8266 Serial1
#define HC05 Serial2
#define UBLOXGPS Serial3

const char SPLIT_FLAG = '|';
const char END_FLAG = '~';

const String WRITE_FLAG = "#W#";
const String READ_FLAG = "#R#";

const int GREEN_LED_PIN = 35;
const int RED_LED_PIN = 37;
const int COMMUNICATION_PIN = 39;

const int MAX_CRASH = 100;
// SABİTLER - BİTİŞ

// DEĞİŞKENLER - BAŞLANGIÇ

String ssid = "."; // Kablosuz ağ(Wi-Fi) adı.
String password = "."; // Kablosuz ağ şifresi.

String serialNo = "iot_1"; // Cihaz seri numarası
String plateNo = "34 IST 34";// Cihaz plaka numarası

/*
  Cihazın plaka numarasında bulunan boşlukların sunucuya göndeririken
  sorun çıkarmaması adına plakanın formatlanmış halini barındırır.
  
  34 IST 34 >>>> 34+IST+34
*/
String plateNoWithoutSpace = "";


/*
  < ...Key > değişkenleri, cihazın sunucuya istekte bulunurken query string' te
  kullanılacak keyleri içerir.
*/
String serialNoKey = "serial_no";
String plateNoKey = "plate_no";
String latKey = "latitude";
String lngKey = "longitude";
String velocityKey = "velocity";
String appKey = "app";
String actionKey="action";
// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

String host = "www.ktakip.com"; // Sunucu alan adı
String url = "location/add"; // url adresi
String app = "location";
String action = "create";

long startTime; // Yazılımın genelinde kullanılan "Timer" için kullanılır.

/*
   Timer aralığı, bu değer milisaniye cinsindendir.
   Yazılımda konum bilgilerinin sunucuya kaç saniyede bir gönderileceğini belirler.
*/
float interval = 4000; 

int addr = 0; // ROM' a veri yazarken kullanılan sayaç değişkeni.
int raddr = 0; // ROM' dan veri okurken kullanılan saya. değişkeni.


/*
  Cihazın GPS modülünün, Wi-Fi modülünün veya ana kartın cevap vermemesi
  durumunda gerçekleşen maksimum çökme sayısıdır. 
  Cihaz çökme ile karşılaştığında <crashTimeout> kadar bekler ve sistemi yeniden
  başlatırarak çalışmaya devam 
*/
int crashCount = 3;

TinyGPSPlus gps;

// DEĞİŞKENLER - BİTİŞ


//PROTOTYPE - BAŞLANGIÇ
boolean findKey(String data, String key);
boolean sendCommand(HardwareSerial *serialPort,String cmd, String ack, boolean _continue, boolean useLed);
void initWiFi();
void serialCommunication();
void initArduino();
void assignToVariables(int index, String data);
String prepareROMData(String params[], int length);
void writeROM(String data);
void readROM();
void bluetoothData();
String readData(HardwareSerial *serialPort);
boolean connectToHost();
void disconnectFromHost();
void sendLocationToHost(double lat, double lng);
void resetSelf();
void changeLedStatus(int status);
void terminateSelf();
//PROTOTYPE - BİTİŞ


void setup()
{
  crashCount = MAX_CRASH;

  initArduino();
  serialCommunication();
  initWiFi();
}

void loop()
{
  if(UBLOXGPS.available())
  { 
    char* gpsData = UBLOXGPS.read();
    if(gps.encode(gpsData))
    {
      if(millis() - startTime >= interval)
      {
        connectToHost(); 
        if (gps.location.isValid())
        {
          changeLedStatus(1);
          double lat = gps.location.lat();
          double lng = gps.location.lng();
          double vel = gps.speed.kmph();
          
          sendLocationToHost(lat,lng,vel);

        }
        else
          changeLedStatus(2);

        startTime = millis();
      }
    }
  }
}


boolean findKey(String data, String key)
{
  if(data.indexOf(key) > 0)
  {
    return true;
  }
  else
  {
    return false;
  }
}

boolean sendCommand(HardwareSerial *serialPort,String cmd, String ack, boolean _continue, boolean useLed)
{
    long startTime = millis();
    serialPort -> println(cmd);

    while(millis() - startTime < TIMEOUT)
    {
      if(findKey(readData(serialPort), ack))
      {
        if(useLed)
          changeLedStatus(1);
        return true;
      }
    }

  if(_continue == false)
    terminateSelf();
  
  return false;
}

void serialCommunication()
{
  while(digitalRead(COMMUNICATION_PIN) == HIGH)
  {
    String serialResponse = Serial.readString();
    serialResponse.trim();
    
    if(serialResponse == READ_FLAG)
    {
        String params[] = {
          serialNo,
          plateNo,
          ssid,
          password,
          host,
          url,
          app,
          action
        };

        String tmp = READ_FLAG;
        tmp+= prepareROMData(params, 8);
        Serial.println(tmp);
    }
    else if(serialResponse.substring(0,3) == WRITE_FLAG)
    {
        serialResponse = serialResponse.substring(3, serialResponse.length());
        writeROM(serialResponse);
        Serial.println(WRITE_FLAG);
    }
  }
}

void initWiFi()
{
  sendCommand(&ESP8266, "AT+CWQAP","OK", true, true);
  Serial.println(" *** BEGIN *** ");
  sendCommand(&ESP8266,"AT","OK", false, true);
  delay(250);
  sendCommand(&ESP8266,"AT+CWMODE=3", "OK", false, true);
  delay(250);  
  
  String cmd = "AT+CWJAP=\"" + ssid + "\",\"" + password + "\"";
  sendCommand(&ESP8266,cmd, "OK", false, true);
  delay(750);
  sendCommand(&ESP8266,"AT+CIPMUX=0", "OK", false, true);
  delay(250);
  startTime = millis();
}

void initArduino()
{
  plateNoWithoutSpace = plateNo;
  plateNoWithoutSpace.replace(' ', '+');
  Serial.begin(115200);
  ESP8266.begin(115200);
  UBLOXGPS.begin(9600);
  HC05.begin(9600);
  
  changeLedStatus(0);

  readROM();
}

void assignToVariables(int index, String data)
{
  switch(index)
  {
    case 1:
      serialNo = data;
      break;
    case 2:
      plateNo = data;
      break;
    case 3:
      ssid = data;
      break;
    case 4:
      password = data;
      break;
    case 5:
      host = data;
      break;
    case 6:
      url = data;
      break;
    case 7:
      app = data;
      break;
    case 8:
      action = data;
      break;
    default:
      break;
  }
}

String prepareROMData(String params[], int length)
{
  /*
    FORMAT:
      [ ORDER ]:
      SERIAL_NO - PLATE_NO - SSID - SSID_PASS - HOST - URL
      [ CHARS ]:
      SPLITTER CHAR -> |
      END CHAR -> ~   
      [ DATA SAMPLE ]:
      SERIAL_NO = 'sn1'
      PLATE_NO = '34 IST 34'
      SSID = 'ssid'
      SSID_PASS = 'ssid_pass'
      HOST = 'www.ktakip.com'
      URL = '/'
      -> sn1|34 IST 34|ssid|ssid_pass|www.ktakip.com|/location|~" 
  */
  String data = "";
  for(int i = 0; i < length ; i++)
  {
    data += params[i];
    data += SPLIT_FLAG;
  }

  data += END_FLAG;
  return data;
}

void writeROM(String data)
{
  addr = 0;
  for (int i = 0; i < data.length(); i++)
  {
    EEPROM.write(addr++, data[i]);
  }
}

void readROM()
{
  raddr = 0;
  int i = 0;
  while(1)
  {
    char isEndFlag = EEPROM.read(raddr);
    if(isEndFlag == END_FLAG)
      break;
    i++;
    String dataStr = "";
    while(1)
    {
      char tmpData = EEPROM.read(raddr++);
      if(tmpData == SPLIT_FLAG)
        break;
      dataStr+= tmpData;
    }
    assignToVariables(i,dataStr);
  }   
}


void bluetoothData()
{
  /*
    FORMAT -> [DATA-ID][DATA]
    ÖRNEK  -> 1ssid
              2password
              3serialNo 
                 ... 
  */
  boolean status = true;
  String data = "";
  if(HC05.available() > 0 && status)
  {
    int length = atoi(HC05.read());
    while(length > 0)
    {
      if(HC05.available() > 0)
      {
        char chr = HC05.read();
        if(chr != '\n')
          data += chr;
        else
        {
          String tmp = "";
          tmp += data[0];
          int index = tmp.toInt();
          data = data.substring(1, data.length());
          assignToVariables(index, data);
          length--;
          data = "";
        }
      }
    }

    if(length <= 0)
    {
      status = false;
      String params[] = 
      {
        ssid,
        password,
        serialNo,
        plateNo,
        host,
        url,
        app,
        action
      };
    
      writeROM(prepareROMData(params, 6));
      resetSelf();
      HC05.println("Bluetooth_OK");
    }
    
  }
}


StaticJsonBuffer<300> JSONBuffer;
String readData(HardwareSerial *serialPort)
{
  String response = "";
  while(serialPort->available() > 0)
  {
      response += serialPort -> readString();
      Serial.println(response);
  }
  
  if(response.length() > 0)
  {
    int si = response.indexOf('{');
    int li = response.lastIndexOf('}');
    if(si >= 0 && li >= 0)
    {
      String response2 = response.substring(si,li+1);
      JsonObject&  parsed = JSONBuffer.parseObject(response2);
      String result = (char *)parsed["result"];
      int digitResult = result.toInt();
      
      if(digitResult == 0)
        changeLedStatus(2);
    }
  }
  return response;
}

boolean connectToHost()
{
  bool result = sendCommand(&ESP8266, "AT+CIPSTART=\"TCP\",\""+host+"\",80","OK",true, false);
  delay(500);
  return result;
}

void disconnectFromHost()
{
  sendCommand(&ESP8266,"AT+CIPCLOSE","OK", false, true);
}

void sendLocationToHost(double lat, double lng, double vel)
{
  //DATA FORMAT
  //app&action&serial_no&plate_no&lat&lng&vel
  String data = "GET /" + url + "/?" +appKey +"=" + app + "&" +actionKey + "=" + action + "&" +serialNoKey + "=" +serialNo+ '&'
                + plateNoKey +"=" + plateNoWithoutSpace + "&" + latKey + "=" + String(lat,8) + '&' + lngKey + "=" + String(lng,8) + "&" 
                + velocityKey +"=" + vel +" HTTP/1.1\r\n";
                
  //Serial.println(data);
  data+="Host: " + host + "\r\n";
  sendCommand(&ESP8266,"AT+CIPSEND=" + String(data.length() + 2),">", false, true);
  sendCommand(&ESP8266,data,"OK",false, true);
  
  delay(100);
}



void resetSelf()
{
  initArduino();
  serialCommunication();
  initWiFi();
}

void changeLedStatus(int status)
{
  if(status == 0)
  {
    digitalWrite(GREEN_LED_PIN, LOW);
    digitalWrite(RED_LED_PIN, LOW);
  }
  else if(status == 1)
  {
    digitalWrite(GREEN_LED_PIN, HIGH);
    digitalWrite(RED_LED_PIN, LOW);
  }
  else if(status == 2)
  {
    digitalWrite(GREEN_LED_PIN, LOW);
    digitalWrite(RED_LED_PIN, HIGH);
  }
}

void terminateSelf()
{
  startTime = millis();
  long crashTime = millis();

  while(true)
  {
    long currentTime = millis();
    if(currentTime - startTime > 500)
    {
      changeLedStatus(0);
    }
    if(currentTime - startTime >= 1000)
    {
      changeLedStatus(2);
      startTime = millis();
    }

    if(crashCount > 0 && currentTime - crashTime >= CRASH_TIMEOUT)
      break;
  }

  crashCount--; 
  resetSelf();
}
