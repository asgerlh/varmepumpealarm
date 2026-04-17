# Varmepumpealarm

Send a mail and blink a diode if a relay is closed.

Used to monitor a heat pump for failures. The heat pump closes a relay if an error occur.

## Setup

Flash an esp32 with micropython.

Copy `config.example.py` to `config.py` and edit to match board pinout and mail addresses. You'll need a gmail sender address with an app password, and a recipient address.

Upload all `.py` files to the esp32.

## Hardware

I used an ESP32-C3 super mini, but any esp32 should work.

Also a LED and a series resistor is needed.
