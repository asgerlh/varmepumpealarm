# Varmepumpealarm

Send a mail and blink a diode if a relay is closed.

Used to monitor a heat pump for failures. The heat pump closes a relay if an error occur.

## Setup

Copy `config.example.py` to `config.py` and edit to match board pinout and mail addresses. You'll need a gmail sender address with an app password, and a recipient address.
