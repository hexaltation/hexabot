Hexabot is a minimal IRC BOT by Grégoire Cutzach Aka Hexaltation
Based on Sean Golin's Tutorial
https://linuxacademy.com/blog/geek/creating-an-irc-bot-with-python3/


Python 3.6 or higher is required.

It requires a mysql database.
You can import the hexabot.sql file doing :

mysql -u <username> -p <databasename> < <filename.sql>

From today you have to change db and irc connections parameters in my_irc_bot.py file.
Soon it will be fixed into config.py

After configuration is done do :

python3.6 setup.py build



Enjoy