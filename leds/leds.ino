#include <FastLED.h>

#define NUM_LEDS 20
#define BRIGHTNESS 200
#define FRIDGE_PIN 6
#define TEST_PIN 7
#define FINAL_PIN 8
#define ROBOT_PIN 9

CRGB fridge[NUM_LEDS];
CRGB test_strip[NUM_LEDS];
CRGB final_strip[NUM_LEDS];
CRGB robot[NUM_LEDS];

String command = "";
bool errorMode = false;
bool blinkState = false;
unsigned long lastBlink = 0;
const int blinkInterval = 500;

void setup() {
  Serial.begin(115200);
  delay(1000);

  FastLED.addLeds<WS2811, FRIDGE_PIN, BRG>(fridge, NUM_LEDS);
  FastLED.addLeds<WS2811, TEST_PIN, BRG>(test_strip, NUM_LEDS);
  FastLED.addLeds<WS2811, FINAL_PIN, BRG>(final_strip, NUM_LEDS);
  FastLED.addLeds<WS2811, ROBOT_PIN, BRG>(robot, NUM_LEDS);
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
  setStrip(fridge, CRGB::Blue);
  setStrip(test_strip, CRGB::Yellow);
  setStrip(final_strip, CRGB::Red);
  setStrip(robot, CRGB(40, 40, 40));
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
    setStrip(fridge, CRGB::Blue);
    setStrip(test_strip, CRGB::Yellow);
    setStrip(final_strip, CRGB::Red);
    setStrip(robot, CRGB(40, 40, 40));
  }
  else if (cmd == "FRIDGE") {
    setStrip(fridge, CRGB::Blue);
    setStrip(test_strip, CRGB::Yellow);
    setStrip(final_strip, CRGB::Red);
    setStrip(robot, CRGB::Blue);
  }
  else if (cmd == "STRONG SHAKE") {
    // setStrip(test_strip, CRGB::Yellow);    // return test to yellow
    setStrip(robot, CRGB(180, 40, 0));     // dark reddish-orange
  }
  else if (cmd == "WEAK SHAKE") {
    setStrip(robot, CRGB(60, 40, 0));
  }
  else if (cmd == "FINAL") {
    setStrip(fridge, CRGB::Blue);
    setStrip(test_strip, CRGB::Yellow);
    setStrip(final_strip, CRGB::Green);
    setStrip(robot, CRGB::Green);
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
    setStrip(fridge, color);
    setStrip(test_strip, color);
    setStrip(final_strip, color);
    setStrip(robot, color);
    FastLED.show();
  }
}

void setStrip(CRGB strip[], CRGB color) {
  for (int i = 0; i < NUM_LEDS; i++) strip[i] = color;
}