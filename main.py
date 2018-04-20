import discord
import functions as f
import random
import time
import asyncio

TOKEN = 'i_dont_think_anyone_reads_this_but_sure_this_is_totally_my_token'

client = discord.Client()

data_file = 'database.csv'

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # give the sender a point
    f.add_point(message.author.id,data_file,1)

    # if the user wants to check how many messages have been counted
    if message.content.startswith('!b'):
        if len(message.mentions) == 0:
            victim = message.author
            print('{} has requested the balance of themselves.'.format(message.author))
        else:
            if len(message.mentions) > 1:
                await client.send_message(message.channel,'Dude, relax! Only one balance at a time, jeez!')
                time.sleep(2)
                await client.send_message(message.channel,'Here, the least I can do, is to give you the first person you mentioned.')
                time.sleep(2)
            victim = message.mentions[0]
            print('{0.author} has requested the balance of {0.mentions[0]}.'.format(message))

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


    # if the user wants to transfer their money
    elif message.content.startswith('!t'):
        if len(message.content.split(' ')) != 3:
            await client.send_message(message.channel,'**Invalid syntax:**\n\n`!transfer <amount> <recipient>`.\n\nExample: `!transfer @Randium#6521 1`')
            return

        amount = 0
        amount_found = False
        name_location = 0

        # Looks for an integer between the arguments
        for i in range(len(message.content.split(' '))):
            if f.check_for_int(message.content.split(' ')[i]) == True:
                amount_found = True
                amount = int(message.content.split(' ')[i])
                if i == 1:
                    name_location = 2
                elif i == 2:
                    namelocation = 1
                else:
                    await client.send_message(message.channel,"Hmmm, that's weird...\nSomething seems to have gone wrong. Make sure to let <@248158876799729664> know about this.")
                    print("i seems to have an invalid value - its value is {}!".format(i))
                    return

        if amount_found == False:
            await client.send_message(message.channel,'**ERROR:** Amount not recognized.\n\n`{0.content}`\nThe third argument is not recognized as a number.\n\nPlease type `!help transfer` if you want a more detailed explanation on the use of this command.'.format(message))
            return

        amount = int(amount)

        if amount > f.check_money(message.author.id,data_file):
            print('{0.author} attempted to make a business transaction, but failed due to lacking the given amount.'.format(message))
            await client.send_message(message.channel,"I'm terribly sorry, {0.author.id}!\nYou don't have enough money for that!".format(message))
            return
        elif amount == 0:
            print('{0.author} attempted to make a business transaction, but failed due to the invalid amount.'.format(message))
            await client.send_message(message.channel,"The amount to transfer must be higher than zero, buddy. :wink:")
            return
        elif amount < 0:
            print('{0.author} attempted to make a business transaction, but failed due to the invalid amount.'.format(message))
            await client.send_message(message.channel,"A smart guy, huh? Don't worry, no exploits for you. I've already thought of this. :wink:")
            return

        if len(message.mentions) == 0:
            print('{0.author} attempted to make a business transaction, but failed due to the invalid amount.'.format(message))
            await client.send_message(message.channel,"I'm sorry, you haven't mentioned anyone! Please tell us who you want to transfer your monoey to. :hugging:")
            return

        time.sleep(2)
        await client.send_message(message.channel,'Transaction ready.\nAre you sure you want to send {0} coins to **{1.mentions[0]}**, <@{1.author.id}>?'.format(amount,message))
        await client.send_message(message.channel,'Please type `yes` to confirm.')
        response = await client.wait_for_message(author = message.author)

        if response.content.startswith('y') or response.content.startswith('Y'):
            f.add_point(message.mentions[0].id,data_file,amount)
            f.add_point(message.author.id,data_file,-amount)
            await client.send_message(message.channel,'Money successfully sent!')
            print("{0.author} has successfully transferred {1} coins to {0.mentions[0]}".format(message,amount))
            return

        await client.send_message(message.channel,"Business transaction canceled.")
        print('{0.author} has canceled a business transaction after having made one.'.format(message))

    # if the text starts (most likely) with a mention
    elif message.content.startswith('<@') and f.check_for_int(message.content[2:16]):
        msg = '{0.author.mention}, it is not very humble to start a message with a mention!'.format(message)
        await client.send_message(message.channel,msg)

        if random.random() > 0.8:
            await asyncio.sleep(2)
            await client.send_message(message.channel,'...wow. That was ironic.')

    # if the command !hello is called
    elif message.content.startswith('!hello'):
        msg = 'Hello there, {0.author.mention}!'.format(message)
        print('{} said hello to me.'.format(message.author.id))
        await client.send_message(message.channel, msg)

    elif ' i ' in message.content:
        await client.send_message(message.channel,'Did you just refer to yourself in lowercase? :scream:')

    elif message.content.startswith('i '):
        await client.send_message(message.channel,'Did you just refer to yourself in lowercase? :scream:')


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
