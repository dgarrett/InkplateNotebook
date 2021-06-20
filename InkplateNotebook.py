import network
import time
from inkplate6 import Inkplate
import urequests
import machine
import esp32
from machine import Pin
from time import sleep

from secrets import ssid, password

# More info here: https://docs.micropython.org/en/latest/esp8266/tutorial/network_basics.html
def do_connect():
    import network

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("connecting to network...")
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print("network config:", sta_if.ifconfig())


# More info here: https://docs.micropython.org/en/latest/esp8266/tutorial/network_tcp.html
def http_get(url):
    res = urequests.get(url)
    return res.text
    import socket

    res = ""
    _, _, host, path = url.split("/", 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes("GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n" % (path, host), "utf8"))
    while True:
        data = s.recv(100)
        if data:
            res += str(data, "utf8")
        else:
            break
    s.close()

    return res

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


print('wake reason: ', machine.wake_reason())
# Calling functions defined above
do_connect()
response = http_get("http://micropython.org/ks/test.html")

# Initialise our Inkplate object
display = Inkplate(Inkplate.INKPLATE_1BIT)
display.begin()

# Print response in lines
cnt = 0
for x in response.split("\n"):
    display.printText(
        10, 10 + cnt, x.upper()
    )  # Default font has only upper case letters
    cnt += 10

# Display image from buffer
display.display()
