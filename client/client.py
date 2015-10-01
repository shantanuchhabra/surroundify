#!/usr/local/bin/python -i

from ws4py.client.threadedclient import WebSocketClient as WebSocket

from threading import Thread
import sys
from time import time, sleep
import math

from subprocess import Popen, PIPE

apoorvaURL = '128.237.222.84'
dropletURL = '104.131.112.48'

wsURL = dropletURL
if 'local' in sys.argv:
    wsURL = apoorvaURL

try:
    myname = sys.argv[1]
except:
    myname = 'Robert'


if myname == 'apoorva':
    discrete = (lambda x: 300 if (math.floor(x)/2) % 2 == 0 else 0)
if myname == 'nancy':
    discrete = (lambda x: 0 if (math.floor(x)/2) % 2 == 0 else 300)
if myname == 'nikhil':
    discrete = (lambda x: 300 if (math.floor(x)/2) % 2 == 0 else 0)
if myname == 'shantanu':
    discrete = (lambda x: 0 if (math.floor(x)/2) % 2 == 0 else 300)


if myname == 'apoorva':
    circular = (lambda x: 200 + (100*(math.sin(x))))
if myname == 'nancy':
    circular = (lambda x: 200 + (100*(math.sin(x - (math.pi/2.0)))))
if myname == 'nikhil':
    circular = (lambda x: 200 + (100*(math.sin(x - (math.pi)))))
if myname == 'shantanu':
    circular = (lambda x: 200 + (100*(math.sin(x - (3.0*(math.pi)/2.0)))))



try:
    volumeFunction = eval(sys.argv[2])
except:
    volumeFunction = lambda x: 200

class SongPlayer(object):
    def __init__(self, filename):
        self.filename = filename

    def startProcess(self):
        self.vlcProcess = Popen(["/Applications/VLC.app/Contents/MacOS/VLC", "-I", "rc", self.filename], stdin=PIPE, stdout=PIPE)

    def sendCommandToProcess(self, input):
        self.vlcProcess.stdin.write(input + '\n')

    def pause(self):
        self.sendCommandToProcess("pause\n")

    def play(self):
        self.sendCommandToProcess("play")

    def seek(self, time):
        # time in seconds
        self.sendCommandToProcess("seek %d\n" % time)

print "Client imported 6"

class WSClient(WebSocket):
    
    
    def opened(self):
        def alterVolume():
            timeAmount = 0
            while True:
                self.player.sendCommandToProcess("volume %d" % volumeFunction(timeAmount))
                timeAmount += 0.25
                sleep(0.25)


        print "We established a connection"
        self.player = SongPlayer("simarik.mp3")
        self.player.startProcess()
        self.player.pause()
        self.serverPrescription = 0
        self.volumeThread = Thread(target=alterVolume)

    def received_message(self, message):
        print "We got : ", message
        # assert message == "play"
        if str(message) == "play":
            print "My UNIX time is ", time()
            self.player.pause()
            self.volumeThread.start()
        elif "seek" in str(message):
            print "Executing ", str(message)
            # self.player.sendCommandToProcess(str(message)+"\n")
            self.player.sendCommandToProcess("get_time")
            self.serverPrescription = int(str(message)[5:])
            print "Server prescription", self.serverPrescription

    def closed(self, code, reason=None):
        print "Connection closed booooo!"

wsclient = WSClient("ws://%s:8888/socket" % wsURL)

print "Client imported 5"

def establishConnection():
    global wsclient
    while not wsclient:
        pass
    wsclient.connect()
    print "RUNNING FOREVER"
    wsclient.run_forever()

WSThread = Thread(target=establishConnection)
WSThread.daemon = True
WSThread.start()

print "Client imported 4"

sleep(1)

def write(arg):
    wsclient.send(arg)
    

print "Client imported 3"

def listenToVLC():
    global wsclient
    print "entered the listener"
    
    while True:
        try:
            pollState = wsclient.player.vlcProcess.poll()
        except:
            continue

        if pollState:
            continue
        line = wsclient.player.vlcProcess.stdout.readline()
        line = line[2:]

        try:
            timestamp = int(line)
            print "The current VLC position is ", timestamp
            if timestamp == wsclient.serverPrescription:
                print "We're in sync"
            else:
                print "Seeking to ", wsclient.serverPrescription
                wsclient.player.seek(wsclient.serverPrescription)

        except:
            pass

print "Client imported 2"


VLCListener = Thread(target=listenToVLC)
VLCListener.daemon = True
VLCListener.start()






















