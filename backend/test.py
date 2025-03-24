import requests

url = "https://api.cal.com/v1/event-types"

response = requests.request("GET", url)
params = {"apiKey": "cal_live_d407b990737cc1b1bc749beda76493cd"}
response = requests.get(url, params=params)
print(response.text)