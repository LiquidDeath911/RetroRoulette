# Made by LiquidDeath911 for his bud TigeltoN
#
# This script is for keeping a record of what number a user
# picks for TigeltoN's Retro Roulette streams on Twitch

## IMPORTS ##
import sys
import json
import os
import ctypes
import codecs
import random

## SCRIPT INFO ##
ScriptName = "Retro Roulette"
Website = "https://github.com/LiquidDeath911/RetroRoulette"
Description = "Retro Roulette for Streamlabs Chatbot"
Creator = "LiquidDeath911"
Version = "2.2.0"

## GLOBAL VARIABLES ##
# file paths
path = os.path.dirname(__file__)
consoleListsPath = os.path.join(path, "ConsoleLists")
responseListsPath = os.path.join(path, "ResponseLists")
gameListsPath = os.path.join(path, "GameLists")

# defaults
settings = {}
liveOnly = True
isRouletteStarted = False
keepTrack = False

# json files
bannedList = []
commands = {}
permissions = {}

# game lists
n64GameList = []
snesGameList = []
nesGameList = []
gbGameList = []
genGameList = []

# user and number lists
userList = []
userNumbers = []
usersPicked = []
numbersPicked = []

# console number lists
n64NumberList = []
snesNumberList = []
nesNumberList = []
gbNumberList = []
genNumberList = []

# current elements and lists
currentConsoleList = []
currentGameList = []
currentConsole = ""
currentMode = ""
currentUser = ""
currentGame = ""
currentNum = 0
consoleMax = 0
refundUser = False
refundedUser = ""

# random response lists
numberAlreadyPickedResponses = []
userLeavesQueueResponses = []
userGotPickedResponses = []
userPickedNumberResponses = []
nextButQueueEmptyResponses = []
numberOutOfBoundsResponses = []

## FUNCTIONS ##
# Init Function
def Init():
    global settings, commands, permissions, bannedList, currentMode, keepTrack, liveOnly, consoleMax, currentConsole, currentConsoleList, currentGameList, refundUser
    global snesNumberList, snesGameList, n64NumberList, n64GameList, nesNumberList, nesGameList, gbNumberList, gbGameList, genNumberList, genGameList
    global userGotPickedResponses, numberAlreadyPickedResponses, numberAlreadyPickedResponses, nextButQueueEmptyResponses, userPickedNumberResponses, userLeavesQueueResponses, numberOutOfBoundsResponses

    try:
        with codecs.open(os.path.join(path, "config.json"), encoding='utf-8-sig', mode='r') as file:
            settings = json.load(file, encoding='utf-8-sig')
    except:
        LoadDefaults()
    
    with open(os.path.join(path, "commands.json"), 'r') as filehandle:
        com = filehandle.read()
    commands = json.loads(com)

    with open(os.path.join(path, "permissions.json"), 'r') as filehandle:
        perm = filehandle.read()
    permissions = json.loads(perm)

    with open(os.path.join(path, "bannedList.json"), 'r') as filehandle:
        bannedList = json.load(filehandle)

    with open(os.path.join(consoleListsPath, "snesNumberList.json"), 'r') as filehandle:
        snesNumberList = json.load(filehandle)

    with open(os.path.join(consoleListsPath, "n64NumberList.json"), 'r') as filehandle:
        n64NumberList = json.load(filehandle)

    with open(os.path.join(consoleListsPath, "nesNumberList.json"), 'r') as filehandle:
        nesNumberList = json.load(filehandle)

    with open(os.path.join(consoleListsPath, "gbNumberList.json"), 'r') as filehandle:
        gbNumberList = json.load(filehandle)

    with open(os.path.join(consoleListsPath, "genNumberList.json"), 'r') as filehandle:
        genNumberList = json.load(filehandle)

    with open(os.path.join(gameListsPath, "snesGameList.json"), 'r') as filehandle:
        snesGameList = json.load(filehandle)

    with open(os.path.join(gameListsPath, "n64GameList.json"), 'r') as filehandle:
        n64GameList = json.load(filehandle)

    with open(os.path.join(gameListsPath, "nesGameList.json"), 'r') as filehandle:
        nesGameList = json.load(filehandle)

    with open(os.path.join(gameListsPath, "gbGameList.json"), 'r') as filehandle:
        gbGameList = json.load(filehandle)

    with open(os.path.join(gameListsPath, "genGameList.json"), 'r') as filehandle:
        genGameList = json.load(filehandle)

    with open(os.path.join(responseListsPath, "userGotPickedResponses.json"), 'r') as filehandle:
        userGotPickedResponses = json.load(filehandle)

    with open(os.path.join(responseListsPath, "numberAlreadyPickedResponses.json"), 'r') as filehandle:
        numberAlreadyPickedResponses = json.load(filehandle)

    with open(os.path.join(responseListsPath, "nextButQueueEmptyResponses.json"), 'r') as filehandle:
        nextButQueueEmptyResponses = json.load(filehandle)

    with open(os.path.join(responseListsPath, "userPickedNumberResponses.json"), 'r') as filehandle:
        userPickedNumberResponses = json.load(filehandle)

    with open(os.path.join(responseListsPath, "userLeavesQueueResponses.json"), 'r') as filehandle:
        userLeavesQueueResponses = json.load(filehandle)

    with open(os.path.join(responseListsPath, "numberOutOfBoundsResponses.json"), 'r') as filehandle:
        numberOutOfBoundsResponses = json.load(filehandle)

    currentMode = settings["defaultMode"]

    keepTrack = settings["keepTrack"]
    liveOnly = settings["liveOnly"]
    refundUser = False

    if settings["defaultConsole"].lower() == "snes":
        consoleMax = 725
        currentConsole = "SNES"
        currentConsoleList = snesNumberList
        currentGameList = snesGameList
    elif settings["defaultConsole"].lower() == "nes":
        consoleMax = 677
        currentConsole = "NES"
        currentConsoleList = nesNumberList
        currentGameList = nesGameList
    elif settings["defaultConsole"].lower() == "n64":
        consoleMax = 296
        currentConsole = "N64"
        currentConsoleList = n64NumberList
        currentGameList = n64GameList
    elif settings["defaultConsole"].lower() == "gb":
        consoleMax = 582
        currentConsole = "GB"
        currentConsoleList = gbNumberList
        currentGameList = gbGameList
    elif settings["defaultConsole"].lower() == "gen":
        consoleMax = 700
        currentConsole = "GEN"
        currentConsoleList = genNumberList
        currentGameList = genGameList
    return

