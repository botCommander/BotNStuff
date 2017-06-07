#-*- coding: utf-8 -*-
import socket
import ssl
import botcfg
import string
import time
from threading import *
import re
import urllib,urllib2, json
import datetime
import random
import sqlite3

re.purge() # some housekeeping
server = "irc.chat.twitch.tv"
port = 443
channohash = "thebuddha3"  # target channel without the hashkey
channel = "#" + channohash
perm = {}
plebcheck = r"subscriber=1|badges=partner|badges=broadcaster|mod=1|bits/10000"
pcheck = False
webpattAlt = r"[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
webpatt = r"\.+[a-zA-Z]+[/]+[a-zA-Z0-9]"
playlistTimerCommand = "playlistTimerCommand"
blacklist = ["[dD][dD][Oo][Ss]"]
squidBlocker = 0
subscriber = ""
subname = ""
submonths = ""
#BOOLS OF BOOLS OF BOOLS
unsetpListwait = False
unsetpSubwait = False
calcwaitplz = False
unsetpMetawait = False
unsetpBobwait = False
unsetpTonywait = False
unsetpReggiewait = False
unsetpPeterwait = False
unsetpGrannywait = False
unsetpMerchwait = False
unsetpDiscordwait = False
unsetpTwitterwait = False
unsetpPostwait = False
uptimewait = False
waitplease = False
waitplease2 = False
systemBootUp = True
#IRC SEND MESSAGES
msg1 = ".me (bot): I don't like links... DansGame " # link posting timeout message
msgPlaylist =  ".me Check Out Buddha's Playlist https://www.youtube.com/playlist?list=PLbegEdtZ4V6V4_76iimPQpJp4MWjAFKJk"
msgSubscriber = ".me If you want to support the channel and get access to our sub only emotes buddhaCrash buddhaLove buddhaPineapple buddhaHi buddhaSellout buddhaCry buddhaLUL buddhaPray buddhaTen buddhaGasm buddhaPray you can subscribe at https://www.twitch.tv/thebuddha3/subscribe <3"
msgMeta = " .me " + " ⚠️ ⚠️ ⚠️ ⚠️ Anyone caught posting META INFO in chat will receive a TIMEOUT. It ruins the experience for BUDDHA AND HIS VIEWERS. It's also against SERVER AND CHANNEL rules ⚠️ ⚠️ ⚠️ ⚠️"
msgBob = ".me Please go checkout Bob at https://www.twitch.tv/coolidgehd show him some love and drop him a follow"
msgReggie = ".me Please go checkout Reggie at https://www.twitch.tv/SirPinkleton00 show him some love and drop him a follow"
msgTony = ".me Please go checkout Tony at https://www.twitch.tv/anthonyz_ show him some love and drop him a follow"
msgPeter = ".me Peter the Great you already know https://www.twitch.tv/bubblescsgo show him some love and drop him a follow"
msgGranny = ".me Please go checkout Granny at https://www.twitch.tv/DisbeArex show her some love and drop her a follow"
msgDiscord = ".me Make sure to Join us in Buddha's Dojo https://discordapp.com/invite/wGx4dtG"
msgTwitter = ".me Keep up to date with the latest streamn info by following Buddha on Twitter at https://www.twitter.com/TheBuddha_3"
msgMerch = "A STATE OF EMERGENCY HAS OFFICIALLY BEEN ISSUED FOR THE CITY OF LOS SANTOS Check out all the \_eanbois and SOE Merch at https://www.designbyhumans.com/shop/Buddha3/"
# CONNECTION #
# init socket
self = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
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
#irc.send("PRIVMSG " + channel + " :" + ".me Im back KappaClaus " + "\r\n")

CHAT_MSG=re.compile(r"@.+?PRIVMSG.+?(:){1}") # New (for irc flags mode)

def permit(name):
    del perm[name]
def plebcheckk(flagz):
    if re.search(plebcheck, flags):
        return True
