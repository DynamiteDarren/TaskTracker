import os
import json
from duty import Duty
from duty_list import duty_list

def save_data(data):
    print("SAVING")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file = open(dir_path + "/Database/kitchen.json", "w+")
    json.dump(data, file)


def load_data():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file = open(dir_path + "/Database/kitchen.json", "r")
    json_data = json.load(file)

    l = duty_list([])
    for duty in json_data:
        d = Duty(duty)

        if d["DATA"] == '':
            d["Data"] = '0' * int(d["FREQUENCY"])
            print(f"New data {d['DATA']}")
        l.append(d)

    print(f"duty list length loaded is { len(l)}")
    return l

    