# Execute Function
def Execute(data):
    
    # This 'if' checks for the following: chat message = command, username NOT in banned list, stream = live (if that setting is enabled)
    if data.IsChatMessage() and ((data.GetParam(0).lower() in commands.values()) or (data.GetParam(0).lower() == "!commands")) and not (data.UserName.lower().lower() in bannedList) and ((liveOnly and Parent.IsLive()) or (not liveOnly or data.UserName == "LiquidDeath911")):

        # Each of the following if functions checks the chat message to see what command it is using and if the user has permission to use that command
        
        ## BAN COMMAND ##
        if data.IsChatMessage() and (data.GetParam(0).lower() == commands["banCommand"]) and (Parent.HasPermission(data.User, permissions["banPermission"], "") or data.UserName == "LiquidDeath911"):
            BanCommand(data)

        ## CONSOLE COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["consoleCommand"]) and (Parent.HasPermission(data.User, permissions["consolePermission"], "") or data.UserName == "LiquidDeath911"):
            ConsoleCommand(data)

        ## CURRENT COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["currentCommand"]) and (Parent.HasPermission(data.User, permissions["currentPermission"], "") or data.UserName == "LiquidDeath911"):
            CurrentCommand(data)

        ## END COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["endCommand"]) and (Parent.HasPermission(data.User, permissions["endPermission"], "") or data.UserName == "LiquidDeath911"):
            EndCommand(data)

        ## INFO COMMAND ##
        elif data.IsChatMessage() and ((data.GetParam(0).lower() == commands["infoCommand"]) or (data.GetParam(0).lower() == "!commands")) and (Parent.HasPermission(data.User, permissions["infoPermission"], "") or data.UserName == "LiquidDeath911"):
            InfoCommand(data)

        ## LEAVE COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["leaveCommand"]) and (Parent.HasPermission(data.User, permissions["leavePermission"], "") or data.UserName == "LiquidDeath911"):
            LeaveCommand(data)

        ## MAX COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["maxCommand"]) and (Parent.HasPermission(data.User, permissions["maxPermission"], "") or data.UserName == "LiquidDeath911"):
            MaxCommand(data)

        ## MODE COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["modeCommand"]) and (Parent.HasPermission(data.User, permissions["modePermission"], "") or data.UserName == "LiquidDeath911"):
            ModeCommand(data)
            
        ## NEXT COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["nextCommand"]) and (Parent.HasPermission(data.User, permissions["nextPermission"], "") or data.UserName == "LiquidDeath911"):
            NextCommand(data)

        ## NO REFUND COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["noRefundCommand"]) and (Parent.HasPermission(data.User, permissions["noRefundPermission"], "") or data.UserName == "LiquidDeath911"):
            NoRefundCommand(data)

        ## PICK COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["pickCommand"]) and (Parent.HasPermission(data.User, permissions["pickPermission"], "") or data.UserName == "LiquidDeath911"):
            PickCommand(data)

        ## QUEUE COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["queueCommand"]) and (Parent.HasPermission(data.User, permissions["queuePermission"], "") or data.UserName == "LiquidDeath911"):
            QueueCommand(data)

        ## REFUND COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["refundCommand"]) and (Parent.HasPermission(data.User, permissions["refundPermission"], "") or data.UserName == "LiquidDeath911"):
            RefundCommand(data)

        ## RESET COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["resetCommand"]) and (Parent.HasPermission(data.User, permissions["resetPermission"], "") or data.UserName == "LiquidDeath911"):
            ResetCommand(data)

        ## RESET CONSOLE COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["resetConsoleCommand"]) and (Parent.HasPermission(data.User, permissions["resetConsolePermission"], "") or data.UserName == "LiquidDeath911"):
            ResetConsoleCommand(data)

        ## RESTART COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["restartCommand"]) and (Parent.HasPermission(data.User, permissions["restartPermission"], "") or data.UserName == "LiquidDeath911"):
            RestartCommand(data)

        ## SHUFFLE COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["shuffleCommand"]) and (Parent.HasPermission(data.User, permissions["shufflePermission"], "") or data.UserName == "LiquidDeath911"):
            ShuffleCommand(data)

        ## SPOT COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["spotCommand"]) and (Parent.HasPermission(data.User, permissions["spotPermission"], "") or data.UserName == "LiquidDeath911"):
            SpotCommand(data)

        ## START COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["startCommand"]) and (Parent.HasPermission(data.User, permissions["startPermission"], "") or data.UserName == "LiquidDeath911"):
            StartCommand(data)

        ## UNBAN COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["unbanCommand"]) and (Parent.HasPermission(data.User, permissions["unbanPermission"], "") or data.UserName == "LiquidDeath911"):
            UnbanCommand(data)

        ## UPDATE COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["updateCommand"]) and (Parent.HasPermission(data.User, permissions["updatePermission"], "") or data.UserName == "LiquidDeath911"):
            UpdateCommand(data)

        ## WHO COMMAND ##
        elif data.IsChatMessage() and (data.GetParam(0).lower() == commands["whoCommand"]) and (Parent.HasPermission(data.User, permissions["whoPermission"], "") or data.UserName == "LiquidDeath911"):
            WhoCommand(data)

    return

# BanCommand Function
def BanCommand(data):
    global bannedList
    ## LOCAL VARIABLES ##
    outputMessage = ""
    toBan = ""

    # reading bannedList file
    with open(os.path.join(path, "bannedList.json"), 'r') as filehandle:
        bannedList = json.load(filehandle)

    # checking to make sure there is an argument after the command
    if (data.GetParamCount() == 2):
        try:
            # username read from chat message, changed to all lowercase letters
            toBan = data.GetParam(1).lower()
        except:
            return

        toBan = toBan.replace("@", "")
        
        # This 'if' checks to see if user is already in bannedList
        if not (toBan in bannedList):
            # username added to ban list, all lowercase letters
            bannedList.append(toBan)
            outputMessage = settings["banResponse"]
            outputMessage = outputMessage.replace("$user", toBan)

    else:
        return

    Parent.SendStreamMessage(outputMessage)

    # writing to bannedList file after changes
    with open(os.path.join(path, "bannedList.json"), 'w') as filehandle:
        json.dump(bannedList, filehandle)

    return

