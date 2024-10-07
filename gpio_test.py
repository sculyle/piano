import RPi.GPIO as GPIO
import time

# Setup
GPIO.setwarnings(False)  # Disable warnings
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
pin = 4  # Replace with your desired GPIO pin number
GPIO.setup(pin, GPIO.OUT)  # Set the pin as an output

# Toggle the pin every 1 second
try:
    while True:
        time.sleep(1)
        GPIO.output(pin, GPIO.HIGH)  # Turn the pin on
        print("on")
        time.sleep(1)                # Wait for 1 second
        GPIO.output(pin, GPIO.LOW)   # Turn the pin off
        time.sleep(1)                # Wait for 1 second
        print("off")
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()  # Reset the GPIO pin state
