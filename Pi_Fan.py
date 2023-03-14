import subprocess
import time
import os
import logging

from datetime import datetime
from gpiozero import OutputDevice

GET_COOL = 45  # (degrees Celsius) Fan kicks on at this temperature.
BE_COOL = 40  # (degress Celsius) Fan shuts off at this temperature.
SLEEP_INTERVAL = 5  # (seconds) How often we check the core temperature.
GPIO_PIN = 18  # Which GPIO pin you're using to control the fan.
LOGS = "" # Path where the log file should be stored. Examlple: home/pi/logs/examplelog.log -- Leave empty to disgart ""

# Get current time
def get_time():
    return str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# Function to write the logs based on the log level
def Write_Log(logtext, level=0):
    if LOGS == "":
        return
    else:
        try:
            logging.basicConfig(filename=LOGS, level=logging.DEBUG, format='')

            if level == 0:
                text = '[Info] - ' + get_time() + ' - ' + logtext
                logging.debug(text)
            elif level == 1:
                text = '[SUCCESS] - ' + get_time() + ' - ' + logtext
                logging.debug(text)
            elif level == 2:
                text = '[WARNING] - ' + get_time() + ' - ' + logtext
                logging.debug(text)
            elif level == 3:
                text = '[ERROR] - ' + get_time() + ' - ' + logtext
                logging.debug(text)
        except (FileNotFoundError):
                print("File path not found")
                return

# Get temperature
def get_temp():
    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
    temp_str = output.stdout.decode()
    try:
        return float(temp_str.split('=')[1].split('\'')[0])
    except (IndexError, ValueError):
        raise RuntimeError('Could not parse temperature output.')

# Jst a simple printout at startup
print("Wongkaying's Pi_Fan started")
Write_Log("Wongkaying's Pi_Fan started", 0)

# Fan control
if __name__ == '__main__':
    # Secure
    if BE_COOL >= GET_COOL:
        raise RuntimeError('BE_COOL must be less than GET_COOL')
    fan = OutputDevice(GPIO_PIN)
    while True:
        temp = get_temp()
        # Start the fan if the temperature has reached the limit and the fan
        # isn't already running.
        # NOTE: `fan.value` returns 1 for "on" and 0 for "off"
        if temp > GET_COOL and not fan.value:
            Write_Log("Fan kicks on", 1)
            fan.on()

        # Stop the fan if the fan is running and the temperature has dropped
        # to 10 degrees below the limit.
        elif fan.value and temp < BE_COOL:
            Write_Log("Fan kicks off")
            fan.off()
        time.sleep(SLEEP_INTERVAL)
