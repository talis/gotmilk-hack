#! /bin/sh
### BEGIN INIT INFO
# Provides:          milk maid
# Required-Start:    $remote_fs $syslog   
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Milk Maid
# Description:       Milk Maid
### END INIT INFO

PATH=/sbin:/bin:/usr/bin:
. /lib/init/vars.sh
. /lib/init/tmpfs.sh

TTYGRP=5
TTYMODE=620
[ -f /etc/default/devpts ] && . /etc/default/devpts

KERNEL="$(uname -s)"

. /lib/lsb/init-functions
. /lib/init/mount-functions.sh

do_start () {
    nohup env python2.7 /home/pi/gotmilk/gotmilk.py 2>&1 >/tmp/gotmilk.log &
}

case "$1" in
  start|"")
	do_start
	;;
  restart|reload|force-reload)
	echo "Error: argument '$1' not supported" >&2
	exit 3
	;;
  stop)
        ps aux | awk ' /gotmilk\.py/ { print $2 } ' | xargs kill -9
	;;
  *)
	echo "Usage: milkmaid.sh [start|stop]" >&2
	exit 3
	;;
esac

: