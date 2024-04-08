import requests

url = "http://localhost:8000/characters"
headers = {'Content-type': 'application/json'}

my_character = {
    "name": "Gandalf",
    "level": 10,
    "role": "Wizard",
    "charisma": 15,
    "strength": 10,
    "dexterity": 10
}
response = requests.post(url, json=my_character, headers=headers)
print(response.json())

response = requests.get(url)
print(response.json())

my_character = {
    "name": "Robin",
    "level": 5,
    "role": "Archer",
    "charisma": 10,
    "strength": 10,
    "dexterity": 10
}
response = requests.post(url, json=my_character, headers=headers)
print(response.json())

my_character = {
    "name": "Howard",
    "level": 1,
    "role": "Shield",
    "charisma": 15,
    "strength": 50,
    "dexterity": 1
}
response = requests.post(url, json=my_character, headers=headers)
print(response.json())


urlp=url+"/?role=Archer&charisma=10"

response = requests.get(urlp)
print("fdasfdsafdsafdsafd", response.json())


update_character = {
    "charisma": 20,
    "strength": 15,
    "dexterity": 15
}
response = requests.put(url+"/2", json=update_character, headers=headers)
print(response.json())


response = requests.delete(url + "/3")
print(response.json())

my_character = {
    "name": "Legolas",
    "level": 5,
    "role": "Archer",
    "charisma": 15,
    "strength": 10,
    "dexterity": 10
}
response = requests.post(url, json=my_character, headers=headers)
print(response.json())


response = requests.get(url)
print(response.json())
