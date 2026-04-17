from config import pin
from send_mail import send_mail
import machine
import time

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

print('Init complete. Monitoring relay state...')
while True:
    if relay_state_changed:
        relay_state_changed = False

        if relay_state == 0:
            print('Relay activated! Sending alert email...')
            led.value(pin.LED_ON)
            send_mail()
        else:
            print('Relay deactivated. System normal.')
    else:
        if relay_state == 0:
            led.toggle()
        else:
            led.value(pin.LED_OFF)
        time.sleep_ms(500)
