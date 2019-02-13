import json

json_data=open('data.json').read()
data = json.loads(json_data)

statusPriceMap =  {
     'interne': 126,
     'medic': 270,
}

workers = []
for user in data["workers"]:
    userId = user["id"]
    userShifts = filter(lambda shift: shift["user_id"] == userId, data["shifts"])
    userPrice = len(userShifts) * statusPriceMap[user["status"]]
    workers.append({'id':userId, 'price':userPrice})

output = {'workers': workers}

with open('output.json', 'w') as outfile:
    json.dump(output, outfile)