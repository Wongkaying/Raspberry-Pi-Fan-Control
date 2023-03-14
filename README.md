# Raspberry-Pi-Fan-Control

This script controls the fan of the Raspberry Pi based on the **gpiozero API**.
You can set the switch-on temperature and the switch-off temperature of the fan as well as the interval at which the temperature is to be queried.
Likewise, a function that writes the events to a log file can be used. -- **__Not mandatory__**

## Installation instructions

Gpiozero must be installed.
If this has not been done yet, follow the [documentation](https://gpiozero.readthedocs.io/en/stable/installing.html)

Once gpiozero is installed, the script can be used.

## Running the script

Change to the location where the Pi_Fan.py script is located
```
cd examplepath/example/.....
```
Start the script
```
python3 Pi_Fan.py
```

## Setting up

The script is executed with the default values of the Rapberry Pi after startup.
Writing the log file is disabled and can be enabled later.
Furthermore the temperatures as well as the path of the log file and the GPIO's can be changed.
```log
GET_COOL = 45  # (degrees Celsius) Fan kicks on at this temperature.
BE_COOL = 40  # (degress Celsius) Fan shuts off at this temperature.
SLEEP_INTERVAL = 5  # (seconds) How often we check the core temperature.
GPIO_PIN = 14  # Which GPIO pin you're using to control the fan.
LOGS = "" # Path where the log file should be stored. Examlple: /home/pi/logs/examplelog.log -- Leave empty to disgart ""
```
