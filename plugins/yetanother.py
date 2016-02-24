import json
import os

outputs = []
crontabs = []

FILE="plugins/yetanother.data"
if os.path.isfile(FILE):
    with open(FILE) as jsonfile:
        data = json.load(jsonfile)

names = data["pilotsById"]
upgrades = data["upgradesById"]
modifications = data["modificationsById"]
title = data["titlesById"]
emojiMap = {"Lambda-Class Shuttle":":lambda:","Firespray-31":":firespray:","A-Wing":":awing:","TIE Advanced":":advanced:","TIE Bomber":":bomber:","B-Wing":":bwing:","YT-1300":":falcon:","TIE Fighter":":fighter:","HWK-290":":hwk:","TIE Interceptor":":interceptor:","X-Wing":":xwing:","Y-Wing":":ywing:"}
print("loaded data")

def process_api(data):
    print("test")

def write(channel, string):
    print("Saying {}".format(string))
    outputs.append([channel, string])

def process_message(data):
    global tasks
    channel = data["channel"]
    text = data["text"]
    #only accept tasks on DM channels

    # Fluff
    if "geordanr" in text:
        print("parsing")
        output = ""
        for fragment in text.split("&amp;"):
            if not fragment.startswith("d=v4!s!"):
                continue
            for ship in fragment[7:].split(';'):
                slots = ship.split(":")
                pts = 0
                if names[slots[0]]["ship"] in emojiMap.keys():
                    ship = emojiMap[names[slots[0]]["ship"]]
                else:
                    ship = "(" + names[slots[0]]["ship"] + ")"
                output += names[slots[0]]["name"] + " " + ship + ": "
                pts += names[slots[0]]["points"]
                print(slots)
                if "," in slots[1]:
                    for slot in slots[1].split(','):
                        if slot != "-1":
                            output += upgrades[slot]["name"] + ", "
                            pts += upgrades[slot]["points"]
                elif slots[1] != "-1" and slots[1] != "":
                    output += upgrades[slots[1]]["name"] + ", "
                    pts += upgrades[slots[1]]["points"]    
                if slots[2] != "-1":
                    output += title[slots[2]]["name"] + ", "
                    pts += title[slots[2]]["points"]
                if slots[3] != "-1":
                    output += modifications[slots[3]]["name"] + ", "
                    pts += modifications[slots[3]]["points"]
                print("done parsing")
                output = output[:-2] + " _(" + str(pts) + ")_\n"
        write(channel, output)