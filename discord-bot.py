import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import sys

# init client
client = Bot(description="BOT NAME by iggnore#0001", command_prefix="PUT YOUR PREFIX HERE", pm_help = False)

# open private key file
key_file = open('./discord_key.txt', 'r')
if not key_file:
	print('File discord_key.txt can\'t be found')
	sys.exit(0)

# read private key from file
api_key = key_file.read().splitlines()[0]
if not api_key:
	print('No API key in discord_key.txt')
	sys.exit(0)

# close private key file
key_file.close()

@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	return await client.change_presence(game=discord.Game(name='PLAYING STATUS HERE'))

@client.command()
async def ping(*args):

	await client.say("REACT TO PING") # message
	await asyncio.sleep(3) # wait for x seconds
	await client.say("REACT TO PING 2") # message
	
@client.event
async def on_message(message):
	await client.send_message(message.channel, message.content)

client.run(str(api_key)) # Send API key from opened file
