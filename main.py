import machine
import time
import micropython

from config import pin
from send_mail import send_mail

# Allocate emergency exception buffer for handling exceptions in interrupt context
micropython.alloc_emergency_exception_buf(100)

# Initialize LED and relay pins
led = machine.Pin(pin.LED, machine.Pin.OUT)
relay = machine.Pin(pin.RELAY, machine.Pin.IN, machine.Pin.PULL_UP)

# Read initial state of the relay and set up a flag to track state changes
# NOTE: these variables are accessed in both the main loop and the interrupt handler,
# so they must be declared as global and protected by critical sections if necessary to avoid race conditions.
relay_state = relay.value()
relay_state_changed = False

def relay_handler(relay):
    global relay_state, relay_state_changed
    relay_state = relay.value()
    relay_state_changed = True

relay.irq(handler=relay_handler,
          trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)

# Helper function to check if the relay state has changed, used in the main loop to avoid race conditions.
def read_relay_state_changed():
    global relay_state_changed, relay_state
    irq_state = machine.disable_irq()
    if relay_state_changed:
        relay_state_changed = False
        changed = True
    else:
        changed = False
    new_relay_state = relay_state
    machine.enable_irq(irq_state)
    return changed, new_relay_state

print('Init complete. Monitoring relay state...')
while True:
    changed, new_relay_state = read_relay_state_changed()
    if changed:
        if new_relay_state == 0:
            print('Relay activated! Sending alert email...')
            led.value(pin.LED_ON)
            send_mail()
        else:
            print('Relay deactivated. System normal.')
    else:
        if new_relay_state == 0:
            led.toggle()
        else:
            led.value(pin.LED_OFF)
        time.sleep_ms(500)
