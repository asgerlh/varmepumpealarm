from config import pin
from send_mail import send_mail
import machine
from utime import sleep

led = machine.Pin(pin.LED, machine.Pin.OUT)

relay = machine.Pin(pin.RELAY, machine.Pin.IN, machine.Pin.PULL_UP)

relay_state = relay.value()  # Read initial state of the relay
relay_state_changed = False

def relay_handler(relay):
    global relay_state, relay_state_changed
    relay_state = relay.value()
    relay_state_changed = True

relay.irq(handler=relay_handler,
          trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)

while True:
    if relay_state_changed:
        relay_state_changed = False

        if relay_state == 0:  # Assuming active low relay
            led.value(pin.LED_ON)
            send_mail()
    else:
        if relay_state == 0:
            led.value(pin.LED_ON)
            sleep(0.5)
            led.value(pin.LED_OFF)
            sleep(0.5)
        else:
            led.value(pin.LED_OFF)
            sleep(0.5)
