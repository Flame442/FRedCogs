import discord
from discord.ext import commands
from __main__ import send_cmd_help

class battleship:
	"""Play battleship with one other person"""
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True, no_pm=True)
	async def battleship(self, a):
		if a.invoked_subcommand is None:
			await send_cmd_help(a)

	@battleship.command(name="play", pass_context=True)
	async def _play_battleship(self, t):
		"""|Start a game of battleship|"""
		await self.bot.say('Setting up, please wait')
		channel = t.message.channel
		name = [str(t.message.author)[:-5]]
		board = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
		let = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		letnum = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}
		bkey = [{0:'· ',1:'O ',2:'X ',3:'· '},{0:'· ',1:'O ',2:'X ',3:'# '}]
		pswap = {1:0,0:1}
		key = [[],[]]
		key2 = {0:0,1:0,2:0,3:0,4:0}
		namekey = {0:'5',1:'4',2:'3',3:'3',4:'2'}
		pid = [t.message.author]

		def bprint(player,bt):
			b = '  '
			for z in range(10): b += let[z]+' '
			b += '\n'
			for y in range(10):
				b += str(y)+' '
				for x in range(10): b += bkey[bt][board[player][(y*10)+x]]
				b += '\n'
			return '```'+b+'```'

		def place(player,length,value):
			hold = {}
			x = letnum[value[0]]
			y = int(value[1])
			d = value[2]
			if d == 'r':
				if 10 - length < x:
					1 / 0
				for z in range(length):
					if board[player][(y*10)+x+z] != 0:
						1 / 0
				for z in range(length):
					board[player][(y*10)+x+z] = 3
					hold[(y*10)+x+z] = 0
			elif d == 'd':
				for z in range(length):
					if board[player][((y+z)*10)+x] != 0:
						1 / 0
				for z in range(length):
					board[player][((y+z)*10)+x] = 3
					hold[((y+z)*10)+x] = 0
			else:
				1 / 0
			key[player].append(hold)

		#RUN CODE
		check = lambda m: m.author != t.message.author and m.author.bot == False
		await self.bot.say('Second player, say I')
		r = await self.bot.wait_for_message(timeout=60, check=check, channel=channel)
		name.append(str(r.author)[:-5])
		pid.append(r.author)
		await self.bot.say('A game of battleship will be played between '+name[0]+' and '+name[1]+'.')
		bank = self.bot.get_cog('Economy').bank
		while True:
			await self.bot.say('How much to bet '+name[0]+'?')
			while True:
				ans = await self.bot.wait_for_message(timeout=60, author=pid[0], channel=channel)
				try:
					bet = int(ans.content)
				except:
					self.bot.say('Pick a valid number')
				if bank.get_balance(pid[0]) < bet or bank.get_balance(pid[1]) < bet: 
					print('Bet too high')
				else:
					break
			await self.bot.say('Do you accept '+name[1]+'? (y/n)')
			while True:
				ans = await self.bot.wait_for_message(timeout=60, author=pid[1], channel=channel)
				if ans.content == 'y':
					break
				elif ans.content == 'n':
					bet = -1
					break
				else:
					await self.bot.say('Pick a valid input')
			if bet != -1:
				break
		bank.withdraw_credits(pid[0], bet)
		await self.bot.say(name[0]+' now has '+str(bank.get_balance(pid[0]))+' VBucks')
		bank.withdraw_credits(pid[1], bet)
		await self.bot.say(name[1]+' now has '+str(bank.get_balance(pid[1]))+' VBucks')
		for x in range(2):
			await self.bot.say('Messaging '+name[x]+' for setup now.')
			await self.bot.send_message(pid[x],content=str(name[x]+', it is your turn to set up your ships. Place ships by entering the top left cord in xyd format.'))
			for k in [5,4,3,3,2]:
				await self.bot.send_message(pid[x],content=bprint(x,1))
				stupid = await self.bot.send_message(pid[x],content='Place your '+str(k)+' length ship')
				while True:
					try:
						t = await self.bot.wait_for_message(timeout=120, author=pid[x], channel=stupid.channel)
						place(x,k,t.content)
						break
					except:
						await self.bot.send_message(pid[x],content='Invalid input')
		###############################################################
		game = True
		p = 1
		while game == True:
			p = pswap[p]
			await self.bot.say(name[p]+'\'s turn!')
			await self.bot.say(bprint(pswap[p],0))
			await self.bot.say(name[p]+', take your shot')
			i = 0
			while i == 0:
				try:
					s = await self.bot.wait_for_message(timeout=120, author=pid[p], channel=channel)
					x = letnum[s.content[0]]
					y = int(s.content[1])
					if board[pswap[p]][(y*10)+x] == 0:
						board[pswap[p]][(y*10)+x] = 1
						await self.bot.send_message(pid[pswap[p]],content=bprint(pswap[p],1))
						await self.bot.say(bprint(pswap[p],0))
						await self.bot.say('Miss!')
						i = 1
					elif board[pswap[p]][(y*10)+x] in [1,2]:
						await self.bot.say('You already shot there!')
					elif board[pswap[p]][(y*10)+x] == 3:
						board[pswap[p]][(y*10)+x] = 2
						await self.bot.send_message(pid[pswap[p]],content=bprint(pswap[p],1))
						await self.bot.say(bprint(pswap[p],0))
						await self.bot.say('Hit!')
						l = -1
						for a in range(5):
							if ((y*10)+x) in key[pswap[p]][a]:
								key[pswap[p]][a][(y*10)+x] = 1
								l = 0
								for b in key[pswap[p]][a]:
									if key[pswap[p]][a][b] == 0:
										l = 1
										break
								if l == 0:
									await self.bot.say(name[pswap[p]]+'\'s '+namekey[a]+' length ship was destroyed!')
									key2[a] = 1
									l = 0
									for c in key2:
										if key2[c] == 0:
											l = 1
											break
									if l == 0:
										await self.bot.say(name[p]+' wins!')
										bank.deposit_credits(pid[p], bet*2)
										await self.bot.say(name[p]+' now has '+str(bank.get_balance(pid[p]))+' VBucks')
										game = False
						if game == False:
							i = 1
				except: await self.bot.say('Invalid input')

def setup(bot):
	bot.add_cog(battleship(bot))
