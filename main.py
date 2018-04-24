import discord
import functions as func
import random
import time
import asyncio

TOKEN = 'hah_i_didnt_forget_to_hide_it_suckers'

client = discord.Client()

fdata = 'database.csv'
femoji = 'emoji.csv'
fmarket = 'market.csv'

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
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
        if len(message.content.split(' ')) > 1:

            emoji = message.content.split(' ')[1]

            if func.isvalid(emoji,femoji) == True:
                await client.send_message(message.channel,func.make_market_branch(emoji,fmarket))
            else:
                await client.send_message(message.channel,"I am terribly sorry! I couldn't recognize the emoji `{}`.".format(emoji))

            return

        await client.send_message(message.channel,func.make_complete_market(femoji,fmarket))

    # ----------------------------------------
    #               BUY STUFF
    # ----------------------------------------
    if message.content.startswith('!bu'):

        message_table = message.content.split(' ')

        # Find all the valid emojis. If not, end with syntax error.
        if len(message_table) != 3:

            await client.send_message(message.channel,"**Invalid syntax:**\n\n`!buy <emoji> <amount>`.\n\nExample: `!buy {} 1`".format(func.import_data(femoji)[0][0]))
            return

        if func.check_for_int(message_table[1]) == True and func.isvalid(message_table[2],femoji) == True:
            if int(message_table[1]) <= 0 or int(message_table[1]) > 1000000:
                await client.send_message(message.channel,"I'm sorry, your sell value is out of bounds! Please choose a reasonable amount.")
                return

            if func.count(message.author.id,1,fdata) < int(message_table[1]):
                await client.send_message(message.channel,"I'm sorry! You do not have enough money to make this deal!")
                return

            msg, person, amount = func.buy_something(message.author,message_table[2],int(message_table[1]),femoji,fmarket,fdata)
            if person != '0':
                victim = await client.get_user_info(person)
                await client.send_message(client.get_channel("438260494743109633"),":moneybag: **{}** bought {} from **{}** for the price of {} coins!".format(message.author,message_table[2],victim,amount))
                print("{} bought {} from {} for the price of {} coins!".format(message.author,message_table[2],victim,amount))
            await client.send_message(message.channel,msg)
            return

        if func.check_for_int(message_table[2]) == True and func.isvalid(message_table[1],femoji) == True:
            if int(message_table[2]) <= 0 or int(message_table[2]) > 1000000:
                await client.send_message(message.channel,"I'm sorry, your sell value is out of bounds! Please choose a reasonable amount.")
                return

            if func.count(message.author.id,1,fdata) < int(message_table[2]):
                await client.send_message(message.channel,"I'm sorry! You do not have enough money to make this deal!")
                return

            msg, person, amount = func.buy_something(message.author,message_table[1],int(message_table[2]),femoji,fmarket,fdata)
            if person != '0':
                victim = await client.get_user_info(person)
                await client.send_message(client.get_channel("438260494743109633"),":moneybag: **{}** bought {} from **{}** for the price of {} coins!".format(message.author,message_table[1],victim,amount))
                print("{} bought {} from {} for the price of {} coins!".format(message.author,message_table[1],victim,amount))
            await client.send_message(message.channel,msg)
            return

        await client.send_message(message.channel,"**Invalid syntax:**\n\n`!buy <emoji> <amount>`.\n\nExample: `!buy {} 1`".format(func.import_data(femoji)[0][0]))
        return

    # ----------------------------------------
    #               SELL STUFF
    # ----------------------------------------
    if message.content.startswith('!s'):

        message_table = message.content.split(' ')

        # Find all the valid emojis. If not, end with syntax error.
        if len(message_table) != 3:

            await client.send_message(message.channel,"**Invalid syntax:**\n\n`!sell <emoji> <amount>`.\n\nExample: `!sell {} 100`".format(func.import_data(femoji)[0][0]))
            return

        if func.check_for_int(message_table[1]) == True and func.isvalid(message_table[2],femoji) == True:
            if int(message_table[1]) <= 0 or int(message_table[1]) > 1000000:
                await client.send_message(message.channel,"I'm sorry, your sell value is out of bounds! Please choose a reasonable amount.")
                return

            if func.count(message.author.id,func.position(message_table[2],femoji),fdata) < 1:
                await client.send_message(message.channel,"I'm sorry! You do not have the {} at your disposal to make this deal!".format(message_table[2]))
                return

            msg, person, amount = func.sell_something(message.author,message_table[2],int(message_table[1]),femoji,fmarket,fdata)
            if person != '0':
                victim = await client.get_user_info(person)
                await client.send_message(client.get_channel("438260494743109633"),":money_with_wings: **{}** sold {} to **{}** for {} coins!".format(message.author,message_table[2],victim,amount))
                print("{} sold {} to {} for {} coins!".format(message.author,message_table[2],victim,amount))
            await client.send_message(message.channel,msg)
            return

        if func.check_for_int(message_table[2]) == True and func.isvalid(message_table[1],femoji) == True:
            if int(message_table[2]) <= 0 or int(message_table[2]) > 1000000:
                await client.send_message(message.channel,"I'm sorry, your sell value is out of bounds! Please choose a reasonable amount.")
                return

            if func.count(message.author.id,func.position(message_table[1],femoji),fdata) < 1:
                await client.send_message(message.channel,"I'm sorry! You do not have the {} at your disposal to make this deal!".format(message_table[1]))
                return

            msg, person, amount = func.sell_something(message.author,message_table[1],int(message_table[2]),femoji,fmarket,fdata)
            if person != '0':
                victim = await client.get_user_info(person)
                await client.send_message(client.get_channel("438260494743109633"),":money_with_wings: **{}** sold {} to **{}** for {} coins!".format(message.author,message_table[1],victim,amount))
                print("{} sold {} to {} for the price of {} coins!".format(message.author,message_table[1],victim,amount))
            await client.send_message(message.channel,msg)
            return

        await client.send_message(message.channel,"**Invalid syntax:**\n\n`!sell <emoji> <amount>`.\n\nExample: `!sell {} 100`".format(func.import_data(femoji)[0][0]))
        return

    if message.content.startswith('!r'):

        if len(message.content.split(' ')) > 1:

            emoji = message.content.split(' ')[1]

            if func.isvalid(emoji,femoji) == True:

                await client.send_message(message.channel,'Are you sure you want to retract all offers and requests of the emoji {}?\nType `Yes` to confirm, or type `No` to cancel.')
                response = await client.wait_for_message(author = message.author)

                if response.content.startswith('Y') or response.content.startswith('y'):
                    msg_table = func.retract_emoji(message.author,emoji,fmarket,femoji,fdata)

                    for msg in msg_table:
                        await client.send_message(message.channel,msg)
                        asyncio.sleep(1)
                    await client.send_message(message.channel,"{} has been cleared!".format(emoji))
                    return

                await client.send_message(message.channel,"Retraction canceled.")
                return

        await client.send_message(message.channel,'Are you sure you want to retract all offers and requests on the *WHOLE* market?\nType `Yes` to confirm, or type `No` to cancel.')
        response = await client.wait_for_message(author = message.author)

        if response.content.startswith('Y') or response.content.startswith('y'):
            for emoji in func.import_data(femoji):
                msg_table = func.retract_emoji(message.author,emoji[0],fmarket,femoji,fdata)

                for msg in msg_table:
                    await client.send_message(message.channel,msg)
                    await asyncio.sleep(0.5)
                await client.send_message(message.channel,"{} has been cleared!".format(emoji[0]))

            await client.send_message(message.channel,"All emojis have been cleared!")
            return

        await client.send_message(message.channel,"Retraction canceled.")
        return

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
