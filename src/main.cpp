#include <Arduino.h>

// Police-car LED flasher — basic example for the YD-ESP32-23 (ESP32-S3).
//
// Flashes the onboard RGB NeoPixel (GPIO 48) alternating red and blue bursts,
// mimicking a police car light bar: three quick red flashes, a short pause,
// then three quick blue flashes, repeated indefinitely.
//
// neopixelWrite(pin, red, green, blue) is provided by the Arduino-ESP32 framework.

static const uint8_t LED_PIN       = 48;
static const uint8_t BRIGHTNESS    = 20;   // 0-255, keep low to avoid eye strain
static const uint32_t FLASH_MS     = 80;   // duration of each colour burst
static const uint32_t PAUSE_MS     = 60;   // gap between bursts within a group
static const uint32_t GROUP_GAP_MS = 400;  // gap between red group and blue group

// Guard setup/loop so they are excluded when building tests with test_build_src = yes.
// Tests supply their own setup() and loop() entry points.
#ifndef UNIT_TEST

void setup() {
    // LED is driven directly; nothing to initialise.
}

void loop() {
    // --- RED side ---
    for (int i = 0; i < 3; i++) {
        neopixelWrite(LED_PIN, BRIGHTNESS, 0, 0); // red on
        delay(FLASH_MS);
        neopixelWrite(LED_PIN, 0, 0, 0);           // off
        delay(PAUSE_MS);
    }

    delay(GROUP_GAP_MS);

    // --- BLUE side ---
    for (int i = 0; i < 3; i++) {
        neopixelWrite(LED_PIN, 0, 0, BRIGHTNESS);  // blue on
        delay(FLASH_MS);
        neopixelWrite(LED_PIN, 0, 0, 0);           // off
        delay(PAUSE_MS);
    }

    delay(GROUP_GAP_MS);
}

#endif // UNIT_TEST