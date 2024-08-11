import requests

URL = "https://random-word-api.herokuapp.com/word?number=10"

response = requests.get(url=URL)

data_words = response.json()
