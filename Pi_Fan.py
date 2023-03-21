import time
import os

from datetime import datetime
from gpiozero import OutputDevice, CPUTemperature

GET_COOL = 45  # (degrees Celsius) Fan kicks on at this temperature.
BE_COOL = 40  # (degrees Celsius) Fan shuts off at this temperature.
SLEEP_INTERVAL = 5  # (seconds) How often we check the core temperature.
GPIO_PIN = 17  # Which GPIO pin you're using to control the fan.
LOGS = ""  # Path where the log file should be stored. Example: home/pi/logs/example_log.log -- Leave empty to ignore the log ""
TEMP_LOGS = ""  # Path where the temperature log file should be stored. Example: home/pi/logs/example_temp_log.log -- Leave empty to ignore the log ""


# Get current time
def get_time(time_format):
    if time_format == "short":
        return str(datetime.now().strftime('%Y-%m-%d'))
    else:
        return str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def get_avg():
    avg = 86400 / SLEEP_INTERVAL
    return avg


# Function to write the logs based on the log level
def write_log(log_text, level=0):
    if LOGS == "":
        return
    else:
        try:
            f = open(LOGS, "a")

            if level == 0:
                text = '[Info] - ' + get_time("") + ' - ' + log_text
                f.write(text + '\n')
            elif level == 1:
                text = '[SUCCESS] - ' + get_time("") + ' - ' + log_text
                f.write(text + '\n')
            elif level == 2:
                text = '[WARNING] - ' + get_time("") + ' - ' + log_text
                f.write(text + '\n')
            elif level == 3:
                text = '[ERROR] - ' + get_time("") + ' - ' + log_text
                f.write(text + '\n')
        except FileNotFoundError:
            print("LOGS path not found")
            return
    if TEMP_LOGS == "":
        return
    else:
        try:
            f = open(TEMP_LOGS, "a")

            if level == 4:
                text = '[TEMPERATURE OF THE DAY] - ' + get_time("short") + ' - ' + log_text
                f.write(text + '\n')
        except FileNotFoundError:
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

# Fan control
if __name__ == '__main__':
    temp_list = []
    # Secure - Let's check if there is really something to cool down
    if BE_COOL >= GET_COOL:
        raise RuntimeError('BE_COOL must be less than GET_COOL')
    fan = OutputDevice(GPIO_PIN)

    # Get temperatures after the desired time
    while True:
        temp = get_temp()
        temp_str = str(temp)
        # If you want to log the Average temperatures. It will continue here. Otherwise, ignore this
        if TEMP_LOGS == "":
            continue
        else:
            if len(temp_list) < get_avg():
                temp_list.append(temp)
            else:
                avg = sum(temp_list) / len(temp_list)
                write_log(str(avg).split(".")[0] + "°C", 4)
                temp_list.clear()
        # Start the fan if the temperature has reached the limit and the fan
        # aren't already running.
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
