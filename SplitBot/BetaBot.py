# -*- coding: utf-8 -*-
import socket
import ssl
import botcfg
import string
import time
from threading import *
import re
import urllib, urllib2, json
import datetime
import random
import sqlite3

re.purge()  # some housekeeping
server = "irc.chat.twitch.tv"
port = 443
channohash = "thebuddha3"  # target channel without the hashkey
channel = "#" + channohash

# BOOLS OF BOOLS OF BOOLS

# IRC SEND MESSAGES



###################################
###########NEW VARS

modList = []
modTemp = ''
modData = ''
WhisperMsg = ''

###################################
# CONNECTION #
# init socket
self = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to said socket
self.connect((server, port))
# wrap in ssl
irc = ssl.wrap_socket(self)
##################################
# SYSTEM STARTUP  #
irc.send("PASS " + botcfg.oa + '\r\n')
irc.send("NICK " + botcfg.botnick + '\r\n')
# capabilities request
irc.send("CAP REQ :twitch.tv/membership" + "\r\n")
# and join channel
irc.send("JOIN " + channel + '\r\n')
##################################
# tags request
irc.send("CAP REQ :twitch.tv/tags" + "\r\n")
# commands request
irc.send("CAP REQ :twitch.tv/commands" + "\r\n")
# join message
irc.send('PRIVMSG ' + channel + ' : .mods' + '\r\n')
# irc.send("PRIVMSG " + channel + " :" + ".me Im back KappaClaus " + "\r\n")

CHAT_MSG = re.compile(r"@.+?PRIVMSG.+?(:){1}")  # New (for irc flags mode)

# Live Checker
def liveCheck(chan):
    cliid = "/?client_id=q6batx0epp608isickayubi39itsckt"
    uptadr = "https://api.twitch.tv/kraken/streams/" + chan + cliid

    response = urllib.urlopen(uptadr)
    data = json.loads(response.read())
    if data['stream'] == None:
        print "Offline"
        return False
    else:
        print "Online"
        return True

def queryPlz(name, ir, count, orig):
    zx = ""
    xzy = ""

    try:
        conne = sqlite3.connect('buddhalog.db')
        co = conne.cursor()

        name = string.replace(name, "\r\n", "")

        co.execute('select mesg from chat where usr = lower((?)) order by id desc limit ' + str(count), [name])

        zx = co.fetchall()

        for i in zx:
            print i[0]
            xzy += i[0] + " >#< "
        xzy = string.replace(xzy, "\r\n", "")
        conne.close()
        print zx
        ir.send(
            'PRIVMSG ' + channel + ' : .w ' + orig + " Last " + str(count) + " from " + name + ": " + str(xzy) + '\r\n')

    except Exception as e:
        print e
        conne.close()

conn = sqlite3.connect('buddhalog.db')
c = conn.cursor()

##Main Bot Start
while True:
    # gets output from IRC server
    data = irc.recv(1024)
    # ping/pong
    if data == "PING :tmi.twitch.tv\r\n":
        irc.send("PONG :tmi.twitch.tv\r\n")

        irc.send('PRIVMSG ' + channel + ' : .mods' + '\r\n')

    user = data.split('!', 1)[-1]
    user = user.split('@')[0]
    message = CHAT_MSG.sub("", data)
    flags = data.split(':', 1)[0]


    if "tmi.twitch.tv WHISPER thebuddha3bot" in (message):
        WhisperMsg = message.split(":")[2]
        WhisperMsg = str.replace(WhisperMsg, "\r\n", "")
        WhisperUsr = user
        if user in modList:
            WhisperUsr = "\|/ " + WhisperUsr

        if "!last" in (WhisperMsg):
            print "test1"
            try:
                # if "mod=1" in (flags) or "badges=broadcaster" in (flags) or (user) == "thor10768765":
                if user in modList:
                    messageq = WhisperMsg.split(" ")
                    messagereqc = messageq[0]
                    messageq = messageq[1]

                    messagereqc = string.replace(messagereqc, "!last", "")

                    print messageq
                    print messagereqc
                    queryPlz(str(messageq), irc, int(messagereqc), user)
            except Exception as e:
                print e

        if "hi" in (WhisperMsg):
            if user in modList:
                print "win"
                irc.send('PRIVMSG ' + channel + ' :' ".w " + user + " Hia dood buddhaLove" + '\r\n')


        print WhisperUsr + ": " + WhisperMsg
    if "@msg-id=room_mods :tmi.twitch.tv NOTICE #thebuddha3 :The moderators of this room are:" in (data):
        modData = str.replace(data, "\r\n", "")
        modData = modData.split(":")[3]
        modTemp = str.replace(modData, " ", "")
        modList = modTemp.split(",")
        print len(modList)
                            # for i in modList



    # print data
    time.sleep(0.1)

