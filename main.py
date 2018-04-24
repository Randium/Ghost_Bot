import discord
import functions as func
import random
import time
import asyncio

TOKEN = 'lets_hide_that_token'

client = discord.Client()

fdata = 'database.csv'
femoji = 'emoji.csv'
fmarket = 'market_place.csv'

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    func.add_score(message.author.id,1,1,fdata)

    # ----------------------------------------
    #               BALANCE
    # ----------------------------------------
    if message.content.startswith('!b') or message.content.startswith('!$'):
        target = message.author

        if len(message.mentions) > 0:
            if len(message.mentions) > 1:
                await client.send_message(message.channel,"Whoah, dude! One person at a time, please!")
                asyncio.sleep(2)
                await client.send_message(message.channel,"Showing you the results for {}...".format(message.mentions[0]))
            target = message.mentions[0]
            print('{} has requested the balance of {}.'.format(message.author,message.mentions[0]))
        else:
            print('{} has requested the balance of themselves.'.format(message.author))

        await client.send_message(message.channel,func.make_balance(target.id,fdata,femoji,target))
        return

    # ----------------------------------------
    #               MARKET
    # ----------------------------------------
    if message.content.startswith('!m'):

        # When a specific emoji has been chosen.
        if len(message.content.split(' ')) > 1:

            emoji = message.content.split(' ')[1]

            if func.isvalid(emoji,femoji):
                await client.send_message(message.channel,func.make_market_branch(emoji,fmarket))

            return

        await client.send_message(message.channel,func.make_complete_market(femoji,fmarket))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.send_message(client.get_channel("436257067573968910"),'Beep boop! I just went online!')

    i = 0
    while True:

        print('===============================')
        print("Up and running since {} hours!".format(i))
        print('===============================')

        await asyncio.sleep(3600)
        i += 1

client.run(TOKEN)
