import requests

auth_token = "426e03663108aa37cdcfc37da0b6e7"

hipchat_url = "https://api.hipchat.com/v1/rooms/message?format=json&auth_token=" + auth_token

payload = {
	'room_id':'429941',
	'from':'Milk Maid',
	'color':'red',
	'notify':'true',
	'message':'More milk required - approximately 10 cups left'
}

print hipchat_url

r = requests.post(hipchat_url, data=payload)

print r.text
