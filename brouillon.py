
url = f"https://api.pipedrive.com/v1/itemSearch?term={name}&item_types=organization&start=0&api_token={API_PIPE}"
headers = {
    "Accept": "application/json"
}
r = requests.request("GET", url, headers=headers)
j = r.json()
try:
    name_pipe = (j['data']['items'][0]['item']['id'])
    res.append(name_pipe)
    print(name_pipe)
except:
    name_pipe = "Not in Pipe"
    print("Not in Pipe")
    res.append(name_pipe)