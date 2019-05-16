import pexpect
import time
import re
import discord
import sys

import threading

chat_output = re.compile("(\[\d\d:\d\d:\d\d\]).*: (\<.*\> .*)")
command_pattern = re.compile("!mine (.*)")


p = pexpect.spawn('java -Xmx2400M -Xms1024M -jar server.jar nogui')
p.setecho(False)

def echoback(stringin):
    p.sendline(stringin)
    echoback = p.readline()
    return echoback.decode();

TOKEN = sys.argv[1]

print("BEFORE CLIENT")

client = discord.Client()

print("AFTER CLIENT")

@client.event
async def on_message(message):
    print("Received message")
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!mine'):
        command = command_pattern.match(message.content)[1]
        p.sendline(command)
        await client.send_message(message.channel, "command executed on minecraft")
        return
    p.sendline("say %s :%s" % (message.author, message.content))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def listen_to_server():
    while (True):
        out = p.readline().decode("utf-8")
        match_result = chat_output.match(out)
        if match_result:
            print(match_result.groups()[1])
        else:
            print("print %s" % out)
        time.sleep (0.05)


thr = threading.Thread(target=listen_to_server, args=(), kwargs={})
thr.start()

client.run(TOKEN)
