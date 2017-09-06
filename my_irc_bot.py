#!/usr/bin/env python3

#import pymysql
import config
import socket
import sys
import datetime
 
 
class IRC:
    """Implementation of a minimaliste IRC BOT by Grégoire Cutzach"""
 
    irc = socket.socket()

  
    def __init__(self):  
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_list = {   "!commands": "Display list of commands",
                                "!answer": "Give answer to Life the Universe and all the rest",
                            }
        self.connect('chat.freenode.net', 'hexabot')
        self.main('#hexatest')

 
    def send(self, chan, msg):
        """Send a message to a channel"""
        
        self.irc.send(("PRIVMSG " + chan + " :" + msg + "\n").encode('utf-8'))

 
    def connect(self, server, botnick):
        """Connection to the server with a socket"""
        
        print("connecting to:"+server)
        self.irc.connect((server, 6667))                                #connects to the server
        self.irc.send(("USER " + botnick + " " + botnick +" " + botnick
                       + " :This is a fun bot!\n").encode('utf-8'))     #user authentication
        self.irc.send(("NICK " + botnick + "\n").encode('utf-8'))       #sets nickname


    def join_chan(self, chan):
        """Joining channel"""
        
        self.irc.send(("JOIN " + chan + "\n").encode('utf-8'))        #join the chan


    def get_commands(self, chan):
        """Display list of bot's commands"""
        
        msg = "Here is the list of avalaible commands :"
        self.send(chan, msg)
        for command, usage in self.command_list.items():
            msg = command +": "+ usage
            self.send(chan, msg)


    def main(self, chan):
        """main function"""
        
        self.join_chan(chan)
        while 1:
            text=self.irc.recv(2040).decode("utf-8")                    #receive the text

            if text.find('PING') != -1:
                self.send(chan, 'PONG')
            elif text.find('!commands') != -1:
                self.get_commands(chan)
            elif text.find('!answer') != -1:
                self.send(chan, '42')
            elif text.find('!rhaus') != -1:
                self.send(chan, "SCHNELLLLLLL\n")
                self.irc.send("QUIT \n".encode('utf-8'))
            
