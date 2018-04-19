import discord
import functions as f
import random
import time

TOKEN = 'NDM2MjYyNjEzMjA3NDgyMzc4.Dbk8vg.9d0zTqhyj_LE47FxD2KEP9UDWQA'

client = discord.Client()

data_file = 'database.csv'

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # give the sender a point
    f.add_points(message.author.id,data_file,1)

    # if the user wants to check how many messages have been counted
    if message.content.startswith('!b'):
        if len(message.mentions) == 0:
            victim = message.author
        else:
            if len(message.mentions) > 1:
                await client.send_message(message.channel,'Dude, relax! Only one balance at a time, jeez!')
                time.sleep(2)
                await client.send_message(message.channel,'Here, the least I can do, is to give you the first person you mentioned.')
                time.sleep(2)
            victim = message.mentions[0]

        balance = f.check_money(victim.id,data_file)

        if balance != 0:
            msg = '__**BALANCE:**__\n'
            msg += '\n'
            msg += 'Money: {}\n'.format(balance)
            msg += '\n'
            msg += 'Balance Owner: **{}**'.format(victim)

            await client.send_message(message.channel,msg)
            return

        await client.send_message(message.channel,"I'm terribly sorry. For some reason, I couldn't find the player you're looking for.")
        time.sleep(2)
        await client.send_message(message.channel,"Maybe I haven't seen them typing before, or maybe they're just broke.")


    # if the text starts (most likely) with a mention
    if message.content.startswith('@') or message.content.startswith('<@'):
        msg = '{0.author.mention}, it is not very humble to start a message with a mention!'.format(message)
        await client.send_message(message.channel,msg)

        if random.random() > 0:
            await client.send_message(message.channel,'...wow. That was ironic.')

    # if the command !hello is called
    if message.content.startswith('!hello'):
        msg = 'Hello there, {0.author.mention}!'.format(message)
        print('{} said hello to me.'.format(message.author.id))
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.send_message(client.get_channel("436257067573968910"),'Beep boop! I just went online!')
    # wait for two message, 'cause it detects its own message as well.
    await client.wait_for_message(channel = client.get_channel("436257067573968910"))

    await client.send_message(client.get_channel("436257067573968910"),'Very cool indeed!')

client.run(TOKEN)
