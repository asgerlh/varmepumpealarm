import machine
import time
import micropython

from button import Button
from config import pin
from send_mail import send_mail

# Allocate emergency exception buffer for handling exceptions in interrupt context
micropython.alloc_emergency_exception_buf(100)

# Initialize LED and relay pins
led = machine.Pin(pin.LED, machine.Pin.OUT)
relay = Button(pin.RELAY)

while True:
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
