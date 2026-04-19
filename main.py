import machine
import time
import micropython

from wifi import connect_to_wifi
from button import Button
from config import pin
from send_mail import send_mail

# Allocate emergency exception buffer for handling exceptions in interrupt context
micropython.alloc_emergency_exception_buf(100)

wlan = connect_to_wifi()

# Initialize LED and relay pins
led = machine.Pin(pin.LED, machine.Pin.OUT)
relay = Button(pin.RELAY)

print("Starting watchdog in 2 seconds. Press Ctrl+C to stop.")
time.sleep(2)
wdt = machine.WDT(timeout=10000)  # Watchdog timer with a 10-second timeout

def main_loop():
    while True:
        if wlan.isconnected():
            wdt.feed()  # Feed the watchdog timer

        was_pressed, is_pressed = relay.get_status()

        if was_pressed:
            led.value(pin.LED_ON)
            send_mail()
        else:
            if is_pressed:
                led.toggle()
            else:
                led.value(pin.LED_OFF)
            time.sleep_ms(500)

print("Device initialized. Monitoring relay state...")
main_loop()
