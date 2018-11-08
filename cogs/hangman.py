import discord
from discord.ext import commands
from __main__ import send_cmd_help
import os
from random import randint

class Hangman:
	"""Play hangman with the bot"""
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True, no_pm=True)
	async def hangman(self, t):
		"""Play hangman with the bot"""
		if t.invoked_subcommand is None:
			await send_cmd_help(t)
			
	@hangman.command(name="leaderboard", pass_context=True) #    389832888889245697 is server ID
	async def _leaderboard_hangman(self):
		"""Prints the rankings of money in the server"""
		bank = self.bot.get_cog('Economy').bank
		dic = {}
		for mem in self.bot.get_all_members():
			if str(mem.server.id) == "389832888889245697":
				try:
					dic[str(mem)] = int(bank.get_balance(mem))
				except:
					continue
		x = sorted(dic.items(), key=lambda kv: kv[1], reverse=True)
		z = "```"
		for y in x:
			z += y[0][:-5]+": "+str(y[1])+"\n"
		await self.bot.say(z+"```")

	@hangman.command(name="list", pass_context=True)
	async def _list_hangman(self):
		"""List the files avalible to select"""
		y = ""
		for x in os.listdir("data/hangman/"):
			y += x+'\n'
		await self.bot.say("```"+y+"```")

	@hangman.command(name="sellist", pass_context=True)
	async def _sellist_hangman(self, t, response: str):
		try:
			x = open("C:\\biggiecheese\\data\\hangman\\"+response+".txt")
			global wordlist
			wordlist = []
			for line in x:
				wordlist.append(line.strip().lower())
			await self.bot.say("Wordlist changed.")
		except:
			await self.bot.say("Invalid wordlist")
			raise

	@hangman.command(name="play", pass_context=True)
	async def _play_hangman(self, t):
		"""Play hangman with the bot"""
		global wordlist
		global man
		word = wordlist[randint(0,len(wordlist))] #pick and format random word
		guessed = ''
		fails = 0
		end = 0
		starter = t.message
		bank = self.bot.get_cog('Economy').bank
		while end == 0:
			p = ''
			for l in word:
				if l not in 'abcdefghijklmnopqrstuvwxyz': #auto print non letter characters
					p += l+' '
				elif l in guessed: #print already guessed characters
					p += l+' '
				else:
					p += '_ ' 
			p += "    ("
			for l in guessed:
				if l not in word:
					p += l
			p += ")"
			check = lambda m: m.author.bot == False #guesser is a human
			await self.bot.say("```"+man[fails]+"\n"+p+"```Guess:")
			t = await self.bot.wait_for_message(timeout=60, author=starter.author, check=check, channel=starter.channel)
			t = t.content[0].lower()
			if t is None: #timeout
				return await self.bot.say("Canceling selection. You took too long.")
			else:
				if t not in word:
					fails += 1
					if fails == 6: #too many fails
						await self.bot.say('```'+man[6]+'```\nGame Over\nThe word was '+word)
						end = 1
						try:
							bank.withdraw_credits(starter.author, 25)
							await self.bot.say("You now have "+str(bank.get_balance(starter.author))+" VBucks")
						except:
							await self.bot.say("You don't have an account")
				guessed += t
				if word.strip(guessed) == word.strip('abcdefghijklmnopqrstuvwxyz'): #guessed entire word
					await self.bot.say('```'+man[fails]+'```\nYou win!\nThe word was '+word)
					try:
						bank.deposit_credits(starter.author, 100)
						await self.bot.say("You now have "+str(bank.get_balance(starter.author))+" VBucks")
					except:
						await self.bot.say("You don't have an account")
					end = 1

def setup(bot):
	bot.add_cog(Hangman(bot))
	global man #hangman picture
	man = ['\
    ___    \n\
   |   |   \n\
   |   O   \n\
   |       \n\
   |       \n\
   |       \n\
   |       \n\
  ','\
    ___    \n\
   |   |   \n\
   |   O   \n\
   |   |   \n\
   |   |   \n\
   |       \n\
   |       \n\
  ','\
    ___    \n\
   |   |   \n\
   |   O   \n\
   |  \|   \n\
   |   |   \n\
   |       \n\
   |       \n\
  ','\
    ___    \n\
   |   |   \n\
   |   O   \n\
   |  \|/  \n\
   |   |   \n\
   |       \n\
   |       \n\
   ','\
    ___    \n\
   |   |   \n\
   |   O   \n\
   |  \|/  \n\
   |   |   \n\
   |  /    \n\
   |       \n\
   ','\
    ___    \n\
   |   |   \n\
   |   O   \n\
   |  \|/  \n\
   |   |   \n\
   |  / \  \n\
   |       \n\
   ','\
    ___    \n\
   |   |   \n\
   |   X   \n\
   |  \|/  \n\
   |   |   \n\
   |  / \  \n\
   |       \n\
   ']
	x = open("C:\\biggiecheese\\data\\hangman\\easywords.txt") #default wordlist
	global wordlist
	wordlist = []
	for line in x:
		wordlist.append(line.strip().lower())
