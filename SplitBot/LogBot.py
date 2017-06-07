# -*- coding: utf-8 -*-
import socket
import ssl
#import botcfg
import string
import time
import re
import urllib, json
import datetime
import sqlite3

re.purge()  # some housekeeping
server = "irc.chat.twitch.tv"
port = 443
channohash = "thebuddha3"  # target channel without the hashkey
channel = "#" + channohash

# BOOLS OF BOOLS OF BOOLS

# CONNECTION #
# init socket
self = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to said socket
self.connect((server, port))
# wrap in ssl
irc = ssl.wrap_socket(self)
##################################
# SYSTEM STARTUP  #
#irc.send("PASS " + botcfg.oa + '\r\n')
irc.send("NICK " + "justinfan420" + '\r\n')
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


CHAT_MSG = re.compile(r"@.+?PRIVMSG.+?(:){1}")  # New (for irc flags mode)



def tablecheck():
    connx = sqlite3.connect("buddhalog.db")
    cu = connx.cursor()

    try:

        blah = "select * from chat"
        cu.execute(blah)

        print "table exists already, skipping"
        return True
    except Exception as (e):
        print e
        date = time.strftime('%d/%m/%Y')
        firsts = "create table if not exists chat"
        firststart = firsts
        firststart += """ (
                        usr text,
                        mesg text,
                        id integer primary key,
                        flags text,
                        channel text,
                        date_time text

                        );"""

        print "firststart ran"
        time.sleep(2)
        cu.execute(firststart)
        date = time.strftime("%Y-%m-%dT%H:%M:%S")
        print date
        strings = "insert into chat"
        cu.execute(strings + " values (?,?,?,?,?,?)",
                   ("username", "message", 1, "flags", "channel", date))
        connx.commit()
        connx.close()

tablecheck()
conn = sqlite3.connect('buddhalog.db')
c = conn.cursor()

##Main Bot Start
while True:
    # gets output from IRC server
    data = irc.recv(1024)
    # ping/pong
    if data == "PING :tmi.twitch.tv\r\n":
        irc.send("PONG :tmi.twitch.tv\r\n")
    user = data.split('!', 1)[-1]
    user = user.split('@')[0]
    message = CHAT_MSG.sub("", data)
    flags = data.split(':', 1)[0]

    if message == "!quit\r\n":
        if user == "breadcam":
            #irc.send('PRIVMSG ' + channel + " :" + "Connection Terminated... BibleThump" + "\r\n")
            #irc.send('PRIVMSG ' + channel + ' :' ".w breadcam " + data + '\r\n')
            irc.send('PART ' + channel + '\r\n')
            quit()

    #print (user + ": " + message)  # new (for flags mode)

    ##LOGGING

    try:
        unicode(message, "utf-8")
        if "tmi.twitch.tv" not in (user) and "tmi.twitch.tv" not in (message) and (user) != "":
            if "jtv MODE" not in (user) and "justinfan" not in (user) and user != "twitchnotify":
                date = time.strftime("%Y-%m-%dT%H:%M:%S")
                blah = "select count (*) from chat"

                c.execute(blah)
                temp = c.fetchone()
                # print temp[0]
                temp = temp[0] + 1
                blah = "insert into chat"

                messageq = '"' + str.replace(message, "\r\n", "") + '"'
                
                c.execute(blah + " values (?,?,?,?,?,?)",
                          (user, messageq, temp, flags, channohash, date))
                conn.commit()

    except Exception as e:
        if (user) != "":
            date = time.strftime("%Y-%m-%dT%H:%M:%S")
            blah = "select count (*) from chat"
            c.execute(blah)
            temp = c.fetchone()
            temp = temp[0] + 1
            conn.text_factory = 'utf-8'

            blah = "insert into chat"
            c.execute(blah + " values (?,?,?,?,?,?)",
                (user, message, temp, flags, channohash, date)
                      )
            conn.commit()

            conn.text_factory = 'string'
            print e
            print messageq
    time.sleep(0.1)
