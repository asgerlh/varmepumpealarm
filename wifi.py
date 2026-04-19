import network
import machine
from time import sleep_ms
from config import wifi, pin

def connect_to_wifi():
    led = machine.Pin(pin.LED, machine.Pin.OUT)
    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)

    if wlan.status() == network.STAT_GOT_IP:
        print("Already connected to Wi-Fi.")
        return wlan
    
    if wlan.status() == network.STAT_CONNECTING:
        print("Already trying to connect to Wi-Fi. Probably from a previous boot.")
        wlan.disconnect()  # Disconnect to reset the connection state

    print(f"Connecting to Wi-Fi '{wifi.ssid}'...")
    wlan.connect(wifi.ssid, wifi.password)

    # Wait for connection with a simple LED blink pattern
    for n in range(20):
        if wlan.isconnected():
            print("Wi-Fi connected successfully!")
            break
        for _ in range(3):
            led.value(pin.LED_ON)
            sleep_ms(100)
            led.value(pin.LED_OFF)
            sleep_ms(200)
        sleep_ms(500)

    if not wlan.isconnected():
        print("Failed to connect to Wi-Fi after multiple attempts.")
        sleep_ms(2000)
        machine.reset()  # Reset the device to try again
    
    return wlan
