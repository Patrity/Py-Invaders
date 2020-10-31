import requests
import json

global url, headers

url = "http://localhost:8080/api/player"
headers = {'content-type': 'application/json'}


def post(name, score):
    x = {
        "name": name,
        "score": score
    }
    player_json = json.dumps(x)

    requests.post(url, player_json, headers=headers)


def get():
    return requests.get(url, headers)
