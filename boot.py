import network
import machine
from time import sleep_ms
from config import wifi, pin

led = machine.Pin(pin.LED, machine.Pin.OUT)

wlan = network.WLAN(network.WLAN.IF_STA)
wlan.active(True)

wlan.connect(wifi.ssid, wifi.password)
while not wlan.isconnected():
    for _ in range(3):
        led.value(pin.LED_ON)
        sleep_ms(100)
        led.value(pin.LED_OFF)
        sleep_ms(200)
    sleep_ms(500)
