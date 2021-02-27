# Made by LiquidDeath911 for his bud TigeltoN
#
# This script is for keeping a record of what number a user
# picks for TigeltoN's retro roulette streams on Twitch

# imports
import clr
import sys
import json
import os
import ctypes
import codecs

# script info
ScriptName = "Retro Roulette"
Website = "https://github.com/LiquidDeath911/RetroRoulette"
Description = "Retro Roulette for Streamlabs Chatbot"
Creator = "LiquidDeath911"
Version = "2.0"

# global variables
path = os.path.dirname(__file__)
pickedNumbersPath = os.path.join(path, PickedNumbers)
responseListsPath = os.path.join(path, ResponseLists)
configFile = "config.json"
settings = {}
isRouletteStarted = False
rouletteMode = ""
consoleMax = 0
userList = []
userNumbers = []
userPicked = []
numbersPicked = []
currentUser = ""
currentNum = 0
bannedList = []
n64List = []
snesList = []
nesList = []
gbList = []
pickedTextList = []
commands = ["!startrr","!endrr","!resetrr","!restartrr","!nextrr","!queuerr","!pickrr","!consolerr","!maxrr","!leaverr","!spotrr","!inforr", "!moderr","!currentrr","!whorr","!banrr", "!unbanrr", "!updaterr"]


