gotmilk
=======

Hackday project for checking milk level in the fridge using a Raspberry Pi and force sensitive resistor.

The Python code posts to a specific room in HipChat - so ensure that you have a `.gotmilk` file in the directory or in /etc/gotmilk that has this format:

    [HipChat]
    token=<your HipChat API token>
    roomid=<your HipChat room id>

    [GotMilk]
    delay=2