def calcIt(v1, op, v2):
    global calcwaitplz
    if calcwaitplz != True:

        try:
            if op == "+":
                answ = int(v1) + int(v2)
                irc.send('PRIVMSG ' + channel + ' :' "Answer is: " + str(answ)  + '\r\n')
            if op == "-":
                answ = int(v1) - int(v2)
                irc.send('PRIVMSG ' + channel + ' :' "Answer is: " + str(answ)  + '\r\n')
            if op == "*":
                answ = int(v1) * int(v2)
                irc.send('PRIVMSG ' + channel + ' :' "Answer is: " + str(answ)  + '\r\n')
            if op == "/":
                answ = int(v1) / int(v2)
                irc.send('PRIVMSG ' + channel + ' :' "Answer is: " + str(answ)  + '\r\n')
            calcwaitplz = True
            xy = Timer(120, unsetCalc)
            xy.start()
        except Exception as e:
            print e
            print "likely NaN" # python has check for Not a number?
###############################
#Timers Unsetters
def unsetCalc():
    global calcwaitplz
    calcwaitplz = False
def unsetUt():
    print "UNSET UT"
    global uptimewait
    uptimewait = False
def unsetpList():
    global unsetpListwait
    unsetpListwait = False
def unsetpSub():
    global unsetpSubwait
    unsetpSubwait = False
def unsetpMeta():
    global unsetpMetawait
    unsetpMetawait = False
def unsetpBob():
    global unsetpBobwait
    unsetpBobwait = False
def unsetpReggie():
    global unsetpReggiewait
    unsetpReggiewait = False
def unsetpTony():
    global unsetpTonywait
    unsetpTonywait = False
def unsetpPeter():
    global unsetpPeterwait
    unsetpPeterwait = False
def unsetpGranny():
    global unsetpGrannywait
    unsetpGrannywait = False
def unsetpDiscord():
    global unsetpDiscordwait
    unsetpDiscordwait = False
def unsetpTwitter():
    global unsetpTwitterwait
    unsetpTwitterwait = False
def unsetpMerch():
    global unsetpMerchwait
    unsetpMerchwait = False
def unsetpPostTimer():
    global unsetpPostwait
    unsetpPostwait = False
def blacklistAdd(garbage):
    global blacklist
    #print "before " + blacklistlist
    blacklist.append(garbage)
    #print "after " + blacklistlist
def blacklistRem(garbage):
    x = 0
    global blacklist
    for i in blacklist:

        if i == garbage:
            blacklist.pop(x)
        x += 1
    print garbage
