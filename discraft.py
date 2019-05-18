import pexpect
import time
import re
import discord
import sys
import asyncio
import requests
import subprocess

if len(sys.argv) < 3:
    print("Usage: python3 discraft.py BOT-TOKEN CHANNEL-ID MINECRAFT-JAVA-COMMAND")
    print("Discraft must be on the same path as the server.jar")
    print('Example: python3 discraft.py XXXXXXXXXXXXXXXXXXXXXXXX.XXXXXX.XXXXXXXXXXXXXXXX 55555555555 "/usr/bin/java -Xmx2400M -Xms1024M -jar server.jar nogui"')
    exit()


TOKEN = sys.argv[1]
CHANNEL_ID = sys.argv[2]
MINECRAFT_SERVER_CMD = sys.argv[3]

p = pexpect.spawn(MINECRAFT_SERVER_CMD, timeout=1)
p.setecho(False)

client = discord.Client()

def load_regexes_for_relaying_messages_from_server():
    messages_regexes = []
    with open('./discord_msgs.txt') as f:
        discord_msgs = f.readlines()

    for reg in [x.strip() for x in discord_msgs]:
        messages_regexes.append(re.compile(reg))

    return messages_regexes

relay_patterns = load_regexes_for_relaying_messages_from_server()

async def listen_to_server():
    global CHANNEL_ID
    await client.wait_until_ready()
    channel = discord.Object(id=CHANNEL_ID)
    msg_info = re.compile(".*: (.*)")
    while (True):
        try:
            line = p.readline()
            out = line.decode("utf-8")
            print(out, end='')
            for pattern in relay_patterns:
                result = pattern.match(out)
                if result:
                    await client.send_message(channel, msg_info.match(out).groups()[0])
                    break
        except pexpect.exceptions.TIMEOUT:
            pass
        except Exception as e:
            print("This is an error message! %s" % str(e))
        await asyncio.sleep(0.05)

command_args_pattern = re.compile("!([^\s]*) ([^\s]*) (.*)")
command_pattern = re.compile("!([^\s]*) ([^\s]*)$")

@client.event
async def on_message(message):
    global CHANNEL_ID
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    channel = message.channel
    channel_id = channel.id

    if channel_id != CHANNEL_ID:
        return

    content = message.content
    author = message.author

    mcserver = "mcserver"
    discraft = "discraft"

    single_command = command_pattern.match(content)
    if single_command:
        type = single_command[1]
        command = single_command[2]
        if type == mcserver:
            p.sendline(command)
            await client.send_message(channel, ("command '%s' executed on minecraft",(command,)) )
            return
        if type == discraft:
            if command == "ip":
                result = requests.get("https://www.canihazip.com/s")
                await client.send_message(channel, result.text)
                return
            if command == "top":
                result = subprocess.run(["top","-b","-n","1"], stdout=subprocess.PIPE)
                output = "\n".join(result.stdout.decode('utf-8').split('\n')[0:10])
                await client.send_message(channel, "top:\n %s" % output)
                return

    command_w_args = command_args_pattern.match(content)
    if command_w_args:
        type = command_w_args[1]
        command = command_w_args[2]
        args = command_w_args[3]

        if type == mcserver:
            command_args_concat = "%s %s" % (command, args)
            p.sendline(command_args_concat)
            await client.send_message(channel, ("command '%s' executed on minecraft" % (command_args_concat)) )
            return
        if type == discraft:
            if command == "set-channel":
                await client.send_message(channel, "I was told that I should use another channel, bye people ;)")
                CHANNEL_ID = args
                new_channel = discord.Object(id=args)
                await client.send_message(new_channel, "Hey, someone told me to use this channel :)")
                return

    p.sendline("say %s :%s" % (author, content))

@client.event
async def on_ready():
    print("Bot logged in as '%s' with id '%s' " % (client.user.name, client.user.id))

client.loop.create_task(listen_to_server())
client.run(TOKEN)
