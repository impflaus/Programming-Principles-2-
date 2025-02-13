import json
def connection():

    with open("data.json", "r") as file:
        fromFile = json.load(file)
        array = fromFile["imdata"]
        for i in range(len(array)):
            tn = array[i]["l1PhysIf"]["attributes"]["dn"]
            description = array[i]["l1PhysIf"]["attributes"]["descr"]
            speed = array[i]["l1PhysIf"]["attributes"]["speed"]
            mtu = array[i]["l1PhysIf"]["attributes"]["mtu"]
            print(f"{tn}         {description}       {speed}        {mtu}")
        file.close()

connection()