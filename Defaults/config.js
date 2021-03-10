﻿var settings = {
  "liveOnly": true,
  "keepTrack": false,
  "defaultMode": "Random",
  "defaultConsole": "SNES",
  "startResponse": "Retro Roulette has started! Use $pickCommand followed by a positive whole number or the word random to enter!",
  "endResponse": "Retro Roulette has ended. Better luck next time!",
  "resetResponse": "Retro Roulette has been reset, everyone can pick numbers again!",
  "restartResponse": "Retro Roulette has been restarted. The queue is now empty and everyone can pick numbers again!",
  "modeRandomResponse": "Retro Roulette's mode has been changed to random!",
  "modeQueueResponse": "Retro Roulette's mode has been changed to queue!",
  "notifyStreamerResponse": "@$user the next game is $game.",
  "invalidNumberResponse": "@$user, please try again. Make sure the number you picked is a positive whole number greater than 0 and less than $consoleMax.",
  "alreadyEnteredResponse": "@$user, you have already entered the queue.",
  "alreadyPickedResponse": "Tigelton played the game you picked @$user, let others have a chance DontAtMe",
  "noRouletteResponse": "@$user, Retro Roulette has not been started.",
  "alreadyStartedResponse": "@$user, Retro Roulette has already been started.",
  "alreadyEndedResponse": "@$user, Retro Roulette has already been ended.",
  "notEmptyResponse": "@$user, queue is not empty. Use $nextCommand to get the next number or use $restartCommand to empty the queue and start over.",
  "noNumberResponse": "@$user you must put a positive whole number after $pickCommand, or the word random.",
  "consoleChangedResponse": "@$user, you have changed the console to $console.",
  "consoleNotChangedResponse": "@$user, you must enter one of the allowed consoles after $consoleCommand.",
  "maxResponse": "@$user, the max number for the $currentConsole is $consoleMax.",
  "removedResponse": "@$user, you have been removed from the queue because your number was too high for the new console.",
  "spotResponse": "@$user, your spot in the queue is $spot out of $total HeadBanging",
  "spotRandomResponse": "@$user, you are in the queue of $total people. But Retro Roulette is in Random mode. Good luck HyperTigel",
  "queueRandomResponse": "The queue has $total people in it but Retro Roulette is in Random mode. Good luck HyperTigel",
  "queueFiveResponse": "The next five $spots are: $user1 with $num1; $user2 with $num2; $user3 with $num3; $user4 with $num4; $user5 with $num5;",
  "modeNotChangedResponse": "@user, the mode was not changed. Make sure you put either Random or Queue after $modeCommand",
  "currentResponse": "The current game is $game picked by $user PepoG",
  "whoSelfResponse": "@$user, you picked number $number",
  "whoByNameResponse": "$user picked number $number",
  "whoByAlreadyPlayedNameResponse": "$user picked number $number and it has already been played",
  "whoByNumberResponse": "The number $number was picked by $user",
  "whoByAlreadyPlayedNumberResponse": "The number $number has already been played, but it was picked by $user",
  "whoNoneResponse": "Error: Not found in queue. pressF",
  "banResponse": "@$user has been banned from Retro Roulette oatsTrash",
  "unbanResponse": "@$user has been unbanned from Retro Roulette peepoSHAKE",
  "lessThanOneResponse": "@$user, You can't pick numbers less than 1",
  "notEnteredLeaveResponse": "@$user, you can't leave the queue without entering first, Idiot KEKW",
  "notEnteredSpotResponse": "@$user, you can't check your spot in the queue without entering first, Idiot KEKW",
  "alreadyPickedPreviousStreamResponse": "@$user, that number was played in a previous stream, try another number or use the word Random",
  "consoleResetResponse": "@$user, you have reset the previously picked numbers for the $console",
  "consoleNotResetResponse": "@$user, the console was not reset. Make sure to put the console name after $resetConsoleCommand",
  "shuffleResponse": "@$user, the games for $console were shuffled.",
  "shuffleFailedResponse": "@$user, nothing was shuffled. Make sure to put the console name or All after $shuffleCommand"
};