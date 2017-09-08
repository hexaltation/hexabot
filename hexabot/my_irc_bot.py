#!/usr/bin/env python3
# coding: utf-8

import pymysql
import config
import socket
import sys
import datetime
import os
 
 
class IRC:
    """
        Implementation of a minimalist IRC BOT by Grégoire Cutzach Aka Hexaltation
        Based on Sean Golin's Tutorial
        https://linuxacademy.com/blog/geek/creating-an-irc-bot-with-python3/
    """
 
    irc = socket.socket()

  
    def __init__(self):  
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_list = {   "!commands": "Display list of commands",
                                "!answer": "Give answer to Life the Universe"
                                           "and all the rest",
                            }
        self.writepath = '/home/gc/Rendu/Python_d03/ircbot.log'
        self.connect('chat.freenode.net', 'hexabot')
        self.main('#hexatest')


    def log(self, text):
        """Log of chan activities"""

        mode = 'a' if os.path.exists(self.writepath) else 'w'
        with open(self.writepath, mode) as logfile:
                logfile.write(text)


    def send(self, chan, msg):
        """Send a message to a channel"""

        text = "PRIVMSG " + chan + " :" + msg + "\n"
        self.irc.send((text).encode('utf-8'))
        self.log("HEXABOT : " +text)
 

    def connect(self, server, botnick):
        """Connection to the server with a socket"""
        
        print("connecting to:"+server)
        #connects to the server
        self.irc.connect((server, 6667))
        #user authentication
        self.irc.send(("USER " + botnick + " " + botnick +" " + botnick
                       + " :This is a fun bot!\n").encode('utf-8'))
        #sets nickname
        self.irc.send(("NICK " + botnick + "\n").encode('utf-8'))
        #identify with nickserv
        #sets nickname
        self.irc.send(("PRIVMSG Nickserv :IDENTIFY freenodeisforhexabot\n").encode('utf-8'))


    def join_chan(self, chan):
        """Joining channel"""
        
        self.irc.send(("JOIN " + chan + "\n").encode('utf-8'))


    def get_commands(self, chan):
        """Display list of bot's commands"""
        
        msg = "Here is the list of avalaible commands :"
        self.send(chan, msg)
        msg = "Usage :         nameOfBot !nameOfCommand"
        self.send(chan, msg)
        for command, usage in self.command_list.items():
            msg = command +": "+ usage
            self.send(chan, msg)


    def access_db(self, request):
        """Connection to db and request execution"""

        conn = pymysql.connect(host='localhost', port=3306, user='bob',
                           passwd='sponge', db='irc_hexatest')
        cur = conn.cursor()
        cur.execute(request)

        result = cur.fetchone()
        if result != None:
            return True
        else:
            return False


    def main(self, chan):
        """main function"""
        
        self.join_chan(chan)
        self.irc.send(('TOPIC '+chan+' :Welcome to '+chan+ '.'
                  + 'to get list of bot commands : "hexabot !commands"\n').encode('utf-8'))
        run = True

        while run:
            #receive the text
            text=self.irc.recv(2040).decode("utf-8")

            #Ping Pong battle
            if text.find('hexabot PING') != -1:
                self.send(chan, 'PONG')
            #Call to display commands
            elif text.find('hexabot !commands') != -1:
                self.get_commands(chan)
            #THE ANSWER   
            elif text.find('hexabot !answer') != -1:                    
                self.send(chan, '42')
            #Admin command to stop bot
            elif text.find('hexabot !rhaus') != -1:
                account = text.split('!')[0][1:]
                if self.access_db("SELECT status from users where status = 1 "
                                  "and account = '"+account+"'"):
                    self.send(chan, "SCHNELLLLLLL\n")
                    self.send(chan, chr(1)+"ACTION leave the room whispering+"+chr(1)+"\n")
                    self.irc.send("QUIT \n".encode('utf-8'))
                    run = False
            #Users welcoming and rights granting
            elif text.find('JOIN #hexatest') != -1:
                account = text.split('!')[0][1:]
                self.send(chan, 'Everybody say hello to '+account)
                if self.access_db("SELECT status from users where status = 1 "
                                  "and account = '"+account+"'"):
                    self.irc.send(('MODE '+chan+" +o "+account+"\n").encode('utf-8'))
                elif self.access_db("SELECT status from users where status = 2 "
                                    "and account = '"+account+"'"):
                    self.irc.send(('MODE '+chan+" +v "+account+"\n").encode('utf-8'))
                elif self.access_db("SELECT status from users where status = 0 "
                                    "and account = '"+account+"'"):
                    self.irc.send(('MODE '+chan+" +b "+account+"\n").encode('utf-8'))

            self.log(text)
            
