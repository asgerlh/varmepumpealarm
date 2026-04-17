import network
import machine
from utime import sleep
from config import wifi, pin

led = machine.Pin(pin.LED, machine.Pin.OUT)

wlan = network.WLAN(network.WLAN.IF_STA)
wlan.active(True)

print('Connecting to WiFi...')
led.value(pin.LED_ON)

wlan.connect(wifi.ssid, wifi.password)
while not wlan.isconnected():
    sleep(1)
    led.toggle()  # Blink LED while trying to connect
led.value(pin.LED_OFF)

print('Connected to WiFi:', wlan.ifconfig()[0])

