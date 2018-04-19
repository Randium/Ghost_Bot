import discord
import functions as f
import random

TOKEN = 'hell_yeah_randium_rocks'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    f.add_point(message.author.id,'database.csv')

    if message.content.startswith('@') or message.content.startswith('<'):
        msg = '{0.author.mention}, it is not very humble to start a message with a mention!'.format(message)
        await client.send_message(message.channel,msg)

        if random.random() > 0:
            await client.send_message(message.channel,'...wow. That was ironic.')

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

client.run(TOKEN)
