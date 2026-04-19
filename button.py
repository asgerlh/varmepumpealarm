import machine
import time

class Button:
    def __init__(self, pin_id, debounce_ms=50):
        # Using PULL_UP: 1 = Released, 0 = Pressed
        self.pin = machine.Pin(pin_id, machine.Pin.IN, machine.Pin.PULL_UP)
        self.debounce_ms = debounce_ms
        self.last_time = time.ticks_ms()
        
        # Initial state is based on the current pin value
        self.state = self.pin.value()
        # This flag "sticks" to True once a press is detected, and will be reset on the next get_status() call
        # Initialize it based on the initial state of the button
        self.was_pressed = self.state == 0
        
        self.pin.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=self._isr)
        
    def _isr(self, pin):
        current_time = time.ticks_ms()
        
        # Debounce check
        if time.ticks_diff(current_time, self.last_time) > self.debounce_ms:
            new_state = pin.value()
            
            if new_state != self.state:
                self.state = new_state
                # If the new stable state is 0 (Pressed), set our sticky flag
                if new_state == 0:
                    self.was_pressed = True
                    
            self.last_time = current_time

    def get_status(self):
        """
        Returns (was_pressed, is_pressed):
        - was_pressed: True if a press occurred since the last call.
        - is_pressed: True if the button is down RIGHT NOW.
        """
        irq_state = machine.disable_irq()
        
        # Grab the "sticky" flag and immediately reset it
        was_pressed = self.was_pressed
        self.was_pressed = False
        
        # Check current state (0 is pressed/down)
        is_pressed = (self.state == 0)
        
        machine.enable_irq(irq_state)
        
        return was_pressed, is_pressed