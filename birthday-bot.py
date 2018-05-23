import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import sys
import sqlite3
import datetime

# connect db
conn = sqlite3.connect('birthdays.db')
db = conn.cursor()

# init client
client = Bot(description="Birthday Bot by iggnore#0001", command_prefix="<", pm_help = False)

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

async def check_birthdays():
	await client.wait_until_ready()

	server = discord.utils.get(client.servers, name='South African Gaming')
	role = discord.utils.get(server.roles, name='Birthday')

	while not client.is_closed:
		today = datetime.datetime.today().date().__format__("%d-%m")
		ids = db.execute("select id from birthdays where birthday=?", (today,))

		# remove birthday roles for previous day
		for member in set(client.get_all_members()):
			if role not in member.roles:
				continue
			await client.remove_roles(member, role)
			print("Removed role from {} on {}".format(member.name, today))

		# add birthday roles for current day
		for idx in ids:
			for member in set(client.get_all_members()):
				if str(idx[0]) != member.id:
					continue

				await client.add_roles(member, role)
				print("Added role for {} on {}".format(member.name, today))
				break

		await asyncio.sleep(86400) # task runs every 24 hours

@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot'.format(client.user.id))

@client.event
async def on_message(message):
	if not message.channel.is_private:
		return

	if message.author == client.user:
		return

	try:
		datetime.datetime.strptime(message.content, '%d-%m')
	except ValueError:
		await client.send_message(message.channel, content="Incorrect data format, should be DD-MM")
		return

	date = message.content
	user = message.author.id
	
	search = db.execute('select count(id) from birthdays where id=?', (user,))
	c = 0
	for s in search:
		if s[0] > 0:
			c += 1
			break
	if c:
		db.execute('UPDATE birthdays SET birthday=? where id=?', (date,user))
		await client.send_message(message.channel, content='Birthday changed to {}'.format(date))
		print('Birthday changed to {}'.format(date))
	else:
		db.execute('insert into birthdays values (?, ?)', (date, user))
		await client.send_message(message.channel, content='Birthday successfully added!')
		print('Added row ({}, {})'.format(date, user))
	
	conn.commit()

def asyncio dontcrash():
    channels = client.get_all_channels()
    asyncio.sleep(50)

client.loop.create_task(dontcrash())
client.loop.create_task(check_birthdays())
client.run(str(api_key)) # Send API key from opened file
