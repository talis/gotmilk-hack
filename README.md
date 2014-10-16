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
- Message - this is a text string message (potentially for posting to HipChat)

Messages are sent to HipChat on a specific status change only - i.e. when going from milk being okay to milk being low. Or if there was no milk and then someone bought milk.

Possible messages sent to HipChat:

- **Milk has all gone (or been left out of the fridge!)** - _This is shown if the milk has literally all gone or is too low to measure or has been left out of the fridge_
- **Milk running low - please buy more** - _This is shown if the milk level is getting low_
- **Milk level currently okay** - _This is shown if there is currently sufficient milk_
- **Milk is plentiful!** - _This is shown if there is a lot of milk left_


Notes on setting up the Pi
==========================

**ensure raspbian up to date**
```
sudo apt-get update
```

**create main folder**
```
cd /home/pi
mkdir gotmilk
cd gotmilk
```

**install python dev tools**
```
sudo apt-get install python-dev
```

**install spi**
```
mkdir py-spidev
cd py-spidev/
wget https://raw.github.com/doceme/py-spidev/master/setup.py
wget https://raw.github.com/doceme/py-spidev/master/spidev_module.c
sudo python setup.py install
```

**install pip**
```
sudo apt-get install python-pip
```

**use pip to install requests module**
```
sudo pip install requests
```

**copy files over to pi**
```
scp -r * pi@<IP ADDRESS>:/home/pi/gotmilk
```

**setup init.d**
```
sudo cp init.d/gotmilk.sh /etc/init.d
sudo chmod +x /etc/init.d/gotmilk.sh
sudo update-rc.d /etc/init.d/gotmilk.sh defaults
```

**duplicate the config file**
```
cd /home/pi/gotmilk
sudo cp .gotmilk /etc/gotmilk
```