def Init():
	global settings, rouletteMode, consoleMax, bannedList, n64List, snesList, nesList, gbList, pickedTextList
	
	try:
		with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
			settings = json.load(file, encoding='utf-8-sig')
	except:
		settings = {
			"liveOnly": True,
                        "defaultMode": "Random",
                        "defaultConsole": "SNES",
                        "banPermission": "Editor",
			"startCommand": "!startrr",
                        "endCommand": "!endrr",
                        "resetCommand": "!resetrr",
                        "restartCommand": "!restartrr",
                        "nextCommand": "!nextrr",
                        "modeCommand": "!moderr",
                        "pickCommand": "!pickrr",
                        "consoleCommand": "!consolerr",
                        "maxCommand": "!maxrr",
                        "leaveCommand": "!leaverr",
                        "spotCommand": "!spotrr",
                        "infoCommand": "!inforr",
                        "queueCommand": "!queuerr",
                        "currentCommand": "!currentrr",
                        "whoCommand": "!whorr",
                        "startPermission": "Editor",
                        "endPermission": "Editor",
                        "resetPermission": "Editor",
                        "restartPermission": "Editor",
                        "nextPermission": "Editor",
                        "modePermission": "Editor",
                        "pickPermission": "Everyone",
                        "consolePermission": "Editor",
                        "maxPermission": "Everyone",
                        "leavePermission": "Everyone",
                        "spotPermission": "Everyone",
                        "infoPermission": "Everyone",
                        "queuePermission": "Everyone",
                        "currentPermission": "Everyone",
                        "whoPermission": "Everyone",
                        "startResponse" : "Retro Roulette has started! Use $pickCommand followed by a positive whole number or the word random to enter!",
			"endResponse" : "Retro Roulette has ended. Better luck next time!",
                        "resetResponse" : "Retro Roulette has been reset, everyone can pick numbers again!",
                        "restartResponse" : "Retro Roulette has been restarted. The queue is now empty and everyone can pick numbers again!",
                        "modeRandomResponse" : "Retro Roulette's mode has been changed to random!",
                        "modeQueueResponse" : "Retro Roulette's mode has been changed to queue!",
			"userChosenResponse" : "Congrats @$user, your number has been picked!",
			"notifyStreamerResponse" : "@$user the next number is $number.",
			"invalidNumberResponse" : "@$user, please try again. Make sure the number you picked is a positive whole number greater than 0 and less than $consoleMax.",
			"alreadyPickedResponse" : "@$user, that number has already been picked. Please try again.",
			"alreadyEnteredResponse" : "@$user, you have already entered the queue.",
			"noRouletteResponse" : "@$user, Retro Roulette has not been started.",
                        "alreadyStartedResponse" : "@$user, Retro Roulette has already been started.",
                        "alreadyEndedResponse" : "@$user, Retro Roulette has already been ended.",
                        "notEmptyResponse" : "@$user, queue is not empty. Use $nextCommand to get the next number or use $restartCommand to empty the queue and start over.",
                        "emptyResponse" : "@$user, queue is empty. $nextCommand doesn't work when the queue is empty.",
                        "noNumberResponse" : "@$user you must put a positive whole number after $pickCommand, or the word random.",
                        "enteredResponse" : "@$user, you have entered the queue with the number $number.",
                        "consoleChangedResponse" : "@$user, you have changed the console to $console.",
                        "consoleNotChangedResponse" : "@$user, you must enter one of the allowed consoles after $consoleCommand.",
                        "maxResponse" : "@$user, the max number that can be chosen is $consoleMax.",
                        "leaveResponse" : "@$user, you have been removed from the queue.",
                        "removedResponse" : "@$user, you have been removed from the queue because your number was too high for the new console.",
                        "outOfBoundsResponse" : "@$user, you have picked a number that is less than 1 or too large. The max number currently is $consoleMax.",
                        "notEnteredLeaveResponse" : "@$user, you can't leave the queue without entering first. Idiot KEKW",
                        "notEnteredSpotResponse" : "@$user, you can't check your spot in the queue without entering first. Idiot KEKW",
                        "spotResponse" : "@$user, your spot in the queue is $spot out of $total HeadBanging",
                        "spotRandomResponse" : "@$user, you are in the queue of $total people. But Retro Roulette is in Random mode. Good luck HyperTigel",
                        "queueRandomResponse" : "The queue has $total people in it but Retro Roulette is in Random mode. Good luck HyperTigel",
                        "queueFiveResponse" : "The next $spots spots are: $user1 with $num1; $user2 with $num2; $user3 with $num3; $user4 with $num4; $user5 with $num5;",
                        "modeNotChangedResponse" : "@user, the mode was not changed. Make sure you put either Random or Queue after the $modeCommand",
                        "currentResponse" : "The current number is $number picked by $user PepoG",
                        "whoResponse" : "@$user, you picked number $number",
                        "whoOtherResponse" : "They picked number $number",
                        "banResponse" : "@$user has been banned oatsTrash",
                        "unbanResponse" : "@$user has been unbanned peepoSHAKE",
		}

        with open(os.path.join(path, "bannedList.json"), 'r') as filehandle:
                bannedList = json.load(filehandle)

        with open(os.path.join(pickedNumbersPath, "n64List.json"), 'r') as filehandle:
                n64List = json.load(filehandle)

        with open(os.path.join(pickedNumbersPath, "snesList.json"), 'r') as filehandle:
                snesList = json.load(filehandle)

        with open(os.path.join(pickedNumbersPath, "nesList.json"), 'r') as filehandle:
                nesList = json.load(filehandle)

        with open(os.path.join(pickedNumbersPath, "gbList.json"), 'r') as filehandle:
                gbList = json.load(filehandle)

        with open(os.path.join(responseListPath, "pickedTextList.json"), 'r') as filehandle:
                pickedTextList = json.load(filehandle)

        rouletteMode = settings["defaultMode"]
        
        if settings["defaultConsole"] == "SNES" or settings["defaultConsole"] == "snes":
                consoleMax = 725
        elif settings["defaultConsole"] == "NES" or settings["defaultConsole"] == "nes":
                consoleMax = 677
        elif settings["defaultConsole"] == "N64" or settings["defaultConsole"] == "n64":
                consoleMax = 296
        elif settings["defaultConsole"] == "GB" or settings["defaultConsole"] == "gb":
                consoleMax = 582
	
	return

