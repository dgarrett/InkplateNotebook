import network
import time
from inkplate6 import Inkplate
import urequests
import machine
import esp32
from machine import Pin
from time import sleep

from secrets import ssid, password

SIMULATE_NET = True
notes_url = "https://raw.githubusercontent.com/dgarrett/InkplateNotebook/master/notebook.txt"

# More info here: https://docs.micropython.org/en/latest/esp8266/tutorial/network_basics.html
def do_connect():
    if SIMULATE_NET:
        return

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("connecting to network...")
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print("network config:", sta_if.ifconfig())


# More info here: https://docs.micropython.org/en/latest/esp8266/tutorial/network_tcp.html
def http_get(url) -> str:
    if SIMULATE_NET:
        return 'Note one\ncontents of note one\nthree\nmore\nlines\n---\nNote two\nand some contents for note two\ntwo more\nlines\n---\nNote three'
    else:
        res = urequests.get(url)
        return res.text

def sleep_until_touch():
    # Try:
    # from inkplate6 import _Inkplate
    # _Inkplate._mcp23017...

    # TODO extend mcp23017.py to allow the equivalent of:
    # // Setup mcp interrupts
    # display.pinModeInternal(MCP23017_INT_ADDR, display.mcpRegsInt, touchPadPin, INPUT);
    # display.setIntOutput(1, false, false, HIGH);
    # display.setIntPin(touchPadPin, RISING);
    wake1 = Pin(34, mode = Pin.IN)

    # // Go to sleep for TIME_TO_SLEEP seconds, but also enable wake up from gpio 34
    # // Gpio 34 is where the mcp interrupt is connected, check
    # // https://github.com/e-radionicacom/Inkplate-6-hardware/blob/master/Schematics%2C%20Gerber%2C%20BOM/Inkplate6%20Schematics.pdf
    # // for more detail
    #level parameter can be: esp32.WAKEUP_ANY_HIGH or esp32.WAKEUP_ALL_LOW
    esp32.wake_on_ext0(pin = wake1, level = esp32.WAKEUP_ANY_HIGH)

    #your main code goes here to perform a task

    print('Im awake. Going to sleep in 10 seconds')
    sleep(10)
    print('Going to sleep now')
    machine.deepsleep()

def print_lines(display: Inkplate, text: str, size = 3):
    display.clearDisplay()
    display.setTextSize(size)
    cnt = 0
    for x in text.split("\n"):
        if cnt == 0:
            display.setTextSize(size * 2)
        display.printText(
            10, 10 + cnt, x.upper()
        )
        if cnt == 0:
            display.setTextSize(size)
            cnt += 10 * size * 2
        else:
            cnt += 10 * size

def split_notes(raw: str) -> list(str):
    return str.split('\n---\n')

def handle_interrupt(pin):
    print('interrupt')

if __name__ == '__main__':
    print('wake reason: ', machine.wake_reason())

    display = Inkplate(Inkplate.INKPLATE_1BIT)
    display.begin()

    # display.TOUCH1.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

    # Calling functions defined above
    do_connect()
    response = http_get(notes_url)

    notes = response.split('\n---\n')
    current_note = 0
    print_lines(display, notes[current_note])

    # Display image from buffer
    display.display()

    prev1 = False
    prev3 = False
    (prev_touch1, prev_touch2, prev_touch3) = (False, False, False)
    while True:
        update = False
        (curr_touch1, curr_touch2, curr_touch3) = (display.TOUCH1(), display.TOUCH2(), display.TOUCH3())
        if curr_touch1 and not prev_touch1:
            print('TOUCH1')
            current_note = current_note - 1 if current_note > 0 else current_note
            update = True
        elif curr_touch3 and not prev_touch3:
            print('TOUCH3')
            current_note = current_note + 1 if current_note < len(notes) - 1 else current_note
            update = True

        if update:
            print_lines(display, notes[current_note])
            display.partialUpdate()

        (prev_touch1, prev_touch2, prev_touch3) = (curr_touch1, curr_touch2, curr_touch3)

