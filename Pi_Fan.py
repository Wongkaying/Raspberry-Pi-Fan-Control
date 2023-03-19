import subprocess
import time
import os
import logging

from datetime import datetime
from gpiozero import OutputDevice, CPUTemperature

GET_COOL = 45  # (degrees Celsius) Fan kicks on at this temperature.
BE_COOL = 40  # (degress Celsius) Fan shuts off at this temperature.
SLEEP_INTERVAL = 5  # (seconds) How often we check the core temperature.
GPIO_PIN = 17  # Which GPIO pin you're using to control the fan.
LOGS = "" # Path where the log file should be stored. Examlple: home/pi/logs/examplelog.log -- Leave empty to disgart ""

# Get current time
def get_time():
    return str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# Function to write the logs based on the log level
def write_log(logtext, level=0):
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
    cpu_temp = str(CPUTemperature(min_temp=30, max_temp=90).temperature)
    output = round(float(cpu_temp), 2)
    try:
        return output
    except(IndexError, ValueError):
        write_log('Could not parse any temperature output', 3)
        raise RuntimeError('Could not parse any temperature output')

# Just a simple printout at startup
print("Wongkaying's Pi_Fan started")
write_log("Wongkaying's Pi_Fan started", 0)

# Fan control
if __name__ == '__main__':
    # Secure
    if BE_COOL >= GET_COOL:
        raise RuntimeError('BE_COOL must be less than GET_COOL')
    fan = OutputDevice(GPIO_PIN)
    while True:
        temp = get_temp()
        temp_str = str(temp)
        # Start the fan if the temperature has reached the limit and the fan
        # isn't already running.
        # NOTE: `fan.value` returns 1 for "on" and 0 for "off"
        if temp > GET_COOL and not fan.value:
            write_log("Fan kicks on at " + temp_str, 1)
            fan.on()

        # Stop the fan if the fan is running and the temperature has dropped
        # to 10 degrees below the limit.
        elif fan.value and temp < BE_COOL:
            write_log("Fan kicks off at " + temp_str, 1)
            fan.off()
        time.sleep(SLEEP_INTERVAL)
