import discord
import functions as func
import random
import time
import asyncio

TOKEN = 'randiums_bot_may_be_a_little_more_structured_since_the_last_update'

client = discord.Client()

fdata = 'database.csv'
femoji = 'emoji_data.csv'
fmarket = 'market_place.csv'

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    func.add_score(message.author,1,1)

    # ----------------------------------------
    #               BALANCE
    # ----------------------------------------
    if message.content.startswith('!ba'):
        target = message.author

        if len(message.mentions) > 0:
            if len(message.mentions) > 1:
                await client.send_message(message.channel,"Whoah, dude! One person at a time, please!")
                asyncio.sleep(2)
            await client.send_message(message.channel,"Showing you the results for {}...".format(message.mentions[0]))
            target = message.mentions[0]


        await client.send_message(message.channel,func.make_balance(target,fdata))
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