def Execute(data):
	global userList, userNumbers, userPicked, commands, rouletteMode, isRouletteStarted, defaultConsole, consoleMax, numbersPicked, currentNum, currentUser, bannedList, n64List, snesList, nesList, gbList, pickedTextList

        if data.IsChatMessage() and (data.GetParam(0).lower() in commands) and ((not (data.UserName.lower() in bannedList)) or (data.GetParam(0).lower() == "!unbanrr")) and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"] or data.UserName == "LiquidDeath911")): 
                if data.IsChatMessage() and (data.GetParam(0).lower() == "!banrr") and (Parent.HasPermission(data.User, settings["banPermission"], "") or data.UserName == "LiquidDeath911"):
                        outputMessage = ""
                        tempBannedList = []
                        
                        with open(os.path.join(path, "bannedList.json"), 'r') as filehandle:
                                tempBannedList = json.load(filehandle)
                        
                        if (data.GetParamCount() == 2):
                                try:
                                        toBan = data.GetParam(1).lower()
                                except:
                                        return
                                if (not (toBan in tempBannedList)):
                                        tempBannedList.append(toBan)
                                        outputMessage = settings["banResponse"]
                                        outputMessage = outputMessage.replace("$user", toBan)
                                
                        else:
                                return

                        Parent.SendStreamMessage(outputMessage)

                        with open(os.path.join(path, "bannedList.json"), 'w') as filehandle:
                                json.dump(tempBannedList, filehandle)

                        return

                elif data.IsChatMessage() and (data.GetParam(0).lower() == "!unbanrr") and (Parent.HasPermission(data.User, settings["banPermission"], "") or data.UserName == "LiquidDeath911"):
                        outputMessage = ""
                        tempBannedList = []
                        
                        with open(os.path.join(path, "bannedList.json"), 'r') as filehandle:
                                tempBannedList = json.load(filehandle)
                        
                        if (data.GetParamCount() == 2):
                                try:
                                        toUnBan = data.GetParam(1).lower()
                                except:
                                        return
                                if (toUnBan in tempBannedList):
                                        place = tempBannedList.IndexOf(toUnBan)
                                        tempBannedList.pop(place)
                                        outputMessage = settings["unbanResponse"]
                                        outputMessage = outputMessage.replace("$user", toUnBan)
                                
                        else:
                                return

                        Parent.SendStreamMessage(outputMessage)

                        with open(os.path.join(path, "bannedList.json"), 'w') as filehandle:
                                json.dump(tempBannedList, filehandle)

                        return
                
                elif data.IsChatMessage() and (data.GetParam(0).lower() == settings["startCommand"]) and (Parent.HasPermission(data.User, settings["startPermission"], "") or data.UserName == "LiquidDeath911"):
                        outputMessage = ""			
                        username = data.UserName

                        if not isRouletteStarted:
                                outputMessage = settings["startResponse"]
                                outputMessage = outputMessage.replace("$pickCommand", settings["pickCommand"])
                                isRouletteStarted = True
                                userList = []
                                userNumbers = []
                                userPicked = []
                                numbersPicked = []
                        else:
                                outputMessage = settings["alreadyStartedResponse"]
                                outputMessage = outputMessage.replace("$user", username)

                        Parent.SendStreamMessage(outputMessage)

                        return
                        
                elif data.IsChatMessage() and (data.GetParam(0).lower() == settings["endCommand"]) and (Parent.HasPermission(data.User, settings["endPermission"], "") or data.UserName == "LiquidDeath911"):
                        outputMessage = ""
                        username = data.UserName

                        if not isRouletteStarted:
                                outputMessage = settings["alreadyEndedResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                        else:
                                outputMessage = settings["endResponse"]
                                isRouletteStarted = False
                                userList = []
                                userNumbers = []
                                userPicked = []
                                numbersPicked = []

                        Parent.SendStreamMessage(outputMessage)

                        return

                elif data.IsChatMessage() and (data.GetParam(0).lower() == settings["resetCommand"]) and (Parent.HasPermission(data.User, settings["resetPermission"], "") or data.UserName == "LiquidDeath911"):
                        outputMessage = ""
                        username = data.UserName

                        if not isRouletteStarted:
                                outputMessage = settings["noRouletteResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                        elif not (userList) and not (userNumbers):
                                outputMessage = settings["resetResponse"]
                                userPicked = []
                        elif (userList or userNumbers):
                                outputMessage = settings["notEmptyResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                                outputMessage = outputMessage.replace("$nextCommand", settings["nextCommand"])
                                outputMessage = outputMessage.replace("$restartCommand", settings["restartCommand"])

                        Parent.SendStreamMessage(outputMessage)

                        return

                elif data.IsChatMessage() and (data.GetParam(0).lower() == settings["restartCommand"]) and (Parent.HasPermission(data.User, settings["restartPermission"], "") or data.UserName == "LiquidDeath911"):
                        outputMessage = ""
                        username = data.UserName

                        if not isRouletteStarted:
                                outputMessage = settings["noRouletteResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                        elif (userList or userNumbers):
                                outputMessage = settings["restartResponse"]
                                userList = []
                                userNumbers = []
                                userPicked = []
                        elif not (userList) and not (userNumbers):
                                outputMessage = settings["resetResponse"]
                                userPicked = []

                        Parent.SendStreamMessage(outputMessage)

                        return

                elif data.IsChatMessage() and (data.GetParam(0).lower() == settings["nextCommand"]) and (Parent.HasPermission(data.User, settings["nextPermission"], "") or data.UserName == "LiquidDeath911"):
                        outputMessage = ""
                        username = data.UserName
                        pickedUser = ""
                        pickedNumber = 0
                        rand = 0

                        if not isRouletteStarted:
                                outputMessage = settings["noRouletteResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                        elif (userList or userNumbers):
                                with open(os.path.join(path, "pickedTextList.json"), 'r') as filehandle:
                                        pickedTextList = json.load(filehandle)
                                
                                pickedTextLength = len(pickedTextList)
                                randLine = (Parent.GetRandom(1, pickedTextLength) - 1)
                                outputMessage = pickedTextList[randLine]
                                
                                outputMessage2 = settings["notifyStreamerResponse"]
                                
                                if rouletteMode == "Random":
                                        userMax = len(userList)
                                        rand = (Parent.GetRandom(1, userMax) - 1)
                                        pickedUser = userList.pop(rand)
                                        pickedNumber = userNumbers.pop(rand)
                                        numbersPicked.append(pickedNumber)
                                        userPicked.append(pickedUser)
                                        currentUser = pickedUser
                                        currentNum = pickedNumber
                                else:
                                        pickedUser = userList.pop(0)
                                        pickedNumber = userNumbers.pop(0)
                                        userPicked.append(pickedUser)

                                outputMessage = outputMessage.replace("$user", pickedUser)
                                outputMessage2 = outputMessage2.replace("$user", username)
                                outputMessage2 = outputMessage2.replace("$number", str(pickedNumber))
                                
                                Parent.SendStreamMessage(outputMessage2)
                                
                        elif not (userList or userNumbers):
                                outputMessage = settings["emptyResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                                outputMessage = outputMessage.replace("$nextCommand", settings["nextCommand"])

                        Parent.SendStreamMessage(outputMessage)

                        return

                elif data.IsChatMessage() and (data.GetParam(0).lower() == settings["modeCommand"]) and (Parent.HasPermission(data.User, settings["modePermission"], "") or data.UserName == "LiquidDeath911"):
                        outputMessage = ""
                        username = data.UserName

                        if (data.GetParamCount() == 2):
                                try:
                                        mode = data.GetParam(1)
                                except:
                                        mode = rouletteMode

                                if mode == "Random" or mode == "random" or mode == "RANDOM":
                                        rouletteMode = "Random"
                                        outputMessage = settings["modeRandomResponse"]
                                elif mode == "Queue" or mode == "queue" or mode == "QUEUE":
                                        rouletteMode = "Queue"
                                        outputMessage = settings["modeQueueResponse"]
                                else:
                                        outputMessage = settings["modeNotChangedResponse"]
                                        outputMessage = outputMessage.replace("$user", username)
                                        outputMessage = outputMessage.replace("$modeCommand", settings["modeCommand"])

                        else:
                                outputMessage = settings["modeNotChangedResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                                outputMessage = outputMessage.replace("$modeCommand", settings["modeCommand"])
                                        

                        Parent.SendStreamMessage(outputMessage)
                        
                        return

                elif data.IsChatMessage() and (data.GetParam(0).lower() == settings["queueCommand"]) and (Parent.HasPermission(data.User, settings["queuePermission"], "") or data.UserName == "LiquidDeath911"):
                        outputMessage = ""
                        username = data.UserName

                        if not isRouletteStarted:
                                outputMessage = settings["noRouletteResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                        elif rouletteMode == "Random":
                                outputMessage = settings["queueRandomResponse"]
                                total = str(len(userList))
                                outputMessage = outputMessage.replace("$total", total)
                        elif rouletteMode == "Queue":
                                if userList or userNumbers:
                                        outputMessage = settings["queueFiveResponse"]
                                        outputMessage = outputMessage.replace("$user1", userList[0])
                                        outputMessage = outputMessage.replace("$num1", str(userNumbers[0]))
                                        if (len(userList) > 1):
                                                outputMessage = outputMessage.replace("$user2", userList[1])
                                                outputMessage = outputMessage.replace("$num2", str(userNumbers[1]))
                                                if (len(userList) > 2):
                                                        outputMessage = outputMessage.replace("$user3", userList[2])
                                                        outputMessage = outputMessage.replace("$num3", str(userNumbers[2]))
                                                        if (len(userList) > 3):
                                                                outputMessage = outputMessage.replace("$user4", userList[3])
                                                                outputMessage = outputMessage.replace("$num4", str(userNumbers[3]))
                                                                if (len(userList) > 4):
                                                                        outputMessage = outputMessage.replace("$user5", userList[4])
                                                                        outputMessage = outputMessage.replace("$num5", str(userNumbers[4]))
                                                                        outputMessage = outputMessage.replace("$spots", "five")
                                                                else:
                                                                        outputMessage = outputMessage.replace("$user5 with $num5;", "")
                                                                        outputMessage = outputMessage.replace("$spots", "four")
                                                        else:
                                                                outputMessage = outputMessage.replace("$user4 with $num4; $user5 with $num5;", "")
                                                                outputMessage = outputMessage.replace("$spots", "three")
                                                else:
                                                        outputMessage = outputMessage.replace("$user3 with $num3; $user4 with $num4; $user5 with $num5;", "")
                                                        outputMessage = outputMessage.replace("$spots", "two")
                                        else:
                                                outputMessage = outputMessage.replace("$user2 with $num2; $user3 with $num3; $user4 with $num4; $user5 with $num5;", "")
                                                outputMessage = outputMessage.replace("$spots spots are", "spot is")
                                else:
                                        outputMessage = "The queue is empty."
                        else:
                                outputMessage = settings["noRouletteResponse"]
                                outputMessage = outputMessage.replace("$user", username)

                        Parent.SendStreamMessage(outputMessage)

                        return

                elif data.IsChatMessage() and (data.GetParam(0).lower() == settings["pickCommand"]) and (Parent.HasPermission(data.User, settings["pickPermission"], "") or data.UserName == "LiquidDeath911"):
                        outputMessage = ""
                        username = data.UserName

                        if not isRouletteStarted:
                                outputMessage = settings["noRouletteResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                        elif (data.GetParamCount() == 2) and not (username in userList) and not (username in userPicked):
                                try: 
                                        number = int(data.GetParam(1))
                                except:
                                        if data.GetParam(1) == 'random':
                                                number = Parent.GetRandom(1, consoleMax)
                                                while number in userNumbers or number in numbersPicked:
                                                        number = Parent.GetRandom(1, consoleMax)

                                                userList.append(username)
                                                userNumbers.append(number)
                                                outputMessage = settings["enteredResponse"]
                                                outputMessage = outputMessage.replace("$user", username)
                                                outputMessage = outputMessage.replace("$number", str(number))
                                        else:
                                                outputMessage = settings["invalidNumberResponse"]
                                                outputMessage = outputMessage.replace("$user", username)
                                                outputMessage = outputMessage.replace("$consoleMax", str(consoleMax))

                                        Parent.SendStreamMessage(outputMessage)
                                        
                                        return

                                if (number in userNumbers) or (number in numbersPicked):
                                        outputMessage = settings["alreadyPickedResponse"]
                                        outputMessage = outputMessage.replace("$user", username)
                                elif (number > consoleMax) or (number < 1):
                                        outputMessage = settings["outOfBoundsResponse"]
                                        outputMessage = outputMessage.replace("$user", username)
                                        outputMessage = outputMessage.replace("$consoleMax", str(consoleMax))
                                else:
                                        userList.append(username)
                                        userNumbers.append(number)
                                        outputMessage = settings["enteredResponse"]
                                        outputMessage = outputMessage.replace("$user", username)
                                        outputMessage = outputMessage.replace("$number", str(number))
                                        
                        elif (username in userList) or (username in userPicked):
                                outputMessage = settings["alreadyEnteredResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                        else:
                                outputMessage = settings["noNumberResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                                outputMessage = outputMessage.replace("$pickCommand", settings["pickCommand"])

                        Parent.SendStreamMessage(outputMessage)

                        return

                elif data.IsChatMessage() and (data.GetParam(0).lower() == settings["consoleCommand"]) and (Parent.HasPermission(data.User, settings["consolePermission"], "") or data.UserName == "LiquidDeath911"):
                        outputMessage = ""
                        outputMessage2 = ""
                        username = data.UserName
                        console = ""

                        if (data.GetParamCount() == 2):
                                try:
                                        console = data.GetParam(1)
                                except:
                                        console = defaultConsole

                                if console == "SNES" or console == "snes" or console == "Snes":
                                        consoleMax = 725
                                elif console == "NES" or console == "nes" or console == "Nes":
                                        consoleMax = 677
                                elif console == "N64" or console == "n64":
                                        consoleMax = 296
                                elif console == "GB" or console == "gb" or console == "Gb":
                                        consoleMax = 582
                                else:
                                        outputMessage = settings["consoleNotChangedResponse"]
                                        outputMessage = outputMessage.replace("$user", username)
                                        outputMessage = outputMessage.replace("$consoleCommand", settings["consoleCommand"])

                                        Parent.SendStreamMessage(outputMessage)

                                        return

                                for num in userNumbers:
                                        if num > consoleMax:
                                                temp3 = userNumbers.index(num)
                                                tempName = userList.pop(temp3)
                                                userNumbers.pop(temp3)
                                                outputMessage2 = settings["removedResponse"]
                                                outputMessage2 = outputMessage.replace("$user", tempName)
                                                Parent.SendStreamMessage(outputMessage2)

                                outputMessage = settings["consoleChangedResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                                outputMessage = outputMessage.replace("$console", console)

                        else:
                                outputMessage = settings["consoleNotChangedResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                                outputMessage = outputMessage.replace("$consoleCommand", settings["consoleCommand"])

                        Parent.SendStreamMessage(outputMessage)

                        return

                elif data.IsChatMessage() and (data.GetParam(0).lower() == settings["maxCommand"]) and (Parent.HasPermission(data.User, settings["maxPermission"], "") or data.UserName == "LiquidDeath911"):
                        outputMessage = ""
                        username = data.UserName
                        
                        outputMessage = settings["maxResponse"]
                        outputMessage = outputMessage.replace("$user", username)
                        outputMessage = outputMessage.replace("$consoleMax", str(consoleMax))

                        Parent.SendStreamMessage(outputMessage)

                        return

                elif data.IsChatMessage() and (data.GetParam(0).lower() == settings["leaveCommand"]) and (Parent.HasPermission(data.User, settings["leavePermission"], "") or data.UserName == "LiquidDeath911"):
                        outputMessage = ""
                        username = data.UserName

                        if not isRouletteStarted:
                                outputMessage = settings["noRouletteResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                        elif (username in userList):
                                temp2 = userList.index(username)
                                userList.pop(temp2)
                                userNumbers.pop(temp2)
                                outputMessage = settings["leaveResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                        else:
                                outputMessage = settings["notEnteredLeaveResponse"]
                                outputMessage = outputMessage.replace("$user", username)

                        Parent.SendStreamMessage(outputMessage)

                        return

                elif data.IsChatMessage() and (data.GetParam(0).lower() == settings["spotCommand"]) and (Parent.HasPermission(data.User, settings["spotPermission"], "") or data.UserName == "LiquidDeath911"):
                        outputMessage = ""
                        username = data.UserName

                        if not isRouletteStarted:
                                outputMessage = settings["noRouletteResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                        elif (username in userList):
                                total = str(len(userList))
                                if rouletteMode == "Queue":
                                        spot = str(userList.index(username) + 1)
                                        outputMessage = settings["spotResponse"]
                                        outputMessage = outputMessage.replace("$user", username)
                                        outputMessage = outputMessage.replace("$spot", spot)
                                        outputMessage = outputMessage.replace("$total", total)
                                else:
                                        outputMessage = settings["spotRandomResponse"]
                                        outputMessage = outputMessage.replace("$user", username)
                                        outputMessage = outputMessage.replace("$total", total)
                        else:
                                outputMessage = settings["notEnteredSpotResponse"]
                                outputMessage = outputMessage.replace("$user", username)

                        Parent.SendStreamMessage(outputMessage)

                        return
                        
                elif data.IsChatMessage() and ((data.GetParam(0).lower() == settings["infoCommand"]) or (data.GetParam(0).lower() == "!commands")) and (Parent.HasPermission(data.User, settings["infoPermission"], "") or data.UserName == "LiquidDeath911"):

                        outputMessage = "For info about Retro Roulette and its command list go here: https://pastebin.com/TxWA4CmS"

                        Parent.SendStreamMessage(outputMessage)

                        return

                elif data.IsChatMessage() and (data.GetParam(0).lower() == settings["currentCommand"]) and (Parent.HasPermission(data.User, settings["currentPermission"], "") or data.UserName == "LiquidDeath911"):
                        outputMessage = ""

                        if not isRouletteStarted:
                                outputMessage = settings["noRouletteResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                        else:
                                outputMessage = settings["currentResponse"]
                                outputMessage = outputMessage.replace("$user", currentUser)
                                outputMessage = outputMessage.replace("$number", str(currentNum))

                        Parent.SendStreamMessage(outputMessage)

                        return
                        
                elif data.IsChatMessage() and (data.GetParam(0).lower() == settings["whoCommand"]) and (Parent.HasPermission(data.User, settings["whoPermission"], "") or data.UserName == "LiquidDeath911"):
                        outputMessage = ""
                        username = data.UserName

                        if not isRouletteStarted:
                                outputMessage = settings["noRouletteResponse"]
                                outputMessage = outputMessage.replace("$user", username)
                        elif (data.GetParamCount() == 2):
                                try:
                                        otherUser = data.GetParam(1)
                                except:
                                        if (username in userList):
                                                whoTemp = userList.index(username)
                                                whoNum = userNumbers[whoTemp]
                                                outputMessage = settings["whoResponse"]
                                                outputMessage = outputMessage.replace("$user", username)
                                                outputMessage = outputMessage.replace("$number", str(whoNum))
                                                
                                                Parent.SendStreamMessage(outputMessage)
                                                
                                                return
                                        else:
                                                outputMessage = settings["whoNoneResponse"]
                                                
                                                Parent.SendStreamMessage(outputMessage)
                                                
                                                return
                                        
                                if (otherUser in userList):
                                        whoTemp = userList.index(otherUser)
                                        whoNum = userNumbers[whoTemp]
                                        outputMessage = settings["whoOtherResponse"]
                                        outputMessage = outputMessage.replace("$user", username)
                                        outputMessage = outputMessage.replace("$number", str(whoNum))
                                else:
                                        outputMessage = settings["whoNoneResponse"]

                        else:
                                if (username in userList):
                                        whoTemp = userList.index(username)
                                        whoNum = userNumbers[whoTemp]
                                        outputMessage = settings["whoResponse"]
                                        outputMessage = outputMessage.replace("$user", username)
                                        outputMessage = outputMessage.replace("$number", str(whoNum))
                                        
                                else:
                                        outputMessage = settings["whoNoneResponse"]

                        Parent.SendStreamMessage(outputMessage)

                        return

        elif data.IsChatMessage() and (data.GetParam(0).lower() == "!updaterr") and (data.UserName == "LiquidDeath911" or data.UserName == "TigeltoN"):

                if isRouletteStarted:
                        outputMessage = "Please end RetroRoulette before updating."
                else:
                        update(https://github.com/LiquidDeath911/RetroRoulette, force_update=True)
                
	return

def ReloadSettings(jsonData):
	Init()
	return

def OpenReadMe():
	location = os.path.join(os.path.dirname(__file__), "README.txt")
	os.startfile(location)
	return

def ScriptToggled(state):
	return

def Tick():
        return

def update(dl_url, force_update=False):
    """
Attempts to download the update url in order to find if an update is needed.
If an update is needed, the current script is backed up and the update is
saved in its place.
"""
    import urllib
    import re
    from subprocess import call
    def compare_versions(vA, vB):
        """
Compares two version number strings
@param vA: first version string to compare
@param vB: second version string to compare
@author <a href="http_stream://sebthom.de/136-comparing-version-numbers-in-jython-pytho/">Sebastian Thomschke</a>
@return negative if vA < vB, zero if vA == vB, positive if vA > vB.
"""
        if vA == vB: return 0

        def num(s):
            if s.isdigit(): return int(s)
            return s

        seqA = map(num, re.findall('\d+|\w+', vA.replace('-SNAPSHOT', '')))
        seqB = map(num, re.findall('\d+|\w+', vB.replace('-SNAPSHOT', '')))

        # this is to ensure that 1.0 == 1.0.0 in cmp(..)
        lenA, lenB = len(seqA), len(seqB)
        for i in range(lenA, lenB): seqA += (0,)
        for i in range(lenB, lenA): seqB += (0,)

        rc = cmp(seqA, seqB)

        if rc == 0:
            if vA.endswith('-SNAPSHOT'): return -1
            if vB.endswith('-SNAPSHOT'): return 1
        return rc

    # dl the first 256 bytes and parse it for version number
    try:
        http_stream = urllib.urlopen(dl_url)
        update_file = http_stream.read(256)
        http_stream.close()
    except IOError, (errno, strerror):
        print "Unable to retrieve version data"
        print "Error %s: %s" % (errno, strerror)
        return

    match_regex = re.search(r'__version__ *= *"(\S+)"', update_file)
    if not match_regex:
        print "No version info could be found"
        return
    update_version = match_regex.group(1)

    if not update_version:
        print "Unable to parse version data"
        return

    if force_update:
        print "Forcing update, downloading version %s..." \
            % update_version
    else:
        cmp_result = compare_versions(__version__, update_version)
        if cmp_result < 0:
            print "Newer version %s available, downloading..." % update_version
        elif cmp_result > 0:
            print "Local version %s newer then available %s, not updating." \
                % (__version__, update_version)
            return
        else:
            print "You already have the latest version."
            return

    # dl, backup, and save the updated script
    app_path = os.path.realpath(sys.argv[0])

    if not os.access(app_path, os.W_OK):
        print "Cannot update -- unable to write to %s" % app_path

    dl_path = app_path + ".new"
    backup_path = app_path + ".old"
    try:
        dl_file = open(dl_path, 'w')
        http_stream = urllib.urlopen(dl_url)
        total_size = None
        bytes_so_far = 0
        chunk_size = 8192
        try:
            total_size = int(http_stream.info().getheader('Content-Length').strip())
        except:
            # The header is improper or missing Content-Length, just download
            dl_file.write(http_stream.read())

        while total_size:
            chunk = http_stream.read(chunk_size)
            dl_file.write(chunk)
            bytes_so_far += len(chunk)

            if not chunk:
                break

            percent = float(bytes_so_far) / total_size
            percent = round(percent*100, 2)
            sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" %
                (bytes_so_far, total_size, percent))

            if bytes_so_far >= total_size:
                sys.stdout.write('\n')

        http_stream.close()
        dl_file.close()
    except IOError, (errno, strerror):
        print "Download failed"
        print "Error %s: %s" % (errno, strerror)
        return

    try:
        if os.path.isfile(backup_path):
            os.remove(backup_path)
        os.rename(app_path, backup_path)
    except OSError, (errno, strerror):
        print "Unable to rename %s to %s: (%d) %s" \
            % (app_path, backup_path, errno, strerror)
        return

    try:
        os.rename(dl_path, app_path)
    except OSError, (errno, strerror):
        print "Unable to rename %s to %s: (%d) %s" \
            % (dl_path, app_path, errno, strerror)
        return

    try:
        import shutil
        shutil.copymode(backup_path, app_path)
    except:
        os.chmod(app_path, 0755)

    print "New version installed as %s" % app_path
    print "(previous version backed up to %s)" % (backup_path)
    return
