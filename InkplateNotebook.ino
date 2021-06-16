#ifndef ARDUINO_ESP32_DEV
#error "Wrong board selection for this example, please select Inkplate 6 in the boards menu."
#endif

#include <Inkplate.h>
#include <HTTPClient.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <vector>

#include "NoteManager.h"

#include "secrets.h"

#define TEST_NO_NETWORK 1

Inkplate display(INKPLATE_1BIT); // Create an object on Inkplate library and also set library into 1 Bit mode (BW)
NoteManager notes(display);

char notes_url[] = "https://raw.githubusercontent.com/dgarrett/InkplateNotebook/master/notebook.txt";

void setup()
{
    display.begin();                                  // Init Inkplate library (you should call this function ONLY ONCE)
    display.clearDisplay();                           // Clear frame buffer of display
    display.display();                                // Put clear image on display
    display.setTextSize(2);                           // Set text scaling to two (text will be two times bigger)
    display.setCursor(0, 0);                          // Set print position
    display.setTextColor(BLACK, WHITE);               // Set text color to black and background color to white

#if TEST_NO_NETWORK
    notes.DownloadNotes("");
#else
    notes.DownloadNotes(notes_url);
#endif
}

void loop()
{
    display.print(" Touch: ");
    display.print(display.readTouchpad(PAD1));
    display.print(display.readTouchpad(PAD2));
    display.print(display.readTouchpad(PAD3));
    display.partialUpdate();
    delay(1000);
}
