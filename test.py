import requests

BASE = "http://127.0.0.1:5000/"

data = [{"name": "Tutorial Python", "views": 500, "likes": 15},
        {"name": "GTA V - Parte 1", "views": 1500, "likes": 30},
        {"name": "Como usar linux", "views": 3000, "likes": 60},
        {"name": "Teclado lindinho 2009", "views": 5000, "likes": 120},
        {"name": "Como zerar dark souls com uma mao", "views": 7000, "likes": 240},
        {"name": "Evidencias", "views": 9000, "likes": 480}]

for i in range(len(data)):
    response = requests.post(BASE + "video/" + str(i), data[i])
    print(response.json())

input()
response = requests.delete(BASE + "video/2")
print(response)

input()
response = requests.get(BASE + "video/2")
print(response.json())
response = requests.put(BASE + "video/2", {"name": "Danete", "likes": 500, "views": 500})
print(response.json())
response = requests.get(BASE + "video/2")
print(response.json())
