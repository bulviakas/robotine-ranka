#include <FastLED.h>

#define ROBOT_NUM_LEDS 40
#define TABLE_NUM_LEDS 187 // All zone LED number
#define TEST_NUM_LEDS 71
#define FRIDGE_NUM_LEDS 60
#define SCAN_NUM_LEDS 56
#define BRIGHTNESS 200
#define TABLE_PIN 11
#define ROBOT_PIN 5

CRGB tables[TABLE_NUM_LEDS];
CRGB robot[ROBOT_NUM_LEDS];

String command = "";
bool errorMode = false;
bool blinkState = false;
unsigned long lastBlink = 0;
const int blinkInterval = 500;

void setup() {
  Serial.begin(115200);
  delay(1000);

  FastLED.addLeds<WS2811, TABLE_PIN, BRG>(tables, TABLE_NUM_LEDS);
  FastLED.addLeds<WS2811, ROBOT_PIN, BRG>(robot, ROBOT_NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);

  resetToIdle();

  Serial.println("READY");
}

void loop() {
  readSerial();
  if (errorMode) {
    handleErrorBlink();
  }
}

void setRobotColor(CRGB color) {
  for (int i = 0; i < ROBOT_NUM_LEDS; i++) robot[i] = color;
}

void setZoneColor(String zone, CRGB color) {
  int start, end;

    if (zone =="TEST") { start = 0; end = TEST_NUM_LEDS; }
    else if (zone == "FRIDGE") { start = TEST_NUM_LEDS; end = FRIDGE_NUM_LEDS + start; }
    else if (zone == "SCAN") { start = FRIDGE_NUM_LEDS + TEST_NUM_LEDS; end = SCAN_NUM_LEDS + start; }
    else { start = 0; end = TABLE_NUM_LEDS; }

  for (int i = start; i < end; i++) tables[i] = color;
}

void readSerial() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (command.length() > 0) {
        handleCommand(command);
        command = "";
      }
    } else {
      command += c;
    }
  }
}

void resetToIdle() {
  setZoneColor("FRIDGE", CRGB(0, 255, 0));
  setZoneColor("TEST", CRGB(180, 0, 255));
  setZoneColor("SCAN", CRGB(255, 0, 0));
  setRobotColor(CRGB(40, 40, 40));
  FastLED.show();
}

void handleCommand(String cmd) {
  cmd.trim();

  if (cmd == "ERROR") {
    errorMode = true;
    return;
  }

  errorMode = false;

  if (cmd == "IDLE") {
    setZoneColor("FRIDGE", CRGB(0, 255, 0));
    setZoneColor("TEST", CRGB(180, 0, 255));
    setZoneColor("SCAN", CRGB(255, 0, 0));
    setRobotColor(CRGB(40, 40, 40));
  }
  else if (cmd == "FRIDGE") {
    setZoneColor("FRIDGE", CRGB(0, 255, 0));
    setZoneColor("TEST", CRGB(255, 0, 255));
    setZoneColor("SCAN", CRGB(255, 0, 0));
    setRobotColor(CRGB::Blue);
  }
  else if (cmd == "STRONG SHAKE") {
    setRobotColor(CRGB(180, 40, 0));     // dark reddish-orange
  }
  else if (cmd == "WEAK SHAKE") {
    setRobotColor(CRGB(60, 40, 0));
  }
  else if (cmd == "FINAL") {
    setZoneColor("FRIDGE", CRGB(0, 255, 0));
    setZoneColor("TEST", CRGB(180, 0, 255));
    setZoneColor("SCAN", CRGB(0, 0, 255));
    setRobotColor(CRGB::Green);
  }
  else if (cmd == "RESET") {
    resetToIdle();
    Serial.println("OK");
    return;
  }
  else {
    Serial.print("UNKNOWN: ");
    Serial.println(cmd);
    return;
  }

  FastLED.show();
  Serial.println("OK");
}

void handleErrorBlink() {
  unsigned long now = millis();
  if (now - lastBlink > blinkInterval) {
    lastBlink = now;
    blinkState = !blinkState;
    CRGB color = blinkState ? CRGB::Red : CRGB::Black;
    setZoneColor("FRIDGE", color);
    setZoneColor("TEST", color);
    setZoneColor("SCAN", color);
    setRobotColor(color);
    FastLED.show();
  }
}