import subprocess
import time
import os

from datetime import datetime
from gpiozero import OutputDevice, CPUTemperature

GET_COOL = 45  # (degrees Celsius) Fan kicks on at this temperature.
BE_COOL = 40  # (degress Celsius) Fan shuts off at this temperature.
SLEEP_INTERVAL = 5  # (seconds) How often we check the core temperature.
GPIO_PIN = 17  # Which GPIO pin you're using to control the fan.
LOGS = "" # Path where the log file should be stored. Examlple: home/pi/logs/example_log.log -- Leave empty to disgart ""
TEMP_LOGS = "" # Path where the temperature log file should be stored. Examlple: home/pi/logs/example_temp_log.log -- Leave empty to disgart ""

# Get current time
def get_time(formate):
    if formate == "shot":
        return str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        return str(datetime.now().strftime('%Y-%m-%d'))

# Function to write the logs based on the log level
def write_log(logtext, level=0):
    if LOGS == "":
        return
    else:
        try:
            f = open(LOGS, "a")

            if level == 0:
                text = '[Info] - ' + get_time("") + ' - ' + logtext
                f.write(text+'\n')
            elif level == 1:
                text = '[SUCCESS] - ' + get_time("") + ' - ' + logtext
                f.write(text+'\n')
            elif level == 2:
                text = '[WARNING] - ' + get_time("") + ' - ' + logtext
                f.write(text+'\n')
            elif level == 3:
                text = '[ERROR] - ' + get_time("") + ' - ' + logtext
                f.write(text+'\n')
        except (FileNotFoundError):
                print("LOGS path not found")
                return
    if TEMP_LOGS == "":
        return
    else:
        try:
            f = open(TEMP_LOGS, "a")

            if level == 4:
                text = '[TEMPERATURE OF THE DAY] - ' + get_time("short") + ' - ' + logtext
                f.write(text+'\n')
        except (FileNotFoundError):
            print("TEMP_LOGS path not found")
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

def temp_list():
    temp_list = []
    return temp_list

# Fan control
if __name__ == '__main__':
    # Secure
    if BE_COOL >= GET_COOL:
        raise RuntimeError('BE_COOL must be less than GET_COOL')
    fan = OutputDevice(GPIO_PIN)
    while True:
        temp = get_temp()
        temp_str = str(temp)
        if TEMP_LOGS == "":
            continue
        else:
            if len(temp_list) < 5:
                temp_list.append(temp)
                print(len(temp_list))
                write_log("Counter: " + str(len(temp_list)) + " with Value: " + temp_str, 4)
            else:
                avg = sum(temp_list) / len(temp_list)
                print(str(avg).split(".")[0])
                temp_list.clear()
        # Start the fan if the temperature has reached the limit and the fan
        # isn't already running.
        # NOTE: `fan.value` returns 1 for "on" and 0 for "off"
        if temp > GET_COOL and not fan.value:
            write_log("Fan kicks on at " + temp_str + "°C", 1)
            fan.on()

        # Stop the fan if the fan is running and the temperature has dropped
        # to 10 degrees below the limit.
        elif fan.value and temp < BE_COOL:
            write_log("Fan kicks off at " + temp_str + "°C", 1)
            fan.off()
        time.sleep(SLEEP_INTERVAL)
