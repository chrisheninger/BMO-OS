import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering

# Define the pin numbers
buttons = {
    17: "b1 (up)",
    27: "b2 (right)",
    22: "b3 (down)",
    23: "b4 (left)",
    24: "b5 (triangle)",
    25: "b6 (small circle)",
    26: "b7 (large circle)"
}

# Function to generate callback functions


def make_callback(name):
    return lambda pin: print(f"{name} was pressed!")


# Setup the pins and attach handlers
for pin, name in buttons.items():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(
        pin, GPIO.FALLING, callback=make_callback(name), bouncetime=100)

# Loop forever
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
