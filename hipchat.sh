#!/bin/bash

TOKEN=426e03663108aa37cdcfc37da0b6e7
ROOMID=429941
MESSAGE=
FROM=
COLOUR=
NOTIFY=

while getopts "t:r:m:f:c:n:" OPTION
do
	case $OPTION in
		r)
			ROOMID=$OPTARG
			;;
		m)
			MESSAGE=$OPTARG
			;;
		f)
			FROM=$OPTARG
			;;
		t)
			TOKEN=$OPTARG
			;;
		c)
			COLOUR=$OPTARG
			;;
		n)
			NOTIFY=$OPTARG
			;;
	esac
done

curl -d "notify=$NOTIFY&color=$COLOUR&room_id=$ROOMID&from=$FROM&message=$MESSAGE" -X POST "https://api.hipchat.com/v1/rooms/message?format=json&auth_token=$TOKEN"
echo $COMMAND
