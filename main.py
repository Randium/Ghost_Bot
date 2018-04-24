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
    #no bots pls
    if message.author.bot:
        return

    func.add_score(message.author.id,1,1,fdata)

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
        args = message.content.split(' ')
        if len(args) > 1: #shoudnt this be 2? or does len actually return count?

            emoji = args[1]
            amountS = args[2]
            if !amountS
                amountS = "1"
            amount = int(amountS)
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