#Live Checker
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
#UpTime Checker
def uptimeCheck(irc):
    global channohash
    global uptimewait
    cliid = "/?client_id=q6batx0epp608isickayubi39itsckt"
    uptadr = "https://api.twitch.tv/kraken/streams/" + channohash + cliid
    #uptadr = "https://api.twitch.tv/kraken/streams/" + 'thebuddha3' + cliid

    if uptimewait != True:
        uptimewait = True
        response = urllib.urlopen(uptadr)
        data = json.loads(response.read())
        if data['stream'] == None:
            print "Offline"
            irc.send('PRIVMSG ' + channel + " :" + ".me The Channel Appears To Be Offline..." + "\r\n")
        else:
                     
            s = data['stream']['created_at'][0:19]
            sucess = time.mktime(datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S").timetuple())
             # change timestamp to epoch time

            answer = time.time() - sucess  # get the difference
            answer = answer + 18000
            print answer  # difference in seconds
            

            answer /= 60  # diff in minutes

            if answer > 0 and answer < 60:                # if under an hour just print minutes
                print "live for " + answer + " minutes"
                irc.send('PRIVMSG ' + channel + " :" + ".me Live For: " + answer + "\r\n")

            if answer > 60:      # if over an hour change to hours and seperate whole hours from the rest
                
                answer /= 60                   # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                answer -= 1  # < < < < < < < < < <# idk why but it was an hour ahead of true time
                splits = str(answer).split('.')  # ^ something to do with gmt/utc and dst? fucked if i know
                answer = splits[0]              # assuming it will be different for you.. bttv /uptime was handy
                idk = float("0." + splits[1])  # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                idk = idk * 60
                idk = str(idk).split('.')
                idk = idk[0]
                answer2 = str(answer)
                print answer + " SPACER " + answer2
                if answer2 == '0':
                    print "live for " + str(idk) + " minutes"
                    irc.send('PRIVMSG ' + channel + " :" + ".me Live For: " + str(idk) + " Minutes" + "\r\n")
                else:
                    print "live for " + str(answer) + " hours and " + str(idk) + " minutes"
                    irc.send('PRIVMSG ' + channel + " :" + ".me Live For: " + str(answer) + " Hours And " + str(idk) + " Minutes" + "\r\n")
           
            
        ut = Timer(30, unsetUt)
        ut.start()
#Points/XP/DBStarter/Steak
# def chatz():
#     global channohash
#     if liveCheck(channohash):
#         conn = sqlite3.connect('buddhalog.db')
#         c = conn.cursor()
#         url = urllib.urlopen('https://tmi.twitch.tv/group/user/' + channohash + '/chatters').read()
#         url = json.loads(url)
#         mods = url.get('chatters').get('moderators')
#         views = url.get('chatters').get('viewers')
#         # print mods
#         # print views
#         if mods != None:
#
#             c.execute('select usr from points')
#
#             test = c.fetchall()
#             try:
#                 if test[0] == None:
#                     test = ":"
#             except IndexError:
#                 print 'db empty'
#
#             for name in (mods):
#
#                 modsit = [item for item in test if item[0] == name]
#
#                 if modsit:
#
#                     # print "sucess!!!"
#                     c.execute("""update points set point = point + 10 where usr = (?)""", [name])
#                     print "adding points for " + name
#
#                     # increment points and timetot
#                     conn.commit()
#
#                 else:
#                     date = time.strftime('%d/%m/%Y')
#                     blah = "select count (*) from points"
#                     c.execute(blah)
#                     temp = c.fetchone()
#                     # print temp[0]
#                     temp = temp[0] + 1
#                     blah = "insert into points"
#
#                     c.execute(blah + " values (?,?,?,?,?)",
#                               (name, 0, temp, channohash, date))
#                     conn.commit()
#                     # c.executemany("""insert into usr Values (?,?,?,?,?)""", [(name, 1, temp, channohash, datenow),])
#
#
#                     print "added user :  " + name
#
#         for plebian in (views):
#
#             plebsit = [pleb for pleb in test if pleb[0] == plebian]
#
#             if plebsit:
#                 c.execute("""update points set point = point + 10 where usr = (?)""", [plebian])
#                 conn.commit()
#                 print "adding points for " + plebian
#             else:
#
#                 date = time.strftime('%d/%m/%Y')
#                 blah = "select count (*) from points"
#                 c.execute(blah)
#                 temp = c.fetchone()
#                 # print temp[0]
#                 temp = temp[0] + 1
#                 blah = "insert into points"
#
#                 c.execute(blah + " values (?,?,?,?,?)",
#                           (plebian, 0, temp, channohash, date))
#                 conn.commit()
#                 # c.executemany("""insert into usr Values (?,?,?,?,?)""", [(name, 1, temp, channohash, datenow),])
#
#                 print "added user : " + plebian
#         conn.commit()
#         conn.close()
#     xyz = Timer(600, chatz)
#     xyz.start()
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
def checkpoints(name):
    global waitplease
    global waitplease2
    global checkpoints
    if waitplease == False:
        waitplease2 = True

        conn = sqlite3.connect('buddhalog.db')
        c = conn.cursor()
        try:
            c.execute('select point from points where usr = (?)', [name])
            chkpoints = c.fetchone()
            temps = chkpoints[0]
            if temps < 30:
                yourrank = 0
            elif temps < 60:
                yourrank = 1
            elif temps < 120:
                yourrank = 2
            elif temps < 240:
                yourrank = 3
            elif temps < 480:
                yourrank = 4
            elif temps < 960:
                yourrank = 5
            elif temps < 1920:
                yourrank = 6
            elif temps < 3840:
                yourrank = 7
            elif temps < 7860:
                yourrank = 8
            elif temps < 15360:
                yourrank = 9
            elif temps < 30720:
                yourrank = 10
            elif temps < 61440:
                yourrank = 11
            elif temps < 122880:
                yourrank = 12

            # temps /= 100
            chkpoints = str(chkpoints[0])
            stringy = user + ": Level: " + str(yourrank)
            stringy += " Points: "

            irc.send('PRIVMSG ' + channel + " : .w " + user + " " + stringy + chkpoints + "\r\n")
            print 'PRIVMSG ' + channel + " : .w " + user + " " + stringy + chkpoints
        except Exception as e:
            print "someting went wrong, user likely not been seen by points system " + user
            irc.send('PRIVMSG ' + channel + " : .w " + user + " " + "Uh like no noodles dood" + "\r\n")
            print 'PRIVMSG ' + channel + " : .w " + user + " " + "Uh like no noodles dood"

        conn.close()

        waitplease2 = False

# 1 point per min Scale will be changed
# (1):30m (2):1h (3):2h (4):4h (5):8h (6):16h (7):32h (8):64h (9):128h (10):256h (11):512h (12):1024h
#    30     60     120    240    480    960    1920    3840    7860      15360    30720      61440

#Auto Poster Startup
uzss = Timer(150, unsetpPostTimer)
uzss.start()
unsetpPostwait = True
#Points Startup
tablecheck()
# breeeeadd = Timer(600, chatz)
# breeeeadd.start()
conn = sqlite3.connect('buddhalog.db')
c = conn.cursor()

##Main Bot Start
while True:
    #gets output from IRC server
    data = irc.recv(1024)
    # ping/pong
    if data == "PING :tmi.twitch.tv\r\n":
        irc.send("PONG :tmi.twitch.tv\r\n")

    user = data.split('!', 1)[-1]
    user = user.split('@')[0]
    message = CHAT_MSG.sub("", data)
    flags = data.split(':', 1)[0]

    if systemBootUp:


        #Startup prep for random message poster


        #System Startup Complete
        systemBootUp = False
    if unsetpPostwait == False:
        unsetpPostwait = True
        if liveCheck(channohash):
            r = random.randint(1, 5)
            if r == 1:
                irc.send("PRIVMSG " + channel + " :" + msgTwitter + "\r\n")
            elif r == 2:
                irc.send("PRIVMSG " + channel + " :" + msgSubscriber + "\r\n")
            elif r == 3:
                irc.send("PRIVMSG " + channel + " :" + msgDiscord + "\r\n")
            elif r == 4:
                irc.send("PRIVMSG " + channel + " :" + msgMerch + "\r\n")
            elif r == 5:
                irc.send("PRIVMSG " + channel + " :" + msgMerch + "\r\n")
            uzss = Timer(300, unsetpPostTimer)
            uzss.start()
    print (user + ": " + message) # new (for flags mode)
#SUB NOTIFICATION
    if "room-id=136765278" and "msg-param-sub-plan-name=Channel\sSubscription\s(thebuddha3)" and "tmi.twitch.tv USERNOTICE"in message:
        subscriber = data
        subname = subscriber.split(";")[2]
        subname = subname.split("=")[1]
        submonths = subscriber.split(";")[8]
        submonths = submonths.split("=")[1]
        if submonths == "1" or submonths == 0:
            irc.send('PRIVMSG ' + channel + ' :' + subname + " just subscribed. Welcome to Buddha's Dojo buddhaHi Spam some love in the chat for our newest member buddhaLove" + '\r\n')
        else:
            irc.send('PRIVMSG ' + channel + ' :' + subname + " just resubscribed for " + submonths + " months. Thanks for staying loyal to Buddha's Dojo buddhaHi Spam some love in the chat! buddhaLove" + '\r\n')

####LinkBlocker####LinkBlocker####LinkBlocker####LinkBlocker####LinkBlocker####LinkBlocker####LinkBlocker####LinkBlocker

    if "PRIVMSG" in data and "clips.twitch.tv" not in (message):
        if not plebcheckk(flags):
            if blacklist != None:
                xa = 0
                for pattern in blacklist:
                    strngy = "["+ blacklist[xa] + "]"
                    xa += 1
                    if re.search(strngy, message):
                        print "blabla"
                        irc.send('PRIVMSG ' + channel + ' :' + "HeyGuys" + '\r\n')
                        #nazi bot ^
                        break
            if re.search(webpatt, message):
                try:
                    print perm[user]
                    if perm[user] > 0:
                        perm[user] -= 1
                except KeyError:
                    #irc.send('PRIVMSG ' + channel + ' :' "link" + '\r\n')
                    print flags
                    irc.send('PRIVMSG ' + channel + ' :' ".timeout " + user + " " + "5" + '\r\n')
                    irc.send('PRIVMSG ' + channel + ' :' + msg1 + "@" + user + '\r\n')

    if "!cccalc" in (message):
        stringy = message.split(" ")
        firts = stringy[1] # first value
        opz = stringy[2]  # operator
        secn = stringy[3] # second val
        calcIt(firts, opz, secn)

    if message == "!quit\r\n":
        if user == "thebuddha3" or user == "breadcam" or user == "riotcam" or user == "thor10768765":
            irc.send('PRIVMSG ' + channel + " :" + "Connection Terminated... BibleThump" + "\r\n")
            irc.send('PRIVMSG ' + channel + ' :' ".w breadcam " + data + '\r\n')
            irc.send('PART ' + channel + '\r\n')
            quit()
            #broken by :quittskiifpv!quittskiifpv@quittskiifpv.tmi.twitch.tv JOIN #thebuddha3

    if "!permit" in (message):
        if "mod=1" in (flags) or "badges=broadcaster" in (flags):
            permtemp = string.split(message, " ")
            permtemp2 = permtemp[1]
            permtemp2 = string.replace(permtemp2, "\r\n", "")
            perm[permtemp2] = 1
            print permtemp2
            print perm[permtemp2]
            t = Timer(60.0, permit, [permtemp2])
            # irc.send('PRIVMSG ' + channel + " :" + permtemp2 + " has 60 seconds to post a link." + "\r\n")
            t.start()

    if "!shout" in (message):
        if "mod=1" in (flags) or "badges=broadcaster" in (flags):
            shoutout = message.split(" ", 1)
            usr = shoutout[1]
            shoutstr = "go check out twitch.tv/" + usr
            irc.send("PRIVMSG " + channel + " :" + shoutstr + "\r\n")
            time.sleep(0.2)
            irc.send("PRIVMSG " + channel + " :" + shoutstr + "\r\n")
            time.sleep(0.2)
            irc.send("PRIVMSG " + channel + " :" + shoutstr + "\r\n")
            time.sleep(0.2)
            irc.send("PRIVMSG " + channel + " :" + shoutstr + "\r\n")
            time.sleep(0.2)
            irc.send("PRIVMSG " + channel + " :" + shoutstr + "\r\n")
            if user == "thebuddha3":
                time.sleep(0.2)
                irc.send("PRIVMSG " + channel + " :" + shoutstr + "\r\n")
                time.sleep(0.2)
                irc.send("PRIVMSG " + channel + " :" + shoutstr + "\r\n")
                time.sleep(0.2)
                irc.send("PRIVMSG " + channel + " :" + shoutstr + "\r\n")
                time.sleep(0.2)
                irc.send("PRIVMSG " + channel + " :" + shoutstr + "\r\n")
                time.sleep(0.2)
                irc.send("PRIVMSG " + channel + " :" + shoutstr + "\r\n")

# Uptime Command
    if message == "!uptime\r\n":
        uptimeCheck(irc)

#Basic Commmands
    if "!playlist" in (message):
        if unsetpListwait != True:
            unsetpListwait = True
            irc.send("PRIVMSG " + channel + " :" + msgPlaylist + "\r\n")
            usl = Timer(120, unsetpList)
            usl.start()

    if message == "!sub\r\n":
        if unsetpSubwait != True:
            unsetpSubwait = True
            irc.send("PRIVMSG " + channel + " :" + msgSubscriber + "\r\n")
            uss = Timer(120, unsetpSub)
            uss.start()

    if message == "!meta\r\n":
        if unsetpMetawait != True:
            unsetpMetawait = True
            irc.send("PRIVMSG " + channel + " :" + msgMeta + "\r\n")
            uss = Timer(30, unsetpMeta)
            uss.start()

#shoutouts
    if message == "!bob\r\n":
        if unsetpBobwait != True:
            unsetpBobwait = True
            irc.send("PRIVMSG " + channel + " :" + msgBob + "\r\n")
            uss = Timer(120, unsetpBob)
            uss.start()

    if message == "!tony\r\n":
        if unsetpTonywait != True:
            unsetpTonywait = True
            irc.send("PRIVMSG " + channel + " :" + msgTony + "\r\n")
            uss = Timer(120, unsetpTony)
            uss.start()

    if message == "!reggie\r\n":
        if unsetpReggiewait != True:
            unsetpReggiewait = True
            irc.send("PRIVMSG " + channel + " :" + msgReggie + "\r\n")
            uss = Timer(120, unsetpReggie)
            uss.start()

    if message == "!peter\r\n":
        if unsetpPeterwait != True:
            unsetpPeterwait = True
            irc.send("PRIVMSG " + channel + " :" + msgPeter + "\r\n")
            uss = Timer(120, unsetpPeter)
            uss.start()

    if message == "!granny\r\n":
        if unsetpGrannywait != True:
            unsetpGrannywait = True
            irc.send("PRIVMSG " + channel + " :" + msgGranny + "\r\n")
            uss = Timer(120, unsetpGranny)
            uss.start()

# Social
    if message == "!discord\r\n":
        if unsetpDiscordwait != True:
            unsetpDiscordwait = True
            irc.send("PRIVMSG " + channel + " :" + msgDiscord + "\r\n")
            uss = Timer(60, unsetpDiscord)
            uss.start()

    if message == "!twitter\r\n":
        if unsetpTwitterwait != True:
            unsetpTwitterwait = True
            irc.send("PRIVMSG " + channel + " :" + msgTwitter + "\r\n")
            uss = Timer(60, unsetpTwitter)
            uss.start()

    if message == "!merch\r\n":
        if unsetpMerchwait != True:
            unsetpMerchwait = True
            irc.send("PRIVMSG " + channel + " :" + msgMerch + "\r\n")
            uss = Timer(60, unsetpMerch)
            uss.start()

# SLAY THE SQUIDS
    if "!squidslayer" in (message):
        if "mod=1" in (flags) or "badges=broadcaster" in (flags):
            squidBlocker = 1
            irc.send("PRIVMSG " + channel + " :" + "Squids, I'm coming for you RIP" + "\r\n")
            irc.send('PRIVMSG ' + channel + ' :' ".w breadcam " + user + '\r\n')
    if "!squidsaver" in (message):
        if "mod=1" in (flags) or "badges=broadcaster" in (flags):
            squidBlocker = 0
            irc.send("PRIVMSG " + channel + " :" + user + " just saved the squids" + "\r\n")
            irc.send('PRIVMSG ' + channel + ' :' ".w breadcam " + user + '\r\n')
    if re.search(r"Squid[1-4]", message):
        if (squidBlocker) == 1:
            irc.send('PRIVMSG ' + channel + ' :' ".timeout " + user + " " + "5" + '\r\n')

    #if "!blacklist" in (message):
    #    if "mod=1" in (flags) or "badges=broadcaster" in (flags):
    #        garbage = message.split(" ")
    #        garbage = str(garbage[1:len(garbage)])
    #        garbage = str(garbage[1:-1])

            #blacklistAdd(garbage)
            #irc.send("PRIVMSG " + channel + " :" + "\"" + garbage + "\"" " Has been added to the blacklist" + "\r\n")

#um unbanned but on warning
    if (user) == "yasirkhan123" or (user) == "billbob19" or (user) == "xeapzz" or (user) == "littlejabari":
        irc.send('PRIVMSG ' + channel + ' :' ".w breadcam " + user + " : " + message + '\r\n')

#Tell me when plebs are retarded so i can ban
    if "nigger" in (message) or "n i g g e r" in (message) or "faggot" in (message) or "f a g g o t" in (message):
        print "shit"


        irc.send('PRIVMSG ' + channel + ' :' ".w breadcam " + user + ":" + message + '\r\n')

#blacklist not working yet
    if "!blacklist" in (message):
        if "mod=1" in (flags) or "badges=broadcaster" in (flags) or (user) == "thor10768765":
            garbage = message.split(" ")
            garbage = str(garbage[1:len(garbage)])

            garbage = string.replace(garbage, "\\r\\n", "")
            print garbage
            garbage = string.replace(garbage, "\\\s", "\s")
            print garbage + " hi"
            garbage = string.replace(garbage, "['", "")
            garbage = string.replace(garbage, "']", "")
            print garbage

            if not str(garbage) in blacklist:
                blacklistAdd(str(garbage))
                irc.send("PRIVMSG " + channel + " :" + "\"" + garbage + "\"" " Has been added to the blacklist" + "\r\n")
            else:
                blacklistRem(garbage)
                irc.send("PRIVMSG " + channel + " :" + "\"" + garbage + "\"" " Has been Removed" + "\r\n")
            print blacklist

#writing msgs to DB (breaks sometimes)



#check points
    if (message) == "!level\r\n" or (message) == "!xp\r\n" or (message) == "!points\r\n" or (message) == "!noodles\r\n":
        checkpoints(user)

    if "!last" in (message):
        try:
            if "mod=1" in (flags) or "badges=broadcaster" in (flags) or (user) == "thor10768765":
                messageq = message.split(" ")
                messagereqc = messageq[0]
                messageq = messageq[1]

                messagereqc = string.replace(messagereqc, "!last", "")

                print messageq
                print messagereqc
                queryPlz(str(messageq), irc, int(messagereqc), user)
        except Exception as e:
            print e

    if message == "avon\r\n":
        irc.send('PRIVMSG ' + channel + ' :' ".timeout " + user + " " + "250" + '\r\n')

    # if "tmi.twitch.tv WHISPER thebuddha3bot" in (message):
    #     WhisperMsg = message.split(":")[2]
    #     WhisperMsg = str.replace(WhisperMsg, "\r\n", "")
    #     if "!last" in (WhisperMsg):
    #         print "test1"
    #         try:
    #             # if "mod=1" in (flags) or "badges=broadcaster" in (flags) or (user) == "thor10768765":
    #             if "!last" in (WhisperMsg):
    #                 messageq = WhisperMsg.split(" ")
    #                 messagereqc = messageq[0]
    #                 messageq = messageq[1]
    #
    #                 messagereqc = string.replace(messagereqc, "!last", "")
    #
    #                 print messageq
    #                 print messagereqc
    #                 queryPlz(str(messageq), irc, int(messagereqc), user)
    #         except Exception as e:
    #             print e

        # # if re.search(r"[cC]heer[0-9]|[Kk]appa[0-9]|[Kk]reygasm[0-9]|[Ss]wift[Rr]age[0-9]", message):
# #
# #     print message
# #
# #     message = message.split(" ")
# #     print str(len(message)) + " msglen"
# #     total = 0
# #     for i in (message):
# #         print i + " hmmm"
# #         xyy = i
# #         if re.match(r"[Cc]heer[0-9]|[Kk]appa[0-9]|[Kk]reygasm[0-9]|[Ss]wift[Rr]age[0-9]", xyy):
# #             print "yay"
# #
# #             x = re.sub("[^0-9]", "", i)
# #             print i + " i"
# #             print x + " x"
# #             total += int(x)
# #
# #     message = string.replace(str(message), "\r\n", "")
# #     # bitstotal = int(bitstotal) + total
# #
# #     if total > 100000:
# #         irc.send("PRIVMSG " + channel + " :" + ".me " + user + "Just Dropped " + str(
# #             total) + " Bits!!! Thanks For Supporting The Stream Maddafakka!! :) " + "\r\n")

    #print data
    time.sleep(0.1)
    

######################################
################Links#################
#https://tmi.twitch.tv/group/user/thebuddha3/chatters


#################CHANGE LOG#######################
#Version Codename TacoCatPizza
#Working Features
#Linkblocker, for those not in plebcheck
#!permit, mod only
#!shout <twitchname> , shoutout 5x for mods, 10x for KingBuddha
#Auto announce on new sub.
#
#
#Known um FEATURES
#Auto announce for new subs fires off when hosting
#Auto announce needs to trigger for msg share rather than the twitch annoucement. This should cover resubs.
#Um Permit
#
#Planned Features
#Setup Pleb command timer so no spam
#CSV Archives
#
#
#
#Examples
#flags
#@badges=broadcaster/1,turbo/1;color=#E100FF;display-name=Breadcam;emotes=;id=e40d4a02-6741-4fa9-847c-aeeb3d923650;mod=0;room-id=123950262;sent-ts=1494032337318;subscriber=0;tmi-sent-ts=1494032328735;turbo=1;user-id=123950262;user-type=






# #Errors
# oh shit something happened... You must not use 8-bit bytestrings unless you use a text_factory that can interpret 8-bit bytestrings (like text_factory = str). It is highly recommended that you instead just switch your application to Unicode strings.
# emmortall: @TheBuddha3 do something man please!@!@!#@!@$#!@#$!@#$!


#Saved Whisper Recieve
#thor10768765: @badges=;color=#0000FF;display-name=thor10768765;emotes=;message-id=1;thread-id=90528942_155572970;turbo=0;user-id=90528942;user-type= :thor10768765!thor10768765@thor10768765.tmi.twitch.tv WHISPER thebuddha3bot :hai
