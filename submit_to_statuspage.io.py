import json
import httplib, urllib, time

from pprint import pprint

with open('/milklevel.json') as milk:
  data = json.load(milk)

api_key = 'REDACTED'
page_id = 'REDACTED'
metric_id = 'REDACTED'
api_base = 'api.statuspage.io'
 
ts = int(time.time())
value = data["milk"]

params = urllib.urlencode({'data[timestamp]': ts, 'data[value]': value})
headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "OAuth " + api_key}
 
conn = httplib.HTTPSConnection(api_base)
conn.request("POST", "/v1/pages/" + page_id + "/metrics/" + metric_id + "/data.json", params, headers)
response = conn.getresponse()