# ConsoleCommand Function
def ConsoleCommand(data):
    global consoleMax, currentConsole, currentConsoleList, currentGameList, userNumbers, userList
    ## LOCAL VARIABLES ##
    outputMessage = ""
    outputMessage2 = ""
    username = data.UserName.lower()
    console = ""
    outOfBounds = 0
    unluckyUser = ""

    if (data.GetParamCount() == 2):
        try:
            console = data.GetParam(1)
        except:
            console = defaultConsole

        if console.lower() == "snes":
            consoleMax = 725
            currentConsole = "SNES"
            currentConsoleList = snesNumberList
            currentGameList = snesGameList
        elif console.lower() == "nes":
            consoleMax = 677
            currentConsole = "NES"
            currentConsoleList = nesNumberList
            currentGameList = nesGameList
        elif console.lower() == "n64":
            consoleMax = 296
            currentConsole = "N64"
            currentConsoleList = n64NumberList
            currentGameList = n64GameList
        elif console.lower() == "gb":
            consoleMax = 582
            currentConsole = "GB"
            currentConsoleList = gbNumberList
            currentGameList = gbGameList
        elif (console.lower() == "gen") or (console.lower() == "genesis"):
            consoleMax = 700
            currentConsole = "GEN"
            currentConsoleList = genNumberList
            currentGameList = genGameList
        else:
            outputMessage = settings["consoleNotChangedResponse"]
            outputMessage = outputMessage.replace("$user", username)
            outputMessage = outputMessage.replace("$consoleCommand", commands["consoleCommand"])

            Parent.SendStreamMessage(outputMessage)

            return

        for num in userNumbers:
            if num > consoleMax:
                outOfBounds = userNumbers.index(num)
                unluckyUser = userList.pop(outOfBounds)
                userNumbers.pop(outOfBounds)
                outputMessage2 = settings["removedResponse"]
                outputMessage2 = outputMessage.replace("$user", unluckyUser)
                Parent.SendStreamMessage(outputMessage2)

        outputMessage = settings["consoleChangedResponse"]
        outputMessage = outputMessage.replace("$user", username)
        outputMessage = outputMessage.replace("$console", currentConsole)

    else:
        outputMessage = settings["consoleNotChangedResponse"]
        outputMessage = outputMessage.replace("$user", username)
        outputMessage = outputMessage.replace("$consoleCommand", commands["consoleCommand"])

    Parent.SendStreamMessage(outputMessage)

    return

# CurrentCommand Function
def CurrentCommand(data):
    ## LOCAL VARIABLES ##
    outputMessage = ""
    username = data.UserName.lower()

    if not isRouletteStarted:
        outputMessage = settings["noRouletteResponse"]
        outputMessage = outputMessage.replace("$user", username)
    else:
        outputMessage = settings["currentResponse"]
        outputMessage = outputMessage.replace("$user", currentUser)
        outputMessage = outputMessage.replace("$game", currentGame)

    Parent.SendStreamMessage(outputMessage)

    return

# EndCommand Function
def EndCommand(data):
    global isRouletteStarted, userList, userNumbers, usersPicked, numbersPicked
    ## LOCAL VARIABLES ##
    outputMessage = ""
    username = data.UserName.lower()

    if not isRouletteStarted:
        outputMessage = settings["alreadyEndedResponse"]
        outputMessage = outputMessage.replace("$user", username)
    else:
        outputMessage = settings["endResponse"]
        isRouletteStarted = False
        userList = []
        userNumbers = []
        usersPicked = []
        numbersPicked = []

    Parent.SendStreamMessage(outputMessage)

    return

# InfoCommand Function
def InfoCommand(data):
    ## LOCAL VARIABLES ##
    outputMessage = ""

    outputMessage = "For info about Retro Roulette and its command list go here: https://pastebin.com/TxWA4CmS"

    Parent.SendStreamMessage(outputMessage)

    return

# LeaveCommand Function
def LeaveCommand(data):
    global userList, userNumbers, userLeavesQueueResponses
    ## LOCAL VARIABLES ##
    outputMessage = ""
    username = data.UserName.lower()
    userLeaving = 0

    if not isRouletteStarted:
        outputMessage = settings["noRouletteResponse"]
        outputMessage = outputMessage.replace("$user", username)
    elif (username in userList):
        userLeaving = userList.index(username)
        userList.pop(userLeaving)
        userNumbers.pop(userLeaving)
        with open(os.path.join(responseListsPath, "userLeavesQueueResponses.json"), 'r') as filehandle:
            userLeavesQueueResponses = json.load(filehandle)

        randLine = (Parent.GetRandom(1, len(userLeavesQueueResponses)) - 1)
        outputMessage = userLeavesQueueResponses[randLine]
        outputMessage = outputMessage.replace("$user", username)
    else:
        outputMessage = settings["notEnteredLeaveResponse"]
        outputMessage = outputMessage.replace("$user", username)

    Parent.SendStreamMessage(outputMessage)

    return

# MaxCommand Function
def MaxCommand(data):
    ## LOCAL VARIABLES ##
    outputMessage = ""
    username = data.UserName.lower()

    outputMessage = settings["maxResponse"]
    outputMessage = outputMessage.replace("$user", username)
    outputMessage = outputMessage.replace("$currentConsole", currentConsole)
    outputMessage = outputMessage.replace("$consoleMax", str(consoleMax))

    Parent.SendStreamMessage(outputMessage)

    return

# ModeCommand Function
def ModeCommand(data):
    global currentMode
    ## LOCAL VARIABLES ##
    outputMessage = ""
    username = data.UserName.lower()
    mode = ""

    if (data.GetParamCount() == 2):
        try:
            mode = data.GetParam(1)
        except:
            mode = currentMode

        if mode.lower() == "random":
            currentMode = "Random"
            outputMessage = settings["modeRandomResponse"]
        elif mode.lower() == "queue":
            currentMode = "Queue"
            outputMessage = settings["modeQueueResponse"]
        else:
            outputMessage = settings["modeNotChangedResponse"]
            outputMessage = outputMessage.replace("$user", username)
            outputMessage = outputMessage.replace("$modeCommand", commands["modeCommand"])

    else:
        outputMessage = settings["modeNotChangedResponse"]
        outputMessage = outputMessage.replace("$user", username)
        outputMessage = outputMessage.replace("$modeCommand", commands["modeCommand"])


    Parent.SendStreamMessage(outputMessage)

    return

