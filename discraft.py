import pexpect
import time
import re
import discord
import sys
import asyncio

TOKEN = sys.argv[1]
CHANNEL_ID = sys.argv[2]

command_pattern = re.compile("!mine (.*)")

p = pexpect.spawn('java -Xmx2400M -Xms1024M -jar server.jar nogui', timeout=1)
p.setecho(False)

client = discord.Client()

@client.event
async def on_message(message):
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

msg_info = re.compile(".*: (.*)")

with open('./discord_msgs.txt') as f:
    discord_msgs = f.readlines()

relay_patterns = []

for reg in [x.strip() for x in discord_msgs]:
    relay_patterns.append(re.compile(reg))

async def listen_to_server():
    await client.wait_until_ready()
    channel = discord.Object(id=CHANNEL_ID)
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

client.loop.create_task(listen_to_server())
client.run(TOKEN)
