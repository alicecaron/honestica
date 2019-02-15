import json
import datetime
from math import *

json_data=open('data.json').read()
data = json.loads(json_data)

statusPriceMap =  {
     'interne': 126,
     'medic': 270,
     'interim': 480,
}

workers = []
commission = 0
interimShifts = 0
for user in data["workers"]:
    userId = user["id"]

    # according to the user status, get the correct price for a weekday user shift
    userShiftPrice = statusPriceMap[user["status"]]
    userShifts = filter(lambda shift: not (shift["user_id"] is None) and shift["user_id"] == userId, data["shifts"])

    userTotalPrice = 0
    for userShift in userShifts:
        # determine if week end
        date = userShift["start_date"]
        year, month, day = (int(x) for x in date.split('-'))
        weekdayNumber = datetime.date(year, month, day).weekday()

        # according to the day, get the correct price of the shift
        shiftPrice = userShiftPrice if weekdayNumber<5 else 2*userShiftPrice
        userTotalPrice += shiftPrice

        # add commision
        if user["status"] == 'interim':
            commission += 80
            interimShifts += 1
        commission += shiftPrice * 5.0 / 100.0
    workers.append({'id':userId, 'price':userTotalPrice})

output = {'workers': workers, 'commission':{'pdg_fee': commission, 'interim_shifts': interimShifts}}

with open('output.json', 'w') as outfile:
    json.dump(output, outfile)