# NextCommand Function
def NextCommand(data):
    global snesNumberList, nesNumberList, n64NumberList, gbNumberList, genNumberList
    global userPickedTextList, currentUser, currentNum, usersPicked, numbersPicked, currentGame, nextButQueueEmptyResponses, refundUser, refundedUser
    ## LOCAL VARIABLES ##
    outputMessage = ""
    username = data.UserName.lower()
    pickedUser = ""
    pickedGame = ""
    pickedNumber = 0
    rand = 0
    randLine = 0

    if not isRouletteStarted:
        outputMessage = settings["noRouletteResponse"]
        outputMessage = outputMessage.replace("$user", username)        
    elif (userList or userNumbers):
        with open(os.path.join(responseListsPath, "userGotPickedResponses.json"), 'r') as filehandle:
            userPickedTextList = json.load(filehandle)

        randLine = (Parent.GetRandom(1, len(userGotPickedResponses)) - 1)
        outputMessage = userGotPickedResponses[randLine]

        outputMessage2 = settings["notifyStreamerResponse"]

        if (refundUser):
            if (refundedUser in userList):
                refundedUserIndex = userList.index(refundedUser)
                pickedUser = userList.pop(refundedUserIndex)
                pickedNumber = userNumbers.pop(refundedUserIndex)
                refundUser = False
                refundedUser = ""
            else:
                outputMessage = "refundWaitResponse"
                outputMessage = outputMessage.replace("$user", username)
                outputMessage = outputMessage.replace("$noRefundCommand", commands["noRefundCommand"])
                Parent.SendStreamMessage(outputMessage)
                return
        elif currentMode == "Random":
            userMax = len(userList)
            rand = (Parent.GetRandom(1, userMax) - 1)
            pickedUser = userList.pop(rand)
            pickedNumber = userNumbers.pop(rand)
        else:
            pickedUser = userList.pop(0)
            pickedNumber = userNumbers.pop(0)

        currentUser = pickedUser
        currentNum = pickedNumber
        usersPicked.append(pickedUser)
        numbersPicked.append(pickedNumber)
        pickedGame = currentGameList[pickedNumber]
        currentGame = pickedGame

        if keepTrack:
            if currentConsole.lower() == "snes":
                with open(os.path.join(consoleListsPath, "snesNumberList.json"), 'r') as filehandle:
                    snesNumberList = json.load(filehandle)
                snesNumberList.append(pickedNumber)
                with open(os.path.join(consoleListsPath, "snesNumberList.json"), 'w') as filehandle:
                    json.dump(snesNumberList, filehandle)
            elif currentConsole.lower() == "nes":
                with open(os.path.join(consoleListsPath, "nesNumberList.json"), 'r') as filehandle:
                    nesNumberList = json.load(filehandle)
                nesNumberList.append(pickedNumber)
                with open(os.path.join(consoleListsPath, "nesNumberList.json"), 'w') as filehandle:
                    json.dump(nesNumberList, filehandle)
            elif currentConsole.lower() == "n64":
                with open(os.path.join(consoleListsPath, "n64NumberList.json"), 'r') as filehandle:
                    n64NumberList = json.load(filehandle)
                n64NumberList.append(pickedNumber)
                with open(os.path.join(consoleListsPath, "n64NumberList.json"), 'w') as filehandle:
                    json.dump(n64NumberList, filehandle)
            elif currentConsole.lower() == "gb":
                with open(os.path.join(consoleListsPath, "gbNumberList.json"), 'r') as filehandle:
                    gbNumberList = json.load(filehandle)
                gbNumberList.append(pickedNumber)
                with open(os.path.join(consoleListsPath, "gbNumberList.json"), 'w') as filehandle:
                    json.dump(gbNumberList, filehandle)
            elif currentConsole.lower() == "gen":
                with open(os.path.join(consoleListsPath, "genNumberList.json"), 'r') as filehandle:
                    genNumberList = json.load(filehandle)
                genNumberList.append(pickedNumber)
                with open(os.path.join(consoleListsPath, "genNumberList.json"), 'w') as filehandle:
                    json.dump(genNumberList, filehandle)

        outputMessage = outputMessage.replace("$user", pickedUser)
        outputMessage2 = outputMessage2.replace("$user", username)
        outputMessage2 = outputMessage2.replace("$game", currentGame)

        Parent.SendStreamMessage(outputMessage2)

    elif not (userList or userNumbers):
        with open(os.path.join(responseListsPath, "nextButQueueEmptyResponses.json"), 'r') as filehandle:
            nextButQueueEmptyResponses = json.load(filehandle)

        randLine = (Parent.GetRandom(1, len(nextButQueueEmptyResponses)) - 1)
        outputMessage = nextButQueueEmptyResponses[randLine]
        outputMessage = outputMessage.replace("$user", username)

    Parent.SendStreamMessage(outputMessage)

    return

# NoRefundCommand Function
def NoRefundCommand(data):
    global refundUser
    ## LOCAL VARIABLES ##
    outputMessage = ""
    if not isRouletteStarted:
        outputMessage = settings["noRouletteResponse"]
        outputMessage = outputMessage.replace("$user", username)
    else:
        refundUser = False
        outputMessage = "No Refunds!"
    
    Parent.SendStreamMessage(outputMessage)
    return

# PickCommand Function
def PickCommand(data):
    global userList, userNumbers, userPickedNumberResponses, numberAlreadyPickedResponses, numberOutOfBoundsResponses
    ## LOCAL VARIABLES ##
    outputMessage = ""
    username = data.UserName.lower()
    number = 0
    rand = 0
    randLine = 0

    if not isRouletteStarted:
        outputMessage = settings["noRouletteResponse"]
        outputMessage = outputMessage.replace("$user", username)
    elif (data.GetParamCount() == 2) and not (username in userList) and not (username in usersPicked):
        try:
            number = int(data.GetParam(1))
        except:
            if data.GetParam(1) == 'random':
                number = Parent.GetRandom(1, consoleMax)
                while (number in userNumbers) or (number in numbersPicked) or (keepTrack and(number in currentConsoleList)):
                    number = Parent.GetRandom(1, consoleMax)

                userList.append(username)
                userNumbers.append(number)
                with open(os.path.join(responseListsPath, "userPickedNumberResponses.json"), 'r') as filehandle:
                    userPickedNumberResponses = json.load(filehandle)

                randLine = (Parent.GetRandom(1, len(userPickedNumberResponses)) - 1)
                outputMessage = userPickedNumberResponses[randLine]
                outputMessage = outputMessage.replace("$user", username)
                outputMessage = outputMessage.replace("$number", str(number))
                rand = Parent.GetRandom(1, consoleMax)
                outputMessage = outputMessage.replace("$rand", str(rand))
            else:
                outputMessage = settings["invalidNumberResponse"]
                outputMessage = outputMessage.replace("$user", username)
                outputMessage = outputMessage.replace("$consoleMax", str(consoleMax))

            Parent.SendStreamMessage(outputMessage)

            return

        if (number in userNumbers) or (number in numbersPicked) or (keepTrack and(number in currentConsoleList)):
            if (keepTrack and(number in currentConsoleList)):
                outputMessage = settings["alreadyPickedPreviousStreamResponse"]
                outputMessage = outputMessage.replace("$user", username)
            else:
                with open(os.path.join(responseListsPath, "numberAlreadyPickedResponses.json"), 'r') as filehandle:
                    numberAlreadyPickedResponses = json.load(filehandle)

                randLine = (Parent.GetRandom(1, len(numberAlreadyPickedResponses)) - 1)
                outputMessage = numberAlreadyPickedResponses[randLine]
                outputMessage = outputMessage.replace("$user", username)

        elif (number > consoleMax) or (number < 1):
            if (number > consoleMax):
                with open(os.path.join(responseListsPath, "numberOutOfBoundsResponses.json"), 'r') as filehandle:
                    numberOutOfBoundsResponses = json.load(filehandle)

                randLine = (Parent.GetRandom(1, len(numberOutOfBoundsResponses)) - 1)
                outputMessage = numberOutOfBoundsResponses[randLine]
                outputMessage = outputMessage.replace("$user", username)
                outputMessage = outputMessage.replace("$consoleMax", str(consoleMax))
            else:
                outputMessage = settings["lessThanOneResponse"]
                outputMessage = outputMessage.replace("$user", username)
        else:
            userList.append(username)
            userNumbers.append(number)
            with open(os.path.join(responseListsPath, "userPickedNumberResponses.json"), 'r') as filehandle:
                userPickedNumberResponses = json.load(filehandle)

            randLine = (Parent.GetRandom(1, len(userPickedNumberResponses)) - 1)
            outputMessage = userPickedNumberResponses[randLine]
            outputMessage = outputMessage.replace("$user", username)
            outputMessage = outputMessage.replace("$user", username)
            outputMessage = outputMessage.replace("$number", str(number))

    elif (username in userList) or (username in usersPicked):
        if (username in usersPicked):
            outputMessage = settings["alreadyPickedResponse"]
            outputMessage = outputMessage.replace("$user", username)
        elif (username in userList):
            outputMessage = settings["alreadyEnteredResponse"]
            outputMessage = outputMessage.replace("$user", username)
    else:
        outputMessage = settings["noNumberResponse"]
        outputMessage = outputMessage.replace("$user", username)
        outputMessage = outputMessage.replace("$pickCommand", commands["pickCommand"])

    Parent.SendStreamMessage(outputMessage)

    return

# QueueCommand Function
def QueueCommand(data):
    ## LOCAL VARIABLES ##
    outputMessage = ""
    username = data.UserName.lower()
    total = 0

    if not isRouletteStarted:
        outputMessage = settings["noRouletteResponse"]
        outputMessage = outputMessage.replace("$user", username)
    elif currentMode == "Random":
        outputMessage = settings["queueRandomResponse"]
        total = len(userList)
        outputMessage = outputMessage.replace("$total", str(total))
    elif currentMode == "Queue":
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

# RefundCommand Function
def RefundCommand(data):
    global refundUser, usersPicked, numbersPicked, refundedUser
    ## LOCAL VARIABLES ##
    outputMessage = ""
    username = data.UserName.lower()

    if not isRouletteStarted:
        outputMessage = settings["noRouletteResponse"]
        outputMessage = outputMessage.replace("$user", username)
    elif (data.GetParamCount() == 2):
        try:
            refundedUser = data.GetParam(1).lower()
        except:
            outputMessage = settings["refundFailedResponse"]
            outputMessage = outputMessage.replace("$user", username)
            
            Parent.SendStreamMessage(outputMessage)
            return

        refundedUser = refundedUser.replace("@", "")
        refundUser = True
        refundedUserIndex = usersPicked.index(refundedUser)
        usersPicked.pop(refundedUserIndex)

        outputMessage = settings["refundResponse"]
        outputMessage = outputMessage.replace("$user", refundedUser)
        
    else:
        outputMessage = settings["refundFailedResponse"]
        outputMessage = outputMessage.replace("$user", username)


    Parent.SendStreamMessage(outputMessage)
    return


# ResetCommand Function
def ResetCommand(data):
    global usersPicked
    ## LOCAL VARIABLES ##
    outputMessage = ""
    username = data.UserName.lower()

    if not isRouletteStarted:
        outputMessage = settings["noRouletteResponse"]
        outputMessage = outputMessage.replace("$user", username)
    elif not (userList) and not (userNumbers):
        outputMessage = settings["resetResponse"]
        usersPicked = []
    elif (userList or userNumbers):
        outputMessage = settings["notEmptyResponse"]
        outputMessage = outputMessage.replace("$user", username)
        outputMessage = outputMessage.replace("$nextCommand", commands["nextCommand"])
        outputMessage = outputMessage.replace("$restartCommand", commands["restartCommand"])

    Parent.SendStreamMessage(outputMessage)

    return

# ResetConsoleCommand Function
def ResetConsoleCommand(data):
    global snesNumberList, nesNumberList, n64NumberList, gbNumberList, genNumberList
    ## LOCAL VARIABLES ##
    outputMessage = ""
    username = data.UserName.lower()
    console = ""

    if (data.GetParamCount() == 2):
        try:
            console = data.GetParam(1)
        except:
            outputMessage = settings["consoleNotResetResponse"]
            outputMessage = outputMessage.replace("$user", username)
            outputMessage = outputMessage.replace("$resetConsoleCommand", commands["resetConsoleCommand"])

            Parent.SendStreamMessage(outputMessage)

            return

        if console.lower() == "snes":
            snesNumberList = []
            with open(os.path.join(consoleListsPath, "snesNumberList.json"), 'w') as filehandle:
                json.dump(snesNumberList, filehandle)
        elif console.lower() == "nes":
            nesNumberList = []
            with open(os.path.join(consoleListsPath, "nesNumberList.json"), 'w') as filehandle:
                json.dump(nesNumberList, filehandle)
        elif console.lower() == "n64":
            n64NumberList = []
            with open(os.path.join(consoleListsPath, "n64NumberList.json"), 'w') as filehandle:
                json.dump(n64NumberList, filehandle)
        elif console.lower() == "gb":
            gbNumberList = []
            with open(os.path.join(consoleListsPath, "gbNumberList.json"), 'w') as filehandle:
                json.dump(gbNumberList, filehandle)
        elif console.lower() == "gen":
            genNumberList = []
            with open(os.path.join(consoleListsPath, "genNumberList.json"), 'w') as filehandle:
                json.dump(genNumberList, filehandle)
        else:
            outputMessage = settings["consoleNotResetResponse"]
            outputMessage = outputMessage.replace("$user", username)
            outputMessage = outputMessage.replace("$resetConsoleCommand", commands["resetConsoleCommand"])

            Parent.SendStreamMessage(outputMessage)

            return

        outputMessage = settings["consoleResetResponse"]
        outputMessage = outputMessage.replace("$user", username)
        outputMessage = outputMessage.replace("$console", console)

        Parent.SendStreamMessage(outputMessage)
    else:
        outputMessage = settings["consoleNotResetResponse"]
        outputMessage = outputMessage.replace("$user", username)
        outputMessage = outputMessage.replace("$resetConsoleCommand", commands["resetConsoleCommand"])

        Parent.SendStreamMessage(outputMessage)

    return

# RestartCommand Function
def RestartCommand(data):
    global userList, userNumbers, usersPicked
    ## LOCAL VARIABLES ##
    outputMessage = ""
    username = data.UserName.lower()

    if not isRouletteStarted:
        outputMessage = settings["noRouletteResponse"]
        outputMessage = outputMessage.replace("$user", username)
    elif (userList or userNumbers):
        outputMessage = settings["restartResponse"]
        userList = []
        userNumbers = []
        usersPicked = []
    elif not (userList) and not (userNumbers):
        outputMessage = settings["resetResponse"]
        usersPicked = []

    Parent.SendStreamMessage(outputMessage)

    return

# ShuffleCommand Function
def ShuffleCommand(data):
    global snesGameList, nesGameList, n64GameList, gbGameList, genGameList, currentGameList, snesNumberList, nesNumberList, n64NumberList, gbNumberList, genNumberList
    ## LOCAL VARIABLES ##
    outputMessage = ""
    username = data.UserName.lower()
    console = ""

    if (data.GetParamCount() == 2):
        try:
            console = data.GetParam(1)
        except:
            outputMessage = settings["shuffleFailedResponse"]
            outputMessage = outputMessage.replace("$user", username)
            outputMessage = outputMessage.replace("$shuffleCommand", commands["shuffleCommand"])

            Parent.SendStreamMessage(outputMessage)

            return

        if console.lower() == "snes":
            with open(os.path.join(gameListsPath, "snesGameListOriginal.json"), 'r') as filehandle:
                snesGameList = json.load(filehandle)
            random.shuffle(snesGameList)
            currentGameList = snesGameList
            with open(os.path.join(gameListsPath, "snesGameList.json"), 'w') as filehandle:
                json.dump(snesGameList, filehandle)
            snesNumberList = []
            with open(os.path.join(consoleListsPath, "snesNumberList.json"), 'w') as filehandle:
                json.dump(snesNumberList, filehandle)
        elif console.lower() == "nes":
            with open(os.path.join(gameListsPath, "nesGameListOriginal.json"), 'r') as filehandle:
                nesGameList = json.load(filehandle)
            random.shuffle(nesGameList)
            currentGameList = nesGameList
            with open(os.path.join(gameListsPath, "nesGameList.json"), 'w') as filehandle:
                json.dump(nesGameList, filehandle)
            nesNumberList = []
            with open(os.path.join(consoleListsPath, "nesNumberList.json"), 'w') as filehandle:
                json.dump(nesNumberList, filehandle)
        elif console.lower() == "n64":
            with open(os.path.join(gameListsPath, "n64GameListOriginal.json"), 'r') as filehandle:
                n64GameList = json.load(filehandle)
            random.shuffle(n64GameList)
            currentGameList = n64GameList
            with open(os.path.join(gameListsPath, "n64GameList.json"), 'w') as filehandle:
                json.dump(n64GameList, filehandle)
            n64NumberList = []
            with open(os.path.join(consoleListsPath, "n64NumberList.json"), 'w') as filehandle:
                json.dump(n64NumberList, filehandle)
        elif console.lower() == "gb":
            with open(os.path.join(gameListsPath, "gbGameListOriginal.json"), 'r') as filehandle:
                gbGameList = json.load(filehandle)
            random.shuffle(gbGameList)
            currentGameList = gbGameList
            with open(os.path.join(gameListsPath, "gbGameList.json"), 'w') as filehandle:
                json.dump(gbGameList, filehandle)
            gbNumberList = []
            with open(os.path.join(consoleListsPath, "gbNumberList.json"), 'w') as filehandle:
                json.dump(gbNumberList, filehandle)
        elif console.lower() == "gen":
            with open(os.path.join(gameListsPath, "genGameListOriginal.json"), 'r') as filehandle:
                genGameList = json.load(filehandle)
            random.shuffle(genGameList)
            currentGameList = genGameList
            with open(os.path.join(gameListsPath, "genGameList.json"), 'w') as filehandle:
                json.dump(genGameList, filehandle)
            genNumberList = []
            with open(os.path.join(consoleListsPath, "genNumberList.json"), 'w') as filehandle:
                json.dump(genNumberList, filehandle)
        elif console.lower() == "all":
            with open(os.path.join(gameListsPath, "snesGameListOriginal.json"), 'r') as filehandle:
                snesGameList = json.load(filehandle)
            random.shuffle(snesGameList)
            currentGameList = snesGameList
            with open(os.path.join(gameListsPath, "snesGameList.json"), 'w') as filehandle:
                json.dump(snesGameList, filehandle)
            snesNumberList = []
            with open(os.path.join(consoleListsPath, "snesNumberList.json"), 'w') as filehandle:
                json.dump(snesNumberList, filehandle)

            with open(os.path.join(gameListsPath, "nesGameListOriginal.json"), 'r') as filehandle:
                nesGameList = json.load(filehandle)
            random.shuffle(nesGameList)
            currentGameList = nesGameList
            with open(os.path.join(gameListsPath, "nesGameList.json"), 'w') as filehandle:
                json.dump(nesGameList, filehandle)
            nesNumberList = []
            with open(os.path.join(consoleListsPath, "nesNumberList.json"), 'w') as filehandle:
                json.dump(nesNumberList, filehandle)

            with open(os.path.join(gameListsPath, "n64GameListOriginal.json"), 'r') as filehandle:
                n64GameList = json.load(filehandle)
            random.shuffle(n64GameList)
            currentGameList = n64GameList
            with open(os.path.join(gameListsPath, "n64GameList.json"), 'w') as filehandle:
                json.dump(n64GameList, filehandle)
            n64NumberList = []
            with open(os.path.join(consoleListsPath, "n64NumberList.json"), 'w') as filehandle:
                json.dump(n64NumberList, filehandle)

            with open(os.path.join(gameListsPath, "gbGameListOriginal.json"), 'r') as filehandle:
                gbGameList = json.load(filehandle)
            random.shuffle(gbGameList)
            currentGameList = gbGameList
            with open(os.path.join(gameListsPath, "gbGameList.json"), 'w') as filehandle:
                json.dump(gbGameList, filehandle)
            gbNumberList = []
            with open(os.path.join(consoleListsPath, "gbNumberList.json"), 'w') as filehandle:
                json.dump(gbNumberList, filehandle)
            
            with open(os.path.join(gameListsPath, "genGameListOriginal.json"), 'r') as filehandle:
                genGameList = json.load(filehandle)
            random.shuffle(genGameList)
            currentGameList = genGameList
            with open(os.path.join(gameListsPath, "genGameList.json"), 'w') as filehandle:
                json.dump(genGameList, filehandle)
            genNumberList = []
            with open(os.path.join(consoleListsPath, "genNumberList.json"), 'w') as filehandle:
                json.dump(genNumberList, filehandle)
        else:
            outputMessage = settings["shuffleFailedResponse"]
            outputMessage = outputMessage.replace("$user", username)
            outputMessage = outputMessage.replace("$shuffleCommand", commands["shuffleCommand"])

            Parent.SendStreamMessage(outputMessage)

            return

        outputMessage = settings["shuffleResponse"]
        outputMessage = outputMessage.replace("$user", username)
        if (console == "all"):
            outputMessage = outputMessage.replace("$console", "all consoles")
        else:
            outputMessage = outputMessage.replace("$console", console)

        Parent.SendStreamMessage(outputMessage)
    else:
        outputMessage = settings["shuffleFailedResponse"]
        outputMessage = outputMessage.replace("$user", username)
        outputMessage = outputMessage.replace("$shuffleCommand", commands["shuffleCommand"])

        Parent.SendStreamMessage(outputMessage)

    return

# SpotCommand Function
def SpotCommand(data):
    ## LOCAL VARIABLES ##
    outputMessage = ""
    username = data.UserName.lower()
    spot = 0
    total = 0

    if not isRouletteStarted:
        outputMessage = settings["noRouletteResponse"]
        outputMessage = outputMessage.replace("$user", username)
    elif (username in userList):
        total = len(userList)
        if currentMode == "Queue":
            spot = userList.index(username) + 1
            outputMessage = settings["spotResponse"]
            outputMessage = outputMessage.replace("$user", username)
            outputMessage = outputMessage.replace("$spot", str(spot))
            outputMessage = outputMessage.replace("$total", str(total))
        else:
            outputMessage = settings["spotRandomResponse"]
            outputMessage = outputMessage.replace("$user", username)
            outputMessage = outputMessage.replace("$total", str(total))
    else:
        outputMessage = settings["notEnteredSpotResponse"]
        outputMessage = outputMessage.replace("$user", username)

    Parent.SendStreamMessage(outputMessage)

    return

# StartCommand Function
def StartCommand(data):
    global consoleMax, currentConsole, currentConsoleList, currentGameList, isRouletteStarted, userList, userNumbers, usersPicked, numbersPicked
    ## LOCAL VARIABLES ##
    outputMessage = ""
    username = data.UserName.lower()
    console = ""

    if not isRouletteStarted:
        if (data.GetParamCount() == 2):
            try:
                console = data.GetParam(1)
            except:
                outputMessage = settings["startNoConsoleResponse"]
                outputMessage = outputMessage.replace("$user", username)
                outputMessage = outputMessage.replace("$startCommand", commands["startCommand"])
                return

            if console.lower() == "snes":
                consoleMax = 725
                currentConsole = "SNES"
                currentConsoleList = snesNumberList
                currentGameList = snesGameList
            elif console.lower() == "nes":
                consoleMax = 677
                currentConsole = "NES"
                currentConsoleList = nesNumberList
                currentGameList = nesGameList
            elif console.lower() == "n64":
                consoleMax = 296
                currentConsole = "N64"
                currentConsoleList = n64NumberList
                currentGameList = n64GameList
            elif console.lower() == "gb":
                consoleMax = 582
                currentConsole = "GB"
                currentConsoleList = gbNumberList
                currentGameList = gbGameList
            elif (console.lower() == "gen") or (console.lower() == "genesis"):
                consoleMax = 700
                currentConsole = "GEN"
                currentConsoleList = genNumberList
                currentGameList = genGameList
            else:
                outputMessage = settings["startNoConsoleResponse"]
                outputMessage = outputMessage.replace("$user", username)
                outputMessage = outputMessage.replace("$startCommand", commands["startCommand"])
                return
            outputMessage = settings["startResponse"]
            outputMessage = outputMessage.replace("$console", currentConsole)
            outputMessage = outputMessage.replace("$pickCommand", commands["pickCommand"])
            isRouletteStarted = True
            userList = []
            userNumbers = []
            usersPicked = []
            numbersPicked = []
        else:
            outputMessage = settings["startNoConsoleResponse"]
            outputMessage = outputMessage.replace("$user", username)
            outputMessage = outputMessage.replace("$startCommand", commands["startCommand"])

    else:
        outputMessage = settings["alreadyStartedResponse"]
        outputMessage = outputMessage.replace("$user", username)

    Parent.SendStreamMessage(outputMessage)

    return

# UnbanCommand Function
def UnbanCommand(data):
    global bannedList
    ## LOCAL VARIABLES ##
    place = 0
    outputMessage = ""
    toUnBan = ""

    # reading bannedList file
    with open(os.path.join(path, "bannedList.json"), 'r') as filehandle:
        bannedList = json.load(filehandle)

    # checking to make sure there is an argument after the command
    if (data.GetParamCount() == 2):
        try:
            # username read from chat message, changed to all lowercase letters
            toUnBan = data.GetParam(1).lower()
        except:
            return

        toUnBan = toUnBan.replace("@", "")
        # This 'if' checks to see if user is in bannedList
        if (toUnBan in bannedList):
            # finding the index of the username
            place = bannedList.index(toUnBan)
            # popping username out of the list
            bannedList.pop(place)
            outputMessage = settings["unbanResponse"]
            outputMessage = outputMessage.replace("$user", toUnBan)

    else:
        return

    Parent.SendStreamMessage(outputMessage)

    # writing to bannedList file after changes
    with open(os.path.join(path, "bannedList.json"), 'w') as filehandle:
        json.dump(bannedList, filehandle)

    return

# UpdateCommand Function
def UpdateCommand(data):
    ## LOCAL VARIABLES ##
    outputMessage = ""

    if isRouletteStarted:
        outputMessage = "Please end Retro Roulette before updating."
        Parent.SendStreamMessage(outputMessage)
    else:
        outputMessage = "Updated."
        Parent.SendStreamMessage(outputMessage)
        Init()
    return

# WhoCommand Function
def WhoCommand(data):
    ## LOCAL VARIABLES ##
    outputMessage = ""
    username = data.UserName.lower()
    number = 0
    otherUser = ""
    whoIndex = 0
    whoNum = 0


    if not isRouletteStarted:
        outputMessage = settings["noRouletteResponse"]
        outputMessage = outputMessage.replace("$user", username)
    elif (data.GetParamCount() == 2):
        try:
            number = int(data.GetParam(1))
        except:
            otherUser = data.GetParam(1).lower()

            otherUser = otherUser.replace("@", "")

            if (otherUser in userList):
                whoIndex = userList.index(otherUser)
                whoNum = userNumbers[whoIndex]
                outputMessage = settings["whoByNameResponse"]
                outputMessage = outputMessage.replace("$user", otherUser)
                outputMessage = outputMessage.replace("$number", str(whoNum))
                Parent.SendStreamMessage(outputMessage)
                return
            elif (otherUser in usersPicked):
                whoIndex = usersPicked.index(otherUser)
                whoNum = numbersPicked[whoIndex]
                outputMessage = settings["whoByAlreadyPlayedNameResponse"]
                outputMessage = outputMessage.replace("$user", otherUser)
                outputMessage = outputMessage.replace("$number", str(whoNum))
                Parent.SendStreamMessage(outputMessage)
                return
            else:
                outputMessage = settings["whoNoneResponse"]
                Parent.SendStreamMessage(outputMessage)
                return
        if (number in userNumbers):
            whoNum = userNumbers.index(number)
            whoIndex = userList[whoNum]
            outputMessage = settings["whoByNumberResponse"]
            outputMessage = outputMessage.replace("$user", whoIndex)
            outputMessage = outputMessage.replace("$number", str(number))
        elif (number in numbersPicked):
            whoNum = numbersPicked.index(number)
            whoIndex = usersPicked[whoNum]
            outputMessage = settings["whoByAlreadyPlayedNumberResponse"]
            outputMessage = outputMessage.replace("$user", whoIndex)
            outputMessage = outputMessage.replace("$number", str(number))
        else:
            outputMessage = settings["whoNoneResponse"]
    else:
        if (username in userList):
            whoIndex = userList.index(username)
            whoNum = userNumbers[whoIndex]
            outputMessage = settings["whoSelfResponse"]
            outputMessage = outputMessage.replace("$user", username)
            outputMessage = outputMessage.replace("$number", str(whoNum))

        else:
            outputMessage = settings["whoNoneResponse"]

    Parent.SendStreamMessage(outputMessage)

    return

# LoadDefaults Function
def LoadDefaults():
    global settings
    settings = {
        "liveOnly": True,
        "keepTrack": False,
        "defaultMode": "Random",
        "defaultConsole": "SNES",
        "startResponse" : "Retro Roulette for $console has started! Use $pickCommand followed by a number to enter!",
        "startNoConsoleResponse" : "@$user, you must put the console name after $startCommand",
        "endResponse" : "Retro Roulette has ended. Better luck next time!",
        "resetResponse" : "Retro Roulette has been reset, everyone can pick numbers again!",
        "restartResponse" : "Retro Roulette has been restarted. The queue is now empty and everyone can pick numbers again!",
        "modeRandomResponse" : "Retro Roulette's mode has been changed to random!",
        "modeQueueResponse" : "Retro Roulette's mode has been changed to queue!",
        "notifyStreamerResponse" : "@$user the next game is $game.",
        "invalidNumberResponse" : "@$user, please try again. Make sure the number you picked is a positive whole number greater than 0 and less than $consoleMax.",
        "alreadyEnteredResponse" : "@$user, you have already entered the queue.",
        "alreadyPickedResponse" : "Tigelton played the game you picked @$user, let others have a chance DontAtMe",
        "noRouletteResponse" : "@$user, Retro Roulette has not been started.",
        "alreadyStartedResponse" : "@$user, Retro Roulette has already been started.",
        "alreadyEndedResponse" : "@$user, Retro Roulette has already been ended.",
        "notEmptyResponse" : "@$user, queue is not empty. Use $nextCommand to get the next number or use $restartCommand to empty the queue and start over.",
        "noNumberResponse" : "@$user you must put a positive whole number after $pickCommand, or the word random.",
        "consoleChangedResponse" : "@$user, you have changed the console to $console.",
        "consoleNotChangedResponse" : "@$user, you must enter one of the allowed consoles after $consoleCommand.",
        "maxResponse" : "@$user, the max number for the $currentConsole is $consoleMax.",
        "removedResponse" : "@$user, you have been removed from the queue because your number was too high for the new console.",
        "lessThanOneResponse" : "@$user, You can't pick numbers less than 1",
        "notEnteredLeaveResponse" : "@$user, you can't leave the queue without entering first. Idiot KEKW",
        "notEnteredSpotResponse" : "@$user, you can't check your spot in the queue without entering first. Idiot KEKW",
        "spotResponse" : "@$user, your spot in the queue is $spot out of $total HeadBanging",
        "spotRandomResponse" : "@$user, you are in the queue of $total people. But Retro Roulette is in Random mode. Good luck HyperTigel",
        "queueRandomResponse" : "The queue has $total people in it but Retro Roulette is in Random mode. Good luck HyperTigel",
        "queueFiveResponse" : "The next $spots spots are: $user1 with $num1; $user2 with $num2; $user3 with $num3; $user4 with $num4; $user5 with $num5;",
        "modeNotChangedResponse" : "@user, the mode was not changed. Make sure you put either Random or Queue after $modeCommand",
        "currentResponse" : "The current game is $game picked by $user PepoG",
        "whoSelfResponse" : "@$user, you picked number $number",
        "whoByNameResponse" : "$user picked number $number",
        "whoByAlreadyPlayedNameResponse" : "$user picked number $number and it has already been played",
        "whoByNumberResponse" : "The number $number was picked by $user",
        "whoByAlreadyPlayedNumberResponse" : "The number $number has already been played, but it was picked by $user",
        "whoNoneResponse" : "Error: Not found in queue. pressF",
        "banResponse" : "@$user has been banned oatsTrash",
        "unbanResponse" : "@$user has been unbanned peepoSHAKE",
        "alreadyPickedPreviousStreamResponse": "@$user, that number was played in a previous stream, try another number or use the word Random",
        "consoleResetResponse" : "@$user, you have reset the previously picked numbers for the $console",
        "consoleNotResetResponse" : "@$user, the console was not reset. Make sure the put the console name after $resetConsoleCommand",
        "shuffleResponse" : "@$user, the games for $console were shuffled.",
        "shuffleFailedResponse" : "@$user, nothing was shuffled. Make sure to put the console name or All after $shuffleCommand",
        "refundResponse" : "@$user, you have been refunded. Pick another number!",
        "refundFailedResponse" : "@$user the refund failed, please check for a typo!",
        "refundWaitResponse" : "@$user, the refunded user has not picked another number! Use $noRefundComand if needed",
    }

# ReloadSettings Function
# This function controls what the Save Settings button in the script settings does
def ReloadSettings(jsonData):
    Init()
    return

# OpenBannedList Function
# This function controls what the Open Banned List button in the script settings does
def OpenBannedList():
    location = os.path.join(path, "bannedList.json")
    os.startfile(location)
    return

# OpenCommands Function
# This function controls what the Open Commands button in the script settings does
def OpenCommands():
    location = os.path.join(path, "commands.json")
    os.startfile(location)
    return

# OpenCommands Function
# This function controls what the Open Permissions button in the script settings does
def OpenPermissions():
    location = os.path.join(path, "permissions.json")
    os.startfile(location)
    return

# OpenCommands Function
# This function controls what the Open Folder of Config Files button in the script settings does
def OpenFolder():
    location = path
    os.startfile(location)
    return

# OpenCommands Function
# This function controls what the Open Read Me button in the script settings does
def OpenReadMe():
    location = os.path.join(path, "README.MD")
    os.startfile(location)
    return

# Tick Function
# This function is required
def Tick():
    return
