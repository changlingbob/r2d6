import os
import pickle

outputs = []
crontabs = []

tasks = []

FILE="plugins/todo.data"
if os.path.isfile(FILE):
    tasks = pickle.load(open(FILE, 'rb'))

def process_api(data):
    print("test")

def process_message(data):
    global tasks
    channel = data["channel"]
    text = data["text"]
    #only accept tasks on DM channels

    # Fluff
    if "contextbot" in text:
        outputs.append([channel, "that's me!"])

    # Topic shenanigans
    if text.startswith("!topic"):
        print(channel)
        outputs.append(["api", "channels.info", {"channel": channel}])

    # Old to-do functionality for reference, mostly
        #do command stuff
    if text.startswith("todo"):
        if text[5:] == "tasks" or text[4:] == "":
            output = ""
            counter = 1
            for task in tasks:
                output += "%i) %s\n" % (counter, task)
                counter += 1
            outputs.append([channel, output])
        elif text[5:] == "fin":
            tasks = []
        elif text[5:].startswith("done"):
            num = int(text[5:].split()[1]) - 1
            tasks.pop(num)
        elif text[5:] == "show":
            print tasks
        else:
            tasks.append(text[5:])
            outputs.append([channel, "added"])
        pickle.dump(tasks, open(FILE,"wb"))
