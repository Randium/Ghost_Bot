import discord
import functions as func
import random
import time
import asyncio

TOKEN = 'this_is_where_your_token_goes_buddy'

client = discord.Client()

fliving = 'living.csv'
fdata = 'database.csv'
femoji = 'emoji.csv'
fmarket = 'market.csv'

bot_spam = "439157069703020544"
stock_market = "438260494743109633"
welcome_channel = "438359881339109376"
play_zone = "438359881339109376"
game_log = "439745133618003969"

authorized = [248158876799729664, 140424290171486208]

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    #no bots pls
    if message.author.bot:
        return

    if int(message.author.id) not in authorized:
        func.add_score(message.author.id,1,1,fliving)

    # Makes sure the player is still alive or at least signed up (we do not want to give any spoilers!)
    if func.is_still_alive(message.author,fdata) and not int(message.author.id) in authorized:
        return

    if message.server == client.get_server("436257067573968908") and not message.channel == client.get_channel(play_zone) and message.content.startswith('!') and not int(message.author.id) in authorized:
        answer = await client.send_message(message.channel,"Wrong channel, buddy! Please go to <#{}> or to my DMs to play with the bot.".format(play_zone))
        await asyncio.sleep(10)
        await client.delete_message(answer)
        return

    # ----------------------------------------
    #               HELP
    # ----------------------------------------
    if message.content.startswith('!h') and not (message.channel == client.get_channel(game_log) or message.channel == client.get_channel(stock_market)):
        msg = ''
        args = message.content.split(' ')

        if len(args) == 1:
            msg += '`!balance` - View the balance of a user\n'
            msg += '`!buy` - Buy certain items'
            msg += '`!description` - View the meaning of all emojis\n'
            msg += '`!market` - View the market\n'
            msg += "`!retract` - Retract certain offers or requests you've made\n"
            msg += '`!sell` - Sell certain items\n'
            if int(message.author.id) in authorized:
                msg += '\n\n**Admin commands:**\n'
                msg += '`!kill` - Kill a player, effectively allowing them to participate on the market.\n'
                msg += '`!redeem` - Redeem a coin and make it invalid\n'
            msg += '\n To view the specific documentation of a command, please type `!help <command>`.'

        elif args[1].startswith('ba'):
            msg += '`!balance` - View your own balance.\n'
            msg += '`!balance <user>` - View the balance of a specific user. The user is a mention.'
        elif args[1].startswith('bu'):
            msg += '`!buy <emoji> <amount>` - Buy a certain emoji for a certain amount.'
        elif args[1].startswith('d'):
            msg += '`!description` - Get an explanation of what certain emojis mean.\n'
            msg += 'If a desciption reads **Player coin**, that means that the emoji is redeemed when the corresponding player dies.'
        elif args[1].startswith('m'):
            msg += '`!market` - See an overview of the whole market.\n'
            msg += '`!market <emoji> - See an overview of the market of a specific emoji. Make sure the emoji exists on the market.`'
        elif args[1].startswith('ret'):
            msg += "`!retract` - Retract all offers and requests you've made on the whole market.\n"
            msg += "`!retract` - Retract all offers and requests you've made on a specific emoji."
        elif args[1].startswith('s'):
            msg += '`!sell <emoji> <amount>` - Sell a certain emoji for a certain amount.'
        elif args[1].startswith('k'):
            if int(message.author.id) in authorized:
                msg += '`!kill <user> <emoji> <amount>` - Kill a user that got voted out by `<amount>` players. The user had `<emoji>` as their emoji in the game.'
            else:
                msg += "You're not even an admin! Why bother looking up this command?"
        elif args[1].startswith('red'):
            if int(message.author.id) in authorized:
                msg += '`!redeem <emoji> <amount>` - Remove a given emoji from the market, and pay all users a given amount for each emoji they had left.'
            else:
                msg += "You're not even an admin! Why bother looking up this command?"
        else:
            msg += "I am terribly sorry! I did not understand what command you meant to type!\n"
            msg += "Please type `!help` for help."

        await client.send_message(message.channel,msg)



    # ----------------------------------------
    #               DESCRIPTION
    # ----------------------------------------
    if message.content.startswith('!d'):
        await client.send_message(message.channel,func.show_desc(femoji))

    # ----------------------------------------
    #               KILL FUNCTION
    # ----------------------------------------
    if int(message.author.id) in authorized and message.content.startswith('!kill') and len(message.mentions) > 0:

        if len(message.content.split(' ')) != 4:
            await client.send_message(message.channel,"**Invalid syntax:**\n\n`!kill <player> <emoji> <amount>`.\n\nExample: `!kill @Randium#6521 😏 12`")
            return


        currency = message.content.split(' ')[2]
        amount = message.content.split(' ')[3]

        if not func.check_for_int(amount):
            await client.send_message(message.channel,"**ERROR:** Invalid amount!")
            return

        amount = int(amount)
        victim = message.mentions[0]

        if int(victim.id) in authorized:
            await client.send_message(message.channel,"I am terribly sorry, but I can't kill an admin! That'd be treason.")
            return

        await client.send_message(client.get_channel(bot_spam),"Are you sure you want to kill <@{}>?\nPlease type `Yes` to confirm.".format(victim.id))

        if func.isvalid(currency,femoji):
            await client.send_message(client.get_channel(bot_spam),"Careful! The emoji you gave up is still valid! You can override by typing `Yes`, but I would advise saying `No`!")
            await client.send_message(client.get_channel(bot_spam),"You can override emojis by typing `!redeem {} <amount>`.".format(currency))

        response = await client.wait_for_message(author = message.author,channel = client.get_channel(bot_spam))

        if not response.content[0] in ['y', 'Y']:
            await client.send_message(response.channel,"Kill function canceled.")
            return

        msg, money = func.kill(victim,fdata,fliving,femoji)
        await client.send_message(client.get_channel(bot_spam),msg)
        if msg[-1] == '!':
            msg = "Hey there, buddy! It seems like you have died!\n"
            msg += "Though the game may be over for you as a living player, it will still be very interesting for you while you're dead!"
            msg += " How so? Well, it is time to use your knowledge about the game to become the richest ghost of all!\n"
            msg += "Players weren't allowed to use the :ghost: emoji as their avatar. Why not? Because that emoji now has a meaning to the dead - it's ectoplasm."
            msg += " The money of the dead.\n\n"
            msg += "See, every player, every team has a type of coin. When a player dies, their coins will be exchanged for money."
            msg += " For example, when you died, your {} coin was exchanged for money.".format(currency)
            msg += " How much? Well, in total, {} players voted to kill you, so every player gained {} ectoplasm for each {} coin they had.\n\n".format(amount,100*amount,currency)
            msg += "Because of your activity, you will gain {} ectoplasm and 10 of every coin as a starter pack.".format(money)
            msg += " Buy and sell these coins on the market to get rich! The player who has the most ectoplasm at the end of the game, wins a special victory badge! Enjoy!"
            await client.send_message(victim,msg)
            await client.send_message(client.get_channel(game_log),"<@{}> has been killed.".format(victim.id))
        return

    # ----------------------------------------
    #               REDEEM COINS
    # ----------------------------------------
    if int(message.author.id) in authorized and message.content.startswith('!red'):
        if len(message.content.split(' ')) != 3:
            await client.send_message(message.channel,"**Invalid syntax:**\n\n`!redeem <emoji> <amount>`.\n\nExample: `!redeem 😏 12`")
            return

        currency = message.content.split(' ')[1]
        amount = message.content.split(' ')[2]

        if not func.check_for_int(amount) or not func.isvalid(currency,femoji):
            await client.send_message(message.channel,"**Invalid syntax:**\n\n`!redeem <emoji> <amount>`.\n\nExample: `!redeem 😏 12`")
            return

        amount = int(amount)

        await client.send_message(client.get_channel(bot_spam),"Are you sure you want to exchange the {} coin for {} ectoplasm?\nPlease type `Yes` to confirm.".format(currency,amount))

        response = await client.wait_for_message(author = message.author,channel = client.get_channel(bot_spam))

        if not response.content[0] in ['y', 'Y']:
            await client.send_message(response.channel,"Money redeem function canceled.")
            return

        score_table = func.import_data(fdata)

        for user in score_table:
            target = await client.get_user_info(user[0])
            user_amount = user[func.position(currency,femoji)]

            func.retract_emoji(target,currency,fmarket,femoji,fdata)

            user[1] = int(user[1]) + amount * int(user_amount)
            if int(user_amount) > 0:
                await client.send_message(target,"The emoji {} has been redeemed for {} ectoplasm! You had {} emojis, meaning that you gained {} coins.".format(currency,amount,user_amount,int(user_amount)*amount))
            user[func.position(currency,femoji)] = 0

        func.save(score_table,fdata)

        emojis = func.import_data(femoji)
        emojis[func.position(currency,femoji)-2][0] = 'N'
        func.save(emojis,femoji)

        await client.send_message(client.get_channel(game_log),"The emoji {} has been redeemed for {} ectoplasm.".format(currency,amount))
        print("The emoji {} has been cleared succesfully.".format(currency))
        await client.send_message(client.get_channel(bot_spam),"The emoji {} has been succesfully redeemed for {} per emoji!".format(currency,amount))
        return

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
            if !amountS:
                amountS = "1"
            amount = int(amountS)
            if func.isvalid(emoji,femoji):
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
                await client.send_message(client.get_channel(stock_market),":moneybag: **{}** bought {} from **{}** for the price of {} coins!".format(message.author,message_table[2],victim,amount))
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
                await client.send_message(client.get_channel(stock_market),":moneybag: **{}** bought {} from **{}** for the price of {} coins!".format(message.author,message_table[1],victim,amount))
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
                await client.send_message(client.get_channel(stock_market),":money_with_wings: **{}** sold {} to **{}** for {} coins!".format(message.author,message_table[2],victim,amount))
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
                await client.send_message(client.get_channel(stock_market),":money_with_wings: **{}** sold {} to **{}** for {} coins!".format(message.author,message_table[1],victim,amount))
                print("{} sold {} to {} for the price of {} coins!".format(message.author,message_table[1],victim,amount))
            await client.send_message(message.channel,msg)
            return

        await client.send_message(message.channel,"**Invalid syntax:**\n\n`!sell <emoji> <amount>`.\n\nExample: `!sell {} 100`".format(func.import_data(femoji)[0][0]))
        return
    # ----------------------------------------
    #               RETRACT
    # ----------------------------------------

    if message.content.startswith('!ret'):

        if len(message.content.split(' ')) > 1:

            emoji = message.content.split(' ')[1]

            if func.isvalid(emoji,femoji) == True:

                await client.send_message(message.channel,'Are you sure you want to retract all offers and requests of the emoji {}?\nType `Yes` to confirm, or type `No` to cancel.')
                response = await client.wait_for_message(author = message.author)

                if response.content.startswith('Y') or response.content.startswith('y'):
                    msg = func.retract_emoji(message.author,emoji,fmarket,femoji,fdata)
                    if msg != '':
                        await client.send_message(message.channel,msg)
                    await client.send_message(message.channel,"{} has been cleared!".format(emoji))
                    await asyncio.sleep(1)
                    return

                await client.send_message(message.channel,"Retraction canceled.")
                return

        await client.send_message(message.channel,'Are you sure you want to retract all offers and requests on the *WHOLE* market?\nType `Yes` to confirm, or type `No` to cancel.')
        response = await client.wait_for_message(author = message.author)

        if response.content.startswith('Y') or response.content.startswith('y'):
            for emoji in func.import_data(femoji):
                msg = func.retract_emoji(message.author,emoji[0],fmarket,femoji,fdata)
                if msg != '':
                    await client.send_message(message.channel,msg)
                await client.send_message(message.channel,"{} has been cleared!".format(emoji[0]))
                await asyncio.sleep(1)

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
    await client.send_message(client.get_channel(welcome_channel),'Beep boop! I just went online!')

    i = 0
    while True:

        print('===============================')
        print("Up and running since {} hours!".format(i))
        print('===============================')

        await asyncio.sleep(3600)
        i += 1

client.run(TOKEN)
