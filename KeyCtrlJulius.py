#! /usr/bin/python -u

import sys
import os
import time
import thread
import logging
import argparse

try:
    import json
except:
    import simplejson as json

parser = argparse.ArgumentParser(description="Keyword Controller for Julius")
parser.add_argument("--quiet", action="store_true", help="reduce output to only word string")
parser.add_argument("--debug", action="store_true", help="(for debug) dump numerous log")
args = parser.parse_args()

class InputEvent:

    def name(self, frame):
        return frame.f_code.co_name

    def execute(self, name):
        logger.debug("Event::%s triggered, call event name", name)
        if not "events" in config or not name in config["events"]:
            logger.debug("Event name \"%s\" was not found", name)
            return

        command = Command({"exec": config["events"][name]})
        command.execute()
        logger.debug("Event::%s was called", name)

    def onReady(self):
        self.execute(self.name(sys._getframe()))

    def onError(self):
        self.execute(self.name(sys._getframe()))

    def onEnding(self):
        self.execute(self.name(sys._getframe()))

    def onStart(self):
        self.execute(self.name(sys._getframe()))

    def onSuccess(self):
        return

    def onKeyword(self):
        self.execute(self.name(sys._getframe()))

    def onCommand(self):
        self.execute(self.name(sys._getframe()))

    def onExpired(self):
        self.execute(self.name(sys._getframe()))

    def onAccept(self):
        self.execute(self.name(sys._getframe()))

    def onExecute(self):
        return

    def onUnknown(self):
        self.execute(self.name(sys._getframe()))

    def onListening(self):
        self.execute(self.name(sys._getframe()))

    def onUnderstand(self):
        self.execute(self.name(sys._getframe()))

class Command:

    def __init__(self, command):
        self.command = command

    def execute(self):
        def run(command):
            logger.debug("Execute command: %s", command)
            event.onExecute()
            os.system(command)

        if isinstance(self.command["exec"], list):
            for command in self.command["exec"]:
                run(command)
        else:
            run(self.command["exec"])

        event.onSuccess()

class CommandParser:

    @staticmethod
    def parse(word):

        logger.debug("Search command in configuration file: %s", confname)
        for command in config["command"]:
            if "name" in command and "exec" in command and command["name"].lower() == word.lower():
                logger.debug("Command record for \"%s\" was found", command["name"])
                return Command(command)

        logger.debug("No matches in list")
        return False

class InputStream:

    def __init__(self, file_object):
        logger.debug("Waiting for input data stream")
        event.onReady()
        keyword     = KeywordListening()
        startstring = "sentence1: <s> "
        endstring   = " </s>"

        while 1:
            line = file_object.readline()
            if not line:
                break

            if "missing phones" in line.lower():
                event.onError()
                logger.error("Missing phonemes for the used grammar file")
                raise

            if line.startswith(startstring) and line.strip().endswith(endstring):
                incomes = line.strip('\n')[len(startstring):-len(endstring)]

                if keyword.isListening == False:
                    logger.debug("Keyword not in listening mode, check input data")
                    logger.debug("Starting listening for keyword: \"%s\"", config["keyword"])
                    thread.start_new_thread(keyword.listen, (incomes,))
                elif keyword.isListening == True:
                    logger.debug("Keyword in listening mode. Parse incomming command")
                    event.onCommand()
                    keyword.parse(incomes)

class KeywordListening:

    isListening = False

    def parse(self, input):

        logger.debug("Execute incomming command, when recognized")
        command = CommandParser.parse(input)
        if command:
            event.onAccept()
            command.execute()
        elif not "-q" in sys.argv and not "--quiet" in sys.argv:
            logger.debug("Unsupportet command entry %s", input)
            event.onUnknown()

    # Define a function for the thread
    def timeout(self, repeat, seconds):
        KeywordListening.isListening = True
        count = 0
        while count < repeat:
            time.sleep(seconds)
            logger.debug("%d seconds to inputting an instruction", (repeat -count))
            count += 1
        logger.debug("instruction expired")
        event.onExpired()
        KeywordListening.isListening = False

    def listen(self, line):
        keyword = config["keyword"]
        timeout = {"repeat": 5, "delay": 1}
        params  = [param.lower() for param in line.split() if param]

        if not "-q" in sys.argv and not "--quiet" in sys.argv:
            logger.debug("Recognized input \"%s\"", params)

            if params[0].upper() == keyword.upper():
                logger.debug("Keyword was said and recognized")
                logger.debug("Starting listening for Commands with a timeout of %d seconds", (timeout["repeat"] *timeout["delay"]))
                thread.start_new_thread(self.timeout, (timeout["repeat"], timeout["delay"]) )
                event.onListening()
                event.onKeyword()
            else:
                logger.debug("Input data isnt a Keyword")
                event.onUnderstand()

        self.params = params

def write(message): 
    if not args.quiet: print message

if __name__ == "__main__":

    basename = os.path.basename(sys.argv[0])
    filename = os.path.splitext(basename)[0]
    confname = os.path.dirname(__file__)+ "/"+ filename +".json"
    config   = {"keyword": "JULIUS", "command": []}

    logging.basicConfig()
    logger = logging.getLogger()
    logger.getChild("client.stt").setLevel(logging.INFO)

    write("*******************************************************")
    write("*              JULIUS - KEYWORD CONTROLLER            *")
    write("*  keyword controlling for speech recognition engine  *")
    write("*  (c) 2015, Ronny Eisenkolb (@eisenkolb)             *")
    write("*******************************************************")

    event = InputEvent()

    if args.debug: logger.setLevel(logging.DEBUG)
    if os.path.isfile(confname):
        logger.debug("Trying to read config file: \"%s\"", confname, exc_info=False)
        try:
            with open(confname) as data_file:
                config = json.load(data_file)
        except Exception:
            event.onError()
            logger.error("Can't open or parse config file: \"%s\"", data_file, exc_info=False)
            raise
    else: logger.warning("Configuration cannot be access file: \"%s\"", confname)

    try:
        event.onStart()
        InputStream(sys.stdin)
    except KeyboardInterrupt:
        event.onError()
        event.onEnding()
        sys.exit(1)