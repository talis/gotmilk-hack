gotmilk
=======

Hackday project for checking milk level in the fridge using a Raspberry Pi and force sensitive resistor.

The Python code posts to a specific room in HipChat - so ensure that you have a `.gotmilk` file in the directory or in /etc/gotmilk that has this format:

    [HipChat]
    token=<your HipChat API token>
    roomid=<your HipChat room id>

    [GotMilk]
    delay=2

Writes the last status of the milk to a file `\milklevel.txt` so that it is possible to ssh into the Pi and see that the Milkmaid is running and monitoring.

Example contents of the file is as follows:

    2014-06-05 08:01,650,2.1,Milk running low - please buy more

This is CSV data containing:

- Last read date/time
- Resistor value - higher values mean LESS pressure (as in less milk)
- Voltage - will vary depending on the resistence in the pad (will be higher with less pressure)
