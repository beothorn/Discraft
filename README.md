# Discraft
Discraft conects the minecraft chat with a discord channel.

Messages on Discord show up on minecraft and vice-versa.

You can also run commands on the server so *only let people you trust on your channel*

# Setup
You need python 3 to run this server. You will also need to install some dependencies:
```
pip3 install discord.py==0.16.12
pip3 install pexpect
```

You will also need to create a discord bot.

To get a channel id inside Discord, just type:
```
/#channel-name
```

Put the server.jar and this script on the same folder.

Usage:
```
python3 discraft.py BOT-TOKEN CHANNEL-ID COMMAND-TO-START-SERVER
```

Example:
```
python3 discraft.py XXXXXXXXXXXXXXXXXXXXXXXX.XXXXXX.XXXXXXXXXXXXXXXX 55555555555 "/usr/bin/java -Xmx2400M -Xms1024M -jar server.jar nogui"
```

# Commands

You can run some commands directly from Discord.

## !discraft help

Shows this file

## !mcserver server command

Runs a command on the minecraft server ( list of commands here: https://minecraft.gamepedia.com/Commands )

Example: 
```
!mcserver say hi you
```

## !discraft ip

Gets current public ip

## !discraft set-channel CHANNEL_ID

Moves the bot to another channel

Example: 
```
!discraft set-channel 55555555
```

## !discraft restart

Restarts minecraft server

## !discraft update urlToNewServer.jar

Replaces server.jar with the result from the url

Example:
```
!discraft update https://launcher.mojang.com/v1/objects/ed76d597a44c5266be2a7fcd77a8270f1f0bc118/server.jar
```

## !discraft set-command new command

Example: 
```
!discraft set-command /usr/bin/java -Xmx4G -Xms1024M -jar server.jar nogu
```

## !discraft top

Gets cpu and memory usage
