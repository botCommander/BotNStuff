# -*- coding: utf-8 -*-
import socket
import ssl
import botcfg
import time
from threading import *
import re
import urllib, json
import datetime
import sqlite3

# re.purge()  # some housekeeping
# server = "irc.chat.twitch.tv"
# port = 443
channohash = "thebuddha3"  # target channel without the hashkey
channel = "#" + channohash
pointSpeed = 600
# perm = {}
# plebcheck = r"subscriber=1|badges=partner|badges=broadcaster|mod=1|bits/10000"
# pcheck = False
# # IRC SEND MESSAGES
#
# # CONNECTION #
# # init socket
# self = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # connect to said socket
# self.connect((server, port))
# # wrap in ssl
# irc = ssl.wrap_socket(self)
# ##################################
# # SYSTEM STARTUP  #
# irc.send("PASS " + botcfg.oa + '\r\n')
# irc.send("NICK " + botcfg.botnick + '\r\n')
# # capabilities request
# irc.send("CAP REQ :twitch.tv/membership" + "\r\n")
# # and join channel
# irc.send("JOIN " + channel + '\r\n')
# ##################################
# # tags request
# irc.send("CAP REQ :twitch.tv/tags" + "\r\n")
# # commands request
# irc.send("CAP REQ :twitch.tv/commands" + "\r\n")
# # join message
# # irc.send("PRIVMSG " + channel + " :" + ".me Im back KappaClaus " + "\r\n")
#
# CHAT_MSG = re.compile(r"@.+?PRIVMSG.+?(:){1}")  # New (for irc flags mode)

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

# Points/XP/DBStarter/Steak
def chatz():
    global channohash
    if liveCheck(channohash):
        conn = sqlite3.connect('buddhalog.db')
        c = conn.cursor()
        url = urllib.urlopen('https://tmi.twitch.tv/group/user/' + channohash + '/chatters').read()
        url = json.loads(url)
        mods = url.get('chatters').get('moderators')
        views = url.get('chatters').get('viewers')
        # print mods
        # print views
        if mods != None:

            c.execute('select usr from points')

            test = c.fetchall()
            try:
                if test[0] == None:
                    test = ":"
            except IndexError:
                print 'db empty'

            for name in (mods):

                modsit = [item for item in test if item[0] == name]

                if modsit:

                    # print "sucess!!!"
                    c.execute("""update points set point = point + 10 where usr = (?)""", [name])
                    print "adding points for " + name

                    # increment points and timetot
                    conn.commit()

                else:
                    date = time.strftime('%d/%m/%Y')
                    blah = "select count (*) from points"
                    c.execute(blah)
                    temp = c.fetchone()
                    # print temp[0]
                    temp = temp[0] + 1
                    blah = "insert into points"

                    c.execute(blah + " values (?,?,?,?,?)",
                              (name, 0, temp, channohash, date))
                    conn.commit()
                    # c.executemany("""insert into usr Values (?,?,?,?,?)""", [(name, 1, temp, channohash, datenow),])


                    print "added user :  " + name

        for plebian in (views):

            plebsit = [pleb for pleb in test if pleb[0] == plebian]

            if plebsit:
                c.execute("""update points set point = point + 10 where usr = (?)""", [plebian])
                conn.commit()
                print "adding points for " + plebian
            else:

                date = time.strftime('%d/%m/%Y')
                blah = "select count (*) from points"
                c.execute(blah)
                temp = c.fetchone()
                # print temp[0]
                temp = temp[0] + 1
                blah = "insert into points"

                c.execute(blah + " values (?,?,?,?,?)",
                          (plebian, 0, temp, channohash, date))
                conn.commit()
                # c.executemany("""insert into usr Values (?,?,?,?,?)""", [(name, 1, temp, channohash, datenow),])

                print "added user : " + plebian
        conn.commit()
        conn.close()
    xyz = Timer(pointSpeed, chatz)
    xyz.start()

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

    try:

        blah = "select * from points"
        cu.execute(blah)

        connx.close()
        print "table exists already, skipping"
        return True
    except Exception as (e):
        print e
        date = time.strftime('%d/%m/%Y')
        firsts = "create table if not exists points"
        firststart = firsts
        firststart += """ (
                        usr text,
                        point integer,
                        id integer primary key,
                        channel text,
                        date_created text

                        );"""

        print "firststart ran"
        time.sleep(2)
        cu.execute(firststart)
        date = time.strftime("%Y-%m-%dT%H:%M:%S")
        print date
        strings = "insert into points"
        cu.execute(strings + " values (?,?,?,?,?)",
                   ("username", 1, 1, "channel", date))
        connx.commit()
        connx.close()

# Points Startup
tablecheck()
breeeeadd = Timer(pointSpeed, chatz)
breeeeadd.start()
conn = sqlite3.connect('buddhalog.db')
c = conn.cursor()

##Main Bot Start
# while True:
#     # gets output from IRC server
#     data = irc.recv(1024)
#     # ping/pong
#     if data == "PING :tmi.twitch.tv\r\n":
#         irc.send("PONG :tmi.twitch.tv\r\n")
#
#     user = data.split('!', 1)[-1]
#     user = user.split('@')[0]
#     message = CHAT_MSG.sub("", data)
#     flags = data.split(':', 1)[0]
#
# #only here to kill bot
#     if message == "!quit\r\n":
#         if user == "thebuddha3" or "breadcam" or "riotcam" or "thor10768765":
#             #irc.send('PRIVMSG ' + channel + " :" + "Connection Terminated... BibleThump" + "\r\n")
#             #irc.send('PRIVMSG ' + channel + ' :' ".w breadcam " + data + '\r\n')
#             irc.send('PART ' + channel + '\r\n')
#             quit()
#     time.sleep(0.1)
