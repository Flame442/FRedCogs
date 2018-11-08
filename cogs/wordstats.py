import discord, re
from discord.ext import commands

class WordStats:
	"""Tracks commonly written words"""
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def wordstats(self, message, user: discord.Member=None):
		"""Prints the most commonly written words"""
		wordlist = [] #list of all words
		worddic = {} #count of each word
		if user == None:
			mention = 'the server'
		else:
			mention = user.mention
		'''Make wordlist'''
		with open('data/wordstats/all.txt') as f:
			for line in f:
				lineid, words = line.split('|') 
				words = words.split(' ')
				if user == None or lineid.strip() == user.id:
					for word in words:
						word = word.strip()
						if word:
							wordlist.append(word)
		'''Count/sort wordlist'''
		num = len(wordlist)
		for word in wordlist:
			try:
				worddic[word] += 1
			except:
				worddic[word] = 1
		order = list(reversed(sorted(worddic,key= lambda w: worddic[w])))
		'''Print result & write to file'''
		result = ''
		smallresult = ''
		n = 0
		for word in order:
			if n < 30:
				smallresult +=str(worddic[word])+' '+str(word)+'\n'
				n += 1
			result += str(worddic[word])+' '+str(word)+'\n'
		await self.bot.say('Out of '+str(num)+' words, the 30 most common words that '+mention+' has said are:\n```'+smallresult.rstrip()+'```')
		with open('data/wordstats/result.txt', 'w') as f:
			f.write(result)

	async def run(self, t):
		"""Passively records all message contents"""
		if t.author.id != self.bot.user.id:
			message = t.content.lower()
			'''epic'''
			if message.find('epic') != -1 and message.find('unepic') == -1:
				with open('data/wordstats/epic.txt') as f:
					for line in f:
						num = int(line)
				num += 1
				await self.bot.send_message(t.channel, content='Ok, now THIS is epic #'+str(num))
				with open('data/wordstats/epic.txt','w') as f:
					f.write(str(num))
			'''ok so basically'''
			if message.find('ok so basically') != -1:
				await self.bot.send_message(t.channel, content='I\'m monkey!')
			'''darn'''
			if message.find('darn') != -1:
				await self.bot.send_message(t.channel, content='What a *darn* shame!')
			'''all text'''
			if t.channel.id != '500150094184841247' and t.channel.id != '495722437997232148' and t.channel.id != '389833321682698240' and t.server.id != '499751595500896257':
				with open('data/wordstats/all.txt','a') as f:
					f.write(str(t.author.id)+' | '+str(re.sub(r'[^a-zA-Z ]','',message))+'\n')

def setup(bot):
	n = WordStats(bot)
	bot.add_listener(n.run, "on_message")
	bot.add_cog(n)
