# Discraft
Discraft conects the minecraft chat with a discord channel.
Messages on Discord show up on minecraft and vice-versa.
Run commands from discord using !mine command

Put discraft.py and discord_msgs.txt in the same folder as the server.

Example:
python3 discraft.py XXXXXXXXXXXXXXXXXXXXXXXX.XXXXXX.XXXXXXXXXXXXXXXX 55555555555 "/usr/bin/java -Xmx2400M -Xms1024M -jar server.jar nogui"

Commands:

!mcserver server command

Runs a command on the minecraft server ( list of commands here: https://minecraft.gamepedia.com/Commands )

Example: !mcserver say hi you

!discraft ip

Gets current public ip

!discraft set-channel CHANNEL_ID

Moves the bot to another channel

Example: !discraft set-channel 55555555

!discraft top

Gets cpu and memory usage
