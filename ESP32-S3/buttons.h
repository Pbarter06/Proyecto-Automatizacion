#pragma once

#include <Arduino.h>

struct BotonMQTT {
  uint8_t pin;
  const char* topic;
  const char* payload;
  bool lastReading;
  bool stableState;
  unsigned long lastDebounceTime;
};