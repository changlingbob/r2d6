import os
import re
import pickle
from random import random

outputs = []
crontabs = []

reports = {"a":{}, "u":{}}
runonce = False
userMap = {}
undoMap = {}
aliensEnum = ["sectoid", "thin man", "outsider", "floater", "cyberdisc", "drone", "muton", "chryssalid", "zombie", "berserker", "sectopod", "ethereal", "mechtoid", "seeker", "viper", "advent", "faceless", "archon", "andromedon", "gatekeeper", "codex", "avatar", "exalt", "friendly"]
aliensSynonym = {"snek":"viper", ":snake:":"viper", "thin mint":"thin man", ":alien:": "sectoid", "beserker": "beserker", "crispalids":"chryssalid", "chrysalid":"chryssalid", ":bug:":"chryssalid"}

FILE="plugins/xcom.data"
if os.path.isfile(FILE):
    reports = pickle.load(open(FILE, 'rb'))

def write(channel, string):
    print("Saying {}".format(string))
    outputs.append([channel, string])

def api_call(func, query):
    outputs.append(["api", func, query])

def process_api(data):
    global userMap
    if "members" in data.keys():
        for member in data["members"]:
            userMap[member["id"]] = member["name"]
    print(userMap)

def handle_kills(alien, text, user, channel):
    numbers = [int(s) for s in text.split() if s.isdigit()]
    if len(numbers) == 0:
        number = 1
    else:
        number = numbers[0]
    report_data(user, alien, number)
    pickle.dump(reports, open(FILE,"wb"))
    quip(user, alien, number, channel)

def report_data(user, alien, num):
    if not user in reports["u"]:
        reports["u"][user] = {}
    if not alien in reports["u"][user]:
        reports["u"][user][alien] = num
    else:
        reports["u"][user][alien] += num
    if not alien in reports["a"]:
        reports["a"][alien] = num
    else:
        reports["a"][alien] += num
    undoMap[user] = [alien, num]

def quip(user, alien, number, channel):
    check = random()
    # write(channel, "{0} have {1} kills; {2} has {3} deaths to {0}".format(alien, reports["a"][alien], userMap[user], reports["u"][user][alien]))
    if alien == "friendly":
        write(channel, "{} has killed {} of their own troops. {}".format(userMap[user], number, "You monster." if random() < 0.3 else ""))
    elif check < 0.25:
        print("a")
        write(channel, "{}(s) have now killed {} troops.".format(alien, reports["a"][alien]))
    elif check < 0.5:
        print("b")
        write(channel, "{} has lost {} troops to {}.".format(userMap[user], reports["u"][user][alien], alien))
    elif check < 0.75:
        print("c")
        if alien == "sectoid" and random() < 0.25:
            write(channel, ":alien: Ayyy lmao :alien:")
        else:
            write(channel, "Hooray for {}!".format(alien))
    else:
        print("d")

def undo_report(user):
    if user in undoMap:
        reports["u"][user][undoMap[user][0]] -= undoMap[user][1]
        reports["a"][undoMap[user][0]] -= undoMap[user][1]
        undoMap.pop(user)

def process_message(data):
    global reports
    global runonce
    global userMap
    global aliensEnum
    global aliensSynonym
    channel = data["channel"]
    user = data["user"]
    text = data["text"]
    if not runonce:
        print("running once")
        api_call("users.list", {"presence":0})
        runonce = True

    if "boulder" in text and random() < 0.01:
        write(channel, "Sadness...")
        write(channel, "But hooray for boulder!")

    if text.startswith("!report"):
        print(text)
        if "undo" in text:
            undo_report(user)
            outputs.append([channel, "Undone"])
            
        #do command stuff
        for alien in aliensEnum:
            if alien in text.lower():
                handle_kills(alien, text, user, channel)

        for alien in aliensSynonym:
            if alien in text.lower():
                handle_kills(aliensSynonym[alien], text, user, channel)

        if "nuke" in text and user == "U08TQGD7X":
            reports = {"a":{}, "u":{}}
        # if text.startswith("todo"):
        #     reports[channel].append(text[5:])
        #     outputs.append([channel, "added"])
        # if text == "reports":
        #     output = ""
        #     counter = 1
        #     for task in reports[channel]:
        #         output += "%i) %s\n" % (counter, task)
        #         counter += 1
        #     outputs.append([channel, output])
        # if text == "fin":
        #     reports[channel] = []
        # if text.startswith("done"):
        #     num = int(text.split()[1]) - 1
        #     reports[channel].pop(num)
        # if text == "show":
        #     print reports
        # pickle.dump(reports, open(FILE,"wb"))
