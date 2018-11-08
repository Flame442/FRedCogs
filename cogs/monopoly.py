import discord
from discord.ext import commands
from __main__ import send_cmd_help
from random import randint, shuffle
from PIL import Image

class Monopoly:
	"""A fun game of monopoly for 2-8 people"""
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	async def monopoly(self, ctx):
		"""A fun game of monopoly for 2-8 people"""
		try:
			channel = ctx.message.channel
			id = [None, ctx.message.author]
			name = [None, str(ctx.message.author)[:-5]] #name of each player
			await self.bot.say('Welcome to Monopoly. How many players?')
			i = 0
			while i == 0:
				try:
					num = await self.bot.wait_for_message(timeout=60, author=id[1], channel=channel)
					if num.content == 'test':
						num = 2
						numalive = 2
						id.append(ctx.message.author)
						name.append(str(ctx.message.author)[:-5])
						i = 1
						hold = 0
					else: #unindent everything to remove test case
						num = int(num.content)
						if num < 2 or num > 8: #2-8 player game
							await self.bot.say('Please select a number between 2 and 8')
						else:
							global numalive
							numalive = num #set number of players still in the game for later
							i = 1 #leave loop
							hold = 1
				except: #not a number
					await self.bot.say('Please select a number between 2 and 8')
			if hold == 1: #unindent everything to remove test case
				for a in range(2,num+1):
					check = lambda m: m.author not in id and m.author.bot == False
					await self.bot.say('Player '+str(a)+', say I')
					r = await self.bot.wait_for_message(timeout=60, check=check, channel=channel)
					name.append(str(r.author)[:-5])
					id.append(r.author)

			async def configdict(filename): #convert content of config-file into dictionary.
				with open(filename, "r") as f:
					cfglines = f.readlines()
				global cfgdict
				cfgdict = {}
				for line in cfglines:
					line = line.strip()
					if not line or line.startswith("#"):
						continue
					try:
						key, value = line.split("=") #split to variable and value
					except ValueError:
						await self.bot.say("Bad line in config-file "+filename+':\n'+line)
						continue
					key, value = key.strip(), value.strip()
					if value in ["True", "False", "None", "''", '""']:
						value = eval(value) #turn to bool
					else:
						try:
							if "." in value:
								value = float(value) #turn to float
							else:
								value = int(value) #turn to int
						except ValueError:
							pass #value need not be converted
					cfgdict[key] = value #put in dictionary
				return cfgdict
			try:
				await configdict('data/monopoly/save.txt') 
				await self.bot.say('Use save file? (y/n)')
				useSave = await self.bot.wait_for_message(timeout=60, author=id[1], channel=channel)
				if useSave.content != 'y':
					raise TypeError('Don\'t Save')
				global injail,tile,bal,p,ownedby,numhouse,ismortgaged,goojf,alive,jailturn
				name = cfgdict['name']
				tilename = cfgdict['tilename']
				bal = cfgdict['bal']
				p = cfgdict['p']
				ownedby = cfgdict['ownedby']
				numhouse = cfgdict['numhouse']
				ismortgaged = cfgdict['ismortgaged']
				goojf = cfgdict['goojf']
				alive = cfgdict['alive']
				jailturn = cfgdict['jailturn']
			except: #default start
				global injail,tile,bal,p,ownedby,numhouse,ismortgaged,goojf,alive,jailturn
				injail = [-1, False, False, False, False, False, False, False, False]
				tile = [-1, 0, 0, 0, 0, 0, 0, 0, 0]
				bal = [-1, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
				p = 0
				ownedby = [-1, 0, -1, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, -1, 0]
				numhouse = [-1, 0, -1, 0, -1, -1, 0, -1, 0, 0, -1, 0, -1, 0, 0, -1, 0, -1, 0, 0, -1, 0, -1, 0, 0, -1, 0, 0, -1, 0, -1, 0, 0, -1, 0, -1, -1, 0, -1, 0]
				ismortgaged = [-1, 0, -1, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, -1, 0]
				goojf = [-1, 0, 0, 0, 0, 0, 0, 0, 0]
				alive = [-1, True, True, True, True, True, True, True, True]
				jailturn = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
				try:
					cfgdict = await configdict('data/monopoly/settings.txt')
					if cfgdict['propName'] == 1: #british
						tilename = ['Go', 'Old Kent Road', 'Community Chest', 'Whitechapel Road', 'Income Tax', 'King\'s Cross Staton', 'The Angel Islington', 'Chance', 'Euston Road', 'Pentonville Road', 'Jail', 'Pall Mall', 'Electric Company', 'Whitehall', 'Northumrl\'d Avenue', 'Marylebone Station', 'Bow Street', 'Community Chest', 'Marlborough Street', 'Vine Street', 'Free Parking', 'Strand', 'Chance', 'Fleet Street', 'Trafalgar Square', 'Fenchurch Station', 'Leicester Square', 'Conventry Street', 'Water Works', 'Piccadilly', 'Go To Jail', 'Regent Street', 'Oxford Street', 'Community Chest', 'Bond Street', 'Liverpool St. Station', 'Chance', 'Park Lane', 'Super Tax', 'Mayfair']
					elif cfgdict['propName'] == 2: #american
						tilename = ['Go', 'Mediterranean Avenue', 'Community Chest', 'Baltic Avenue', 'Income Tax', 'Reading Rainbow', 'Oriental Avenue', 'Chance', 'Vermont Avenue', 'Connecticut Avenue', 'Jail', 'St. Charles Place', 'Electric Company', 'States Avenue', 'Virginia Avenue', 'Pennsylvania Railroad', 'St. James Place', 'Community Chest', 'Tennessee Avenue', 'New York Avenue', 'Free Parking', 'Kentucky Avenue', 'Chance', 'Indiana Avenue', 'Illinois Avenue', 'B&O Railroad', 'Atlantic Avenue', 'Ventnor Avenue', 'Water Works', 'Marvin Gardens', 'Go To Jail', 'Pacific Avenue', 'North Carolina Avenue', 'Community Chest', 'Pennsylvania Avenue', 'Short Line', 'Chance', 'Park Place', 'Luxury Tax', 'Boardwalk']
					elif cfgdict['propName'] == 3: #custom
						tilename = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
						for x in range(40):
							tilename[x] = cfgdict[str(x)]
				except:
					with open('data/monopoly/settings.txt', 'w') as f:
						f.write('#Settings for Monopoly by Flame442\n\n#What property names to use (default 2)\n#1 = British\n#2 = US\n#3 = Custom\n\npropName = 2\n\n#If propName is set to Custom, these names will be used (default British names)\n#0-39 for every property in order starting at go\n\n 0 = Go\n 1 = Old Kent Road\n 2 = Community Chest\n 3 = Whitechapel Road\n 4 = Income Tax\n 5 = King\'s Cross Station\n 6 = The Angel Islington\n 7 = Chance\n 8 = Euston Road\n 9 = Pentonville Road\n10 = Jail\n11 = Pall Mall\n12 = Electric Company\n13 = Whitehall\n14 = Northumrl\'d Avenue\n15 = Marylebone Station\n16 = Bow Street\n17 = Community Chest\n18 = Marlborough Street\n19 = Vine Street\n20 = Free Parking\n21 = Strand\n22 = Chance\n23 = Fleet Street\n24 = Trafalgar Square\n25 = Fenchurch Station\n26 = Leicester Square\n27 = Conventry Street\n28 = Water Works\n29 = Piccadilly\n30 = Go To Jail\n31 = Regent Street\n32 = Oxford Street\n33 = Community Chest\n34 = Bond Street\n35 = Liverpool St. Station\n36 = Chance\n37 = Park Lane\n38 = Super Tax\n39 = Mayfair')
					await self.bot.say("No config file read, so one was created")
					await configdict('data/monopoly/settings.txt')
					tilename = ['Go', 'Mediterranean Avenue', 'Community Chest', 'Baltic Avenue', 'Income Tax', 'Reading Rainbow', 'Oriental Avenue', 'Chance', 'Vermont Avenue', 'Connecticut Avenue', 'Jail', 'St. Charles Place', 'Electric Company', 'States Avenue', 'States Avenue', 'Pennsylvania Railroad', 'St. James Place', 'Community Chest', 'Tennessee Avenue', 'New York Avenue', 'Free Parking', 'Kentucky Avenue', 'Chance', 'Indiana Avenue', 'Illinois Avenue', 'B&O Railroad', 'Atlantic Avenue', 'Ventnor Avenue', 'Water Works', 'Marvin Gardens', 'Go To Jail', 'Pacific Avenue', 'North Carolina Avenue', 'Community Chest', 'Pennsylvania Avenue', 'Short Line', 'Chance', 'Park Place', 'Luxury Tax', 'Boardwalk']
			pricebuy = [-1, 60, -1, 60, -1, 200, 100, -1, 100, 120, -1, 140, 150, 140, 160, 200, 180, -1, 180, 200, -1, 220, -1, 220, 240, 200, 260, 260, 150, 280, -1, 300, 300, -1, 320, 200, -1, 350, -1, 400]
			rentprice = [-1, -1, -1, -1, -1, -1, 2, 10, 30, 90, 160, 250, -1, -1, -1, -1, -1, -1, 4, 20, 60, 180, 360, 450, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, 30, 90, 270, 400, 550, -1, -1, -1, -1, -1, -1, 6, 30, 90, 270, 400, 550, 8, 40, 100, 300, 450, 600, -1, -1, -1, -1, -1, -1, 10, 50, 150, 450, 625, 750, -1, -1, -1, -1, -1, -1, 10, 50, 150, 450, 625, 750, 12, 60, 180, 500, 700, 900, -1, -1, -1, -1, -1, -1, 14, 70, 200, 550, 750, 950, -1, -1, -1, -1, -1, -1, 14, 70, 200, 550, 750, 950, 16, 80, 220, 600, 800, 1000, -1, -1, -1, -1, -1, -1, 18, 90, 250, 700, 875, 1050, -1, -1, -1, -1, -1, -1, 10, 90, 250, 700, 875, 1050, 20, 100, 300, 750, 925, 1100, -1, -1, -1, -1, -1, -1, 22, 110, 330, 800, 975, 1150, 22, 110, 330, 800, 975, 1150, -1, -1, -1, -1, -1, -1, 22, 120, 360, 850, 1025, 1200, -1, -1, -1, -1, -1, -1, 26, 130, 390, 900, 1100, 1275, 26, 130, 390, 900, 1100, 1275, -1, -1, -1, -1, -1, -1, 28, 150, 450, 1000, 1200, 1400, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 35, 175, 500, 1100, 1300, 1500, -1, -1, -1, -1, -1, -1, 50, 200, 600, 1400, 1700, 2000]
			rrprice = [0, 25, 50, 100, 200]
			global ccorder, chanceorder, ccn, chancen
			ccorder = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
			shuffle(ccorder)
			ccn = 0
			chanceorder = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
			shuffle(chanceorder)
			chancen = 0
			ccname = ['Advance to Go (Collect $200)', 'Bank error in your favor\nCollect $200', 'Doctor\'s fee\nPay $50', 'From sale of stock you get $50', 'Get Out of Jail Free', 'Go to Jail\nGo directly to jail\nDo not pass Go\nDo not collect $200', 'Grand Opera Night\nCollect $50 from every player for opening night seats', 'Holiday Fund matures\nReceive $100', 'Income tax refund\nCollect $20', 'It is your birthday\nCollect $10', 'Life insurance matures\nCollect $100', 'Pay hospital fees of $100', 'Pay school fees of $150', 'Receive $25 consultancy fee', 'You are assessed for street repairs\n$40 per house\n$115 per hotel', 'You have won second prize in a beauty contest\nCollect $10', 'You inherit $100']
			chancename = ['Advance to Go (Collect $200)', 'Advance to Illinois Ave\nIf you pass Go, collect $200.', 'Advance to St. Charles Place\nIf you pass Go, collect $200', 'Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total ten times the amount thrown.', 'Advance token to the nearest Railroad and pay owner twice the rental to which he/she is otherwise entitled. If Railroad is unowned, you may buy it from the Bank.', 'Bank pays you dividend of $50', 'Get Out of Jail Free', 'Go Back 3 Spaces', 'Go to Jail\nGo directly to Jail\nDo not pass Go\nDo not collect $200', 'Make general repairs on all your property\nFor each house pay $25\nFor each hotel $100', 'Pay poor tax of $15', 'Take a trip to Reading Railroad\nIf you pass Go, collect $200', 'Take a walk on the Boardwalk\nAdvance token to Boardwalk', 'You have been elected Chairman of the Board\nPay each player $50', 'Your building and loan matures\nCollect $150', 'You have won a crossword competition\nCollect $100']
			mortgageprice = [-1, 50, -1, 50, -1, 100, 50, -1, 50, 60, -1, 70, 75, 70, 80, 100, 90, -1, 90, 100, -1, 110, -1, 110, 120, 100, 140, 140, 75, 150, -1, 200, 200, -1, 200, 100, -1, 175, -1, 200]
			tenmortgageprice = [-1, 55, -1, 55, -1, 110, 55, -1, 55, 66, -1, 77, 83, 77, 88, 110, 99, -1, 99, 110, -1, 121, -1, 121, 132, 110, 154, 154, 83, 165, -1, 220, 220, -1, 220, 110, -1, 188, -1, 220]
			houseprice = [-1, 30, -1, 30, -1, -1, 50, -1, 50, 50, -1, 100, -1, 100, 100, -1, 100, -1, 100, 100, -1, 150, -1, 150, 150, -1, 150, 150, -1, 150, -1, 150, 150, -1, 150, -1, -1, 200, -1, 200]
			global autosave
			autosave = ''

			async def bprint():
				def fill(i,color,x1,y1,x2,y2):
					for x in range(x1,x2):
						for y in range(y1,y2):
							i.putpixel( (x, y), color )
					return i
				pcolor = [-1, (0,0,255,255), (255,0,0,255), (0,255,0,255), (255,255,0,255), (0,255,255,255), (255,140,0,255), (140,0,255,255), (255,0,255,255)]
				img = Image.open('data/monopoly/img.png')
				#OWNEDBY
				for t in range(40):
					if ownedby[t] > 0:
						if 0 < t < 10:
							img = fill(img,(0,0,0,255),(650-(t*50))-39,702,(650-(t*50))-10,735)
							img = fill(img,pcolor[ownedby[t]],(650-(t*50))-37,702,(650-(t*50))-12,733)
						elif 10 < t < 20:
							img = fill(img,(0,0,0,255),16,(650-((t-10)*50))-39,50,(650-((t-10)*50))-10)
							img = fill(img,pcolor[ownedby[t]],18,(650-((t-10)*50))-37,50,(650-((t-10)*50))-12)
						elif 20 < t < 30:
							img = fill(img,(0,0,0,255),(100+((t-20)*50))+11,16,(100+((t-20)*50))+41,50)
							img = fill(img,pcolor[ownedby[t]],(100+((t-20)*50))+13,18,(100+((t-20)*50))+39,50)
						elif 30 < t < 40:
							img = fill(img,(0,0,0,255),702,(100+((t-30)*50))+11,736,(100+((t-30)*50))+41)
							img = fill(img,pcolor[ownedby[t]],702,(100+((t-30)*50))+13,734,(100+((t-30)*50))+39)
				#TILE
				for t in range(1,num+1):
					if tile[t] == 0:
						img = fill(img,(0,0,0,255),(12*(t-1))+604,636,(12*(t-1))+614,646)
						img = fill(img,pcolor[t],(12*(t-1))+605,637,(12*(t-1))+613,645)
					elif 0 < tile[t] < 10:
						if t < 5:
							img = fill(img,(0,0,0,255),((650-(tile[t]*50))-47)+(12*(t-1)),636,((650-(tile[t]*50))-37)+(12*(t-1)),646)
							img = fill(img,pcolor[t],((650-(tile[t]*50))-46)+(12*(t-1)),637,((650-(tile[t]*50))-38)+(12*(t-1)),645)
						else:
							img = fill(img,(0,0,0,255),((650-(tile[t]*50))-47)+(12*(t-5)),648,((650-(tile[t]*50))-37)+(12*(t-5)),658)
							img = fill(img,pcolor[t],((650-(tile[t]*50))-46)+(12*(t-5)),649,((650-(tile[t]*50))-38)+(12*(t-5)),657)
					elif tile[t] == 10:
						img = fill(img,(0,0,0,255),106,(12*(t-1))+604,116,(12*(t-1))+614)
						img = fill(img,pcolor[t],107,(12*(t-1))+605,115,(12*(t-1))+613)
					elif 10 < tile[t] < 20:
						if t < 5:
							img = fill(img,(0,0,0,255),106,((650-((tile[t]-10)*50))-47)+(12*(t-1)),116,((650-((tile[t]-10)*50))-37)+(12*(t-1)))
							img = fill(img,pcolor[t],107,((650-((tile[t]-10)*50))-46)+(12*(t-1)),115,((650-((tile[t]-10)*50))-38)+(12*(t-1)))
						else:
							img = fill(img,(0,0,0,255),94,((650-((tile[t]-10)*50))-47)+(12*(t-5)),104,((650-((tile[t]-10)*50))-37)+(12*(t-5)))
							img = fill(img,pcolor[t],95,((650-((tile[t]-10)*50))-46)+(12*(t-5)),103,((650-((tile[t]-10)*50))-38)+(12*(t-5)))
					elif tile[t] == 20:
						img = fill(img,(0,0,0,255),138-(12*(t-1)),106,148-(12*(t-1)),116)
						img = fill(img,pcolor[t],139-(12*(t-1)),107,147-(12*(t-1)),115)
					elif 20 < tile[t] < 30:
						if t < 5:
							img = fill(img,(0,0,0,255),((100+((tile[t]-20)*50))+39)-(12*(t-1)),106,((100+((tile[t]-20)*50))+49)-(12*(t-1)),116)
							img = fill(img,pcolor[t],((100+((tile[t]-20)*50))+40)-(12*(t-1)),107,((100+((tile[t]-20)*50))+48)-(12*(t-1)),115)
						else:
							img = fill(img,(0,0,0,255),((100+((tile[t]-20)*50))+39)-(12*(t-5)),94,((100+((tile[t]-20)*50))+49)-(12*(t-5)),104)
							img = fill(img,pcolor[t],((100+((tile[t]-20)*50))+40)-(12*(t-5)),95,((100+((tile[t]-20)*50))+48)-(12*(t-5)),103)
					elif tile[t] == 30:
						img = fill(img,(0,0,0,255),636,138-(12*(t-1)),646,148-(12*(t-1)))
						img = fill(img,pcolor[t],637,139-(12*(t-1)),645,147-(12*(t-1)))
					elif 30 < tile[t] < 40:
						if t < 5:
							img = fill(img,(0,0,0,255),636,((100+((tile[t]-30)*50))+39)-(12*(t-1)),646,((100+((tile[t]-30)*50))+49)-(12*(t-1)))
							img = fill(img,pcolor[t],637,((100+((tile[t]-30)*50))+40)-(12*(t-1)),645,((100+((tile[t]-30)*50))+48)-(12*(t-1)))
						else:
							img = fill(img,(0,0,0,255),648,((100+((tile[t]-30)*50))+39)-(12*(t-5)),658,((100+((tile[t]-30)*50))+49)-(12*(t-5)))
							img = fill(img,pcolor[t],649,((100+((tile[t]-30)*50))+40)-(12*(t-5)),657,((100+((tile[t]-30)*50))+48)-(12*(t-5)))
				#NUMHOUSE
				for t in range(40):
					if numhouse[t] == 5:
						if 0 < t < 10:
							img = fill(img,(0,0,0,255),(650-(t*50))-33,606,(650-(t*50))-15,614)
							img = fill(img,(255,0,0,255),(650-(t*50))-32,607,(650-(t*50))-16,613)
						elif 10 < t < 20:			
							img = fill(img,(0,0,0,255),138,(650-((t-10)*50))-33,146,(650-((t-10)*50))-17)
							img = fill(img,(255,0,0,255),139,(650-((t-10)*50))-32,145,(650-((t-10)*50))-18)
						elif 20 < t < 30:
							img = fill(img,(0,0,0,255),(100+((t-20)*50))+17,138,(100+((t-20)*50))+35,146)
							img = fill(img,(255,0,0,255),(100+((t-20)*50))+18,139,(100+((t-20)*50))+34,145)
						elif 30 < t < 40:
							img = fill(img,(0,0,0,255),606,(100+((t-30)*50))+17,614,(100+((t-30)*50))+35)
							img = fill(img,(255,0,0,255),607,(100+((t-30)*50))+18,613,(100+((t-30)*50))+34)
					elif numhouse[t] > 0:
						for tt in range(numhouse[t]):
							if 0 < t < 10:
								img = fill(img,(0,0,0,255),((650-(t*50))-47)+(tt*12),606,((650-(t*50))-37)+(tt*12),614)
								img = fill(img,(0,255,0,255),((650-(t*50))-46)+(tt*12),607,((650-(t*50))-38)+(tt*12),613)
							elif 10 < t < 20:
								img = fill(img,(0,0,0,255),138,((650-((t-10)*50))-47)+(tt*12),146,((650-((t-10)*50))-37)+(tt*12))
								img = fill(img,(0,255,0,255),139,((650-((t-10)*50))-46)+(tt*12),145,((650-((t-10)*50))-38)+(tt*12))
							elif 20 < t < 30:
								img = fill(img,(0,0,0,255),((100+((t-20)*50))+39)-(tt*12),138,((100+((t-20)*50))+49)-(tt*12),146)
								img = fill(img,(0,255,0,255),((100+((t-20)*50))+40)-(tt*12),139,((100+((t-20)*50))+48)-(tt*12),145)
							elif 30 < t < 40:
								img = fill(img,(0,0,0,255),606,((100+((t-30)*50))+39)-(tt*12),614,((100+((t-30)*50))+49)-(tt*12))
								img = fill(img,(0,255,0,255),607,((100+((t-30)*50))+40)-(tt*12),613,((100+((t-30)*50))+48)-(tt*12))
				#END
				img.save('data/monopoly/temp.png')
				await self.bot.send_file(channel, 'data/monopoly/temp.png')

			def monopolytest(t,test): #tests if prop in monopoly or any properties in color group has houses
				pga = [1, 6, 11, 16, 21, 26, 31, 37]
				pgb = [3, 8, 13, 18, 23, 27, 32, 39] #3 properties in each color
				pgc = [3, 9, 14, 19, 24, 29, 34, 39]
				if test == 'm':
					for i in range(8):
						if bool(bool(t == pga[i] or t == pgb[i] or t == pgc[i]) and bool(ownedby[pga[i]] == ownedby[pgb[i]] == ownedby[pgc[i]]) and bool(ownedby[pga[i]] != 0)): #if the tested property is one of the 3 currently selected, all three are owned by the same person and not unowned, return True
							return True
					return False
				elif test == 'h':
					for i in range(8):
						if bool(bool(t == pga[i] or t == pgb[i] or t == pgc[i]) and bool(bool(numhouse[pga[i]] != 0) or bool(numhouse[pgb[i]] != 0) or bool(numhouse[pgc[i]]) != 0) and bool(ownedby[pga[i]] != 0)): #if at least one of the properties in the color group has houses, return True
							return True
					return False
				return False

			async def trade(): #trades between players, messy don't even try to read...
				await self.bot.say('Select the player you want to trade with')
				a,monp,monn,jp,jn = 1,0,0,0,0
				tradeidp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				tradeidn = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				ptotrade = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				ntotrade = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				hold = ''
				while a < 9:
					if a <= num:
						if a == p or not alive[a]: #can't trade with yourself or dead players
							a += 1
							continue
						else:
							hold += str(a)+' '+name[a]+'\n' #print name if tradeable
							a += 1
							continue
					else:
						break
				await self.bot.say('```'+hold.strip()+'```')
				i = 0
				while i != 1:
					try:
						tradep = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel) #select the number of the player to trade
						tradep = int(tradep.content)
						if 1 <= tradep <= num and tradep != p and alive[tradep] == True: #make sure the number is a player, is not the person starting the trade, and is alive
							i = 1
						else:
							await self.bot.say('Select one of the options')
							continue
					except:
						await self.bot.say('Select one of the options')
				a,pti = 0,1
				while a < 40:
					if ownedby[a] == p and bool(numhouse[a] == 0 or numhouse[a] == -1): #can only trade if owned by the player and does not have a house
						tradeidp[pti] = a #put in the holding cell
						pti += 1
					a += 1
				while i == 1:
					hold = 'id sel name\n'
					a = 1
					while a < pti:
						if ptotrade[tradeidp[a]] == 1: #if already selected
							hold += str(a)+'  +   '+tilename[tradeidp[a]]+'\n'
						else:
							hold += str(a)+'      '+tilename[tradeidp[a]]+'\n'
						a += 1
					hold += '$'+str(monp)+'\n' #money trade
					if jp == 1: #plural test
						hold += str(jp)+' get out of jail free card'
					elif jp != 0:
						hold += str(jp)+' get out of jail free cards'
					await self.bot.say('```'+hold.strip()+'```\nType the number of the properties you want to give, "m" to give money, "j" to give get out of jail free cards, and "d" when you are done')
					t = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
					t = t.content
					try: #swap select/deselect property if valid number
						if 0 < int(t) < pti and ptotrade[tradeidp[int(t)]] == 0:
							ptotrade[tradeidp[int(t)]] = 1
							continue
						elif 0 < int(t) < pti and ptotrade[tradeidp[int(t)]] == 1:
							ptotrade[tradeidp[int(t)]] = 0
							continue
						else:
							pass
					except ValueError: #not a number
						if t == 'm': #money select screen
							try:
								await self.bot.say('How much money? You have $'+str(bal[p]))
								monp = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
								monp = int(monp.content)
								if monp > bal[p]: #can't be greater than owned money
									monp = 0
								continue
							except:
								monp = 0
						elif t == 'd': #exit loop
							i = 2
							continue
						elif t == 'j':
							try:
								await self.bot.say('How many? You have '+str(goojf[p]))
								jp = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
								jp = int(jp.content)
								if jp > goojf[p]: #can't be greater than owned goojf
									jp = 0
								continue
							except:
								jp = 0
						else:
							continue
				a,nti = 0,1 #EVERYTHIN ABOVE REPEATED FOR SELECTING PROPERTIES FROM TRADEP(artner)
				while a < 40:
					if ownedby[a] == tradep and bool(numhouse[a] == 0 or numhouse[a] == -1):
						tradeidn[nti] = a
						nti += 1
					a += 1
				while i == 2:
					hold = 'id sel name\n'
					a = 1
					while a < nti:
						if ntotrade[tradeidn[a]] == 1:
							hold += str(a)+'  +   '+tilename[tradeidn[a]]+'\n'
						else:
							hold += str(a)+'      '+tilename[tradeidn[a]]+'\n'
						a += 1
					hold += '$'+str(monn)+'\n'
					if jn == 1:
						hold += str(jn)+' get out of jail free card'
					elif jn != 0:
						hold == str(jn)+' get out of jail free cards'
					await self.bot.say('```'+hold.strip()+'```\nType the number of the properties you want to take, "m" to take money, "j" to take get out of jail free cards, and "d" when you are done')
					t = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
					t = t.content
					try:
						if 0 < int(t) < nti and ntotrade[tradeidn[int(t)]] == 0:
							ntotrade[tradeidn[int(t)]] = 1
							continue
						elif 0 < int(t) < nti and ntotrade[tradeidn[int(t)]] == 1:
							ntotrade[tradeidn[int(t)]] = 0
							continue
						else:
							pass
					except ValueError:
						if t == 'm':
							try:
								await self.bot.say('How much money? You have $'+str(bal[tradep]))
								monn = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
								monn = int(monn.content)
								if monn > bal[tradep]:
									monn = 0
								continue
							except:
								monn = 0
						elif t == 'd':
							i = 3
							continue
						elif t == 'm':
							try:
								await self.bot.say('How many? You have '+str(goojf[tradep]))
								jn = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
								jn = int(jn.content)
								if jn > goojf[tradep]:
									jn = 0
								continue
							except:
								jn = 0
						else:
							continue
				await self.bot.say('Confirm with y or quit with n\n\nYou will give:')
				a = 1
				hold = ''
				while a < pti:
					if ptotrade[tradeidp[a]] == 1: #print selected properties
						hold += tilename[tradeidp[a]]+'\n'
					a += 1
				hold += '$'+str(monp)+'\n'
				if jp == 1:
					hold += str(jp)+' get out of jail free card'
				elif jp != 0:
					hold += str(jp)+' get out of jail free cards'
				await self.bot.say('```'+hold.strip()+'```\nYou will get:')
				hold = ''
				a = 1
				while a < nti:
					if ntotrade[tradeidn[a]] == 1:
						hold += tilename[tradeidn[a]]+'\n'
					a += 1
				hold += '$'+str(monn)+'\n'
				if jn == 1:
					hold += str(jn)+' get out of jail free card'
				elif jn != 0:
					hold += str(jn)+' get out of jail free cards'
				await self.bot.say('```'+hold.strip()+'```')
				while i == 3:
					a = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
					a = a.content 
					if str(a) == 'y':
						i = 4 
					elif str(a) == 'n':
						i = 10
					else:
						await self.bot.say('Select y or n')
				if i == 4:
					await self.bot.say(name[tradep]+',\n'+name[p]+' would like to trade with you. Here is their offer.\nAccept with y or deny with n.\n\nYou will get:')
					a = 1
					hold = ''
					while a < pti:
						if ptotrade[tradeidp[a]] == 1:
							hold += tilename[tradeidp[a]]+'\n'
						a += 1
					hold += '$'+str(monp)+'\n'
					if jp == 1:
						hold += str(jp)+' get out of jail free card'
					elif jp != 0:
						hold += str(jp)+' get out of jail free cards'
					await self.bot.say('```'+hold.strip()+'```\nYou will give:')
					a = 1
					hold = ''
					while a < nti:
						if ntotrade[tradeidn[a]] == 1:
							hold += tilename[tradeidn[a]]+'\n'
						a += 1
					hold += '$'+str(monn)+'\n'
					if jn == 1:
						hold += str(jn)+' get out of jail free card'
					elif jn != 1:
						hold += str(jn)+' get out of jail free cards'
					await self.bot.say('```'+hold.strip()+'```')
					while i == 4:
						a = await self.bot.wait_for_message(timeout=60, author=id[tradep], channel=channel)
						a = a.content
						if str(a) == 'y':
							i = 5
						elif str(a) == 'n':
							i = 10
						else:
							await self.bot.say('Select y or n')
				if i == 5:
					bal[p] += monn
					bal[tradep] += monp
					bal[p] -= monp
					bal[tradep] -= monn
					goojf[p] += jn
					goojf[tradep] += jp
					goojf[p] -= jp
					goojf[tradep] -= jn
					a = 0
					while a < pti: 
						if ptotrade[tradeidp[a]] == 1: #swap selected properties
							ownedby[tradeidp[a]] = tradep
						a += 1
					a = 0
					while a < nti:
						if ntotrade[tradeidn[a]] == 1:
							ownedby[tradeidn[a]] = p
						a += 1
					await bprint()
				await self.bot.say('Back to '+name[p]+'\'s turn')
				
			async def roll(): #rolls d1 and d2 (1-6) and prints if 'doubles'
				global d1
				global d2
				d1 = randint(1,6)
				d2 = randint(1,6)
				if d1 == d2:
					await self.bot.say(name[p]+' rolled a '+str(d1)+' and a '+str(d2)+', Doubles!')
				else:
					await self.bot.say(name[p]+' rolled a '+str(d1)+' and a '+str(d2))

			async def jail(): #turn code when in jail
				global wd, d1, d2
				await self.bot.say(name[p]+' is in jail!')
				if jailturn[p] == -1: #just entered jail
					jailturn[p] = 0
				jailturn[p] += 1
				if goojf[p] > 0:
					if jailturn[p] == 4:
						await self.bot.say('Your 3 turns in jail are up. Type b to post bail, or g to use your "Get Out of Jail Free" card.')
					else:
						await self.bot.say('Type r to roll, b to post bail, or g to use your "Get Out of Jail Free" card.')
				else:
					if jailturn[p] == 4:
						await self.bot.say('Your 3 turns in jail are up. You have to post bail.')
					else:
						await self.bot.say('Type r to roll or b to post bail.')
				jr = 0
				while jr == 0:
					if jailturn[p] == 4 and goojf[p] == 0:
						choice = 'b'
					else:
						choice = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
						choice = choice.content
					if choice == 'r' and not jailturn[p] == 4:
						await roll()
						if d1 == d2:
							wd = 1
							await self.bot.say('You rolled out of jail.')
							jailturn[p] = -1
							injail[p] = False
							await land()
							jr = 1
						else:
							await self.bot.say('Sorry, not doubles')
							jr = 1
					elif choice == 'r' and jailturn[p] == 4:
						await self.bot.say('Select one of the options.')
					elif choice == 'b' and bal[p] >= 50:
						bal[p] -= 50
						await self.bot.say('You posted bail. You now have $'+str(bal[p]))
						jailturn[p] = -1
						injail[p] = False
						await roll()
						if d1 == d2:
							wd = 1
						await land()
						jr = 1
					elif choice == 'b' and bal[p] < 50:
						i = 0
						if jailturn[p] == 4:
							i = 1
						while i == 0:
							await self.bot.say('Doing that will put you into debt. Are you sure you want to do that (y/n)?')
							ask = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
							ask = ask.content
							if ask == 'y':
								i = 1
							if ask == 'n':
								i = 2
						while i == 1:
							bal[p] -= 50
							await self.bot.say('You posted bail. You now have $'+str(bal[p]))
							jailturn[p] = -1
							injail[p] = False
							await debt()
							if alive[p]:
								await roll()
								if d1 == d2:
									wd = 1
								await land()
							i = 2
							jr = 1
					elif choice == 'g' and goojf[p] > 0:
						goojf[p] -= 1
						await self.bot.say('You used your get out of jail free card.')
						jailturn[p] = -1
						injail[p] = False
						await roll()
						if d1 == d2:
							wd = 1
						await land()
						jr = 1
					else:
						await self.bot.say('Select one of the options.')

			async def debt(): #player balance below 0 turn code
				while bal[p] < 0 and alive[p]:
					await self.bot.say('You are in debt. You have $'+str(bal[p])+'.\nSelect an option to get out of debt:\nt: Trade\nm: Mortgage\nh: Sell Houses\ng: Give up')
					choice = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
					choice = choice.content
					if choice == 't':
						await trade()
					elif choice == 'm':
						await mortgage()
					elif choice == 'h':
						await house()
					elif choice == 'g':
						a = 0
						while a == 0:
							await self.bot.say('Are you sure? (y/n)')
							choice = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
							choice = choice.content
							if choice == 'y':
								a = 1
								for i in range(40):
									if ownedby[i] == p:
										ownedby[i] = 0
										numhouse[i] = 0
										ismortgaged[i] = 0
										global numalive
										numalive -= 1
								alive[p] = False
								await self.bot.say(name[p]+' is now out of the game.')
							elif choice == 'n':
								a = 1
							else:
								await self.bot.say('Select one of the options')
					else:
						await self.bot.say('Select one of the options')
				if alive[p]:
					await self.bot.say('You are now out of debt. You now have $'+str(bal[p]))

			async def mortgage(): #mortgage properties 
				mid = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				mi = 1
				for a in range(40):
					if ownedby[a] == p and numhouse[a] <= 0:
						mid[mi] = a
						mi += 1
				i = 0
				while i == 0:
					a = 1
					await self.bot.say('Select the property you want to mortgage')
					hold = 'id isM price name\n'
					while a < mi:
						if monopolytest(a,'h') == False: #cannot morgage a property in a color group with houses because houses can only be built on full monopolies
							if ismortgaged[mid[a]] == 1:
								hold += '{:2}   + {:5d} {}'.format(a,mortgageprice[mid[a]],tilename[mid[a]])+'\n'
							else:
								hold += '{:2}     {:5d} {}'.format(a,mortgageprice[mid[a]],tilename[mid[a]])+'\n'
						a += 1
					await self.bot.say('```'+hold.strip()+'```')
					t = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
					t = t.content
					try:
						t = int(t)
						if 0 < t < mi:
							if ismortgaged[mid[t]] == 0:
								await self.bot.say('Mortgage '+tilename[mid[t]]+' for $'+str(mortgageprice[mid[t]])+'? (y/n) You have $'+str(bal[p]))
								a = 0
								while a == 0:
									responce = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
									responce = responce.content
									if responce == 'y':
										bal[p] += mortgageprice[mid[t]]
										ismortgaged[mid[t]] = 1
										await self.bot.say('You now have $'+str(bal[p]))
										a = 1
									elif responce == 'n':
										a = 1
									else:
										await self.bot.say('Select y or n')
							else:
								if bal[p] >= tenmortgageprice[mid[t]]:
									await self.bot.say('Unmortgage '+tilename[mid[t]]+' for $'+str(tenmortgageprice[mid[t]])+'? (y/n) You have $'+str(bal[p])+'. ($'+str(mortgageprice[mid[t]])+' + 10% interest)')
									a = 0
									while a == 0:
										responce = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
										responce = responce.content
										if responce == 'y':
											ismortgaged[mid[t]] = 0
											bal[p] -= tenmortgageprice[mid[t]]
											await self.bot.say('You now have $'+str(bal[p]))
											a = 1
										elif responce == 'n':
											a = 1
										else:
											await self.bot.say('Select y or n')
								else:
									await self.bot.say('You cannot afford the $'+str(tenmortgageprice[mid[t]])+' it would take to unmortgage that. You only have $'+str(bal[p]))
						else:
							await self.bot.say('Select one of the options')
					except ValueError:
						if t == 'd':
							i = 1
						else:
							await self.bot.say('Select one of the options')

			async def house(): #buy/sell houses
				io = 0
				while io == 0:
					doprint = False
					hid = [0, 0, 0, 0, 0, 0, 0, 0, 0]
					hs = [1, 6, 11, 16, 21, 26, 31, 37]
					color = {1:'Brown',6:'Light Blue',11:'Pink',16:'Orange',21:'Red',26:'Yellow',31:'Green',37:'Dark Blue'}
					hdic = {1:[1,3],6:[6,8,9],11:[11,13,14],16:[16,18,19],21:[21,23,24],26:[26,27,29],31:[31,32,34],37:[37,39]}
					hi = 1
					for x in hs:
						if monopolytest(x, 'm') and ownedby[x] == p:
							z = 0
							for y in hdic[x]:
								if ismortgaged[y]:
									z = 1
							if z == 0:
								hid[hi] = x
								hi += 1
					a = 1
					await self.bot.say('Select the color groups to buy houses')
					hold = 'id numh price name\n'
					while a < hi:
						hold += '{:2} {:4} {:5d} {}'.format(a,numhouse[hid[a]],houseprice[hid[a]],color[hid[a]])+'\n'
						a += 1
					await self.bot.say('```'+hold.strip()+'\nYou have $'+str(bal[p])+'```')
					i = 0
					while i == 0:
						t = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
						t = t.content               # t            : Color group number identifier
						try:                        # tt           : Number of houses to change to
							t = int(t)              # ttt          : y/n to confirm
							if 0 < t < hi:          # hid[t]       : first prop number in color group
								i = 1               # hdic[hid[t]] : list of 2 or 3 props in color group
							else:
								await self.bot.say('Select one of the options')
						except:
							if t == 'd':
								i,io = 10,1
							else:
								await self.bot.say('Select one of the options')
					while i == 1:
						await self.bot.say('Enter a new house amount or "c" to cancel')
						tt = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
						tt = tt.content
						try:
							tt = int(tt)
							if tt == numhouse[hid[t]]:
								await self.bot.say('You already have that many houses!')
							elif 0 <= tt <= 5:
								i = 2
							else:
								await self.bot.say('Select a number from 0 to 5')
						except:
							if tt == 'c':
								i = 10
							else:
								await self.bot.say('Select a number from 0 to 5')
					if i == 2:
						amount = 0
						if tt < numhouse[hid[t]]: #losing houses
							for x in hdic[hid[t]]:
								amount += (numhouse[hid[t]]-tt)*(houseprice[hid[t]]//2)
							await self.bot.say('Are you sure you want to sell '+str(numhouse[hid[t]]-tt)+' houses on '+color[hid[t]]+'? You will get $'+str(amount))
							while i == 2:
								ttt = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
								ttt = ttt.content
								if ttt == 'y':
									for x in hdic[hid[t]]:
										numhouse[x] = tt
									bal[p] += amount
									doprint = True
									i = 3
								elif ttt == 'n':
									i = 3
								else:
									await self.bot.say('Select y or n')
						elif tt > numhouse[hid[t]]: #gaining houses
							for x in hdic[hid[t]]:
								amount += (tt-numhouse[hid[t]])*(houseprice[hid[t]])
							if bal[p] < amount:
								await self.bot.say('You do not have enough money. You need $'+str(amount-bal[p])+' more.')
								i = 3
							else:
								await self.bot.say('Are you sure you want to buy '+str(tt-numhouse[hid[t]])+' houses on '+color[hid[t]]+'? You will lose $'+str(amount))
								while i == 2:
									ttt = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
									ttt = ttt.content
									if ttt == 'y':
										for x in hdic[hid[t]]:
											numhouse[x] = tt
										bal[p] -= amount
										doprint = True
										i = 3
									elif ttt == 'n':
										i = 3
									else:
										await self.bot.say('Select one of the options')
					if doprint:
						await bprint()
						await self.bot.say('You now have $'+str(bal[p]))

			async def cc(): #get a cc card
				global ccn
				await self.bot.say('Your card reads:\n'+ccname[ccorder[ccn]])
				if ccorder[ccn] == 0:
					tile[p] = 0
					bal[p] += 200
					await bprint()
					await self.bot.say('You now have $'+str(bal[p]))
				elif ccorder[ccn] == 1:
					bal[p] += 200
					await self.bot.say('You now have $'+str(bal[p]))
				elif ccorder[ccn] == 2:
					bal[p] -= 50
					await self.bot.say('You now have $'+str(bal[p]))
				elif ccorder[ccn] == 3:
					bal[p] += 50
					await self.bot.say('You now have $'+str(bal[p]))
				elif ccorder[ccn] == 4:
					goojf[p] += 1
					if goojf[p] == 1:
						await self.bot.say('You now have '+str(goojf[p])+' get out of jail free card.')
					else:
						await self.bot.say('You now have '+str(goojf[p])+' get out of jail free cards.')
				elif ccorder[ccn] == 5:
					tile[p] = 10
					injail[p] = True
					await bprint()
					global wd
					wd = 0
				elif ccorder[ccn] == 6:
					bal[p] += 50*numalive
					for i in range(1,num+1):
						if alive[i]:
							bal[i] -= 50
							await self.bot.say(name[i]+' now has $'+str(bal[i]))
				elif ccorder[ccn] == 7 or ccorder[ccn] == 10 or ccorder[ccn] == 16:
					bal[p] += 100
					await self.bot.say('You now have $'+str(bal[p]))
				elif ccorder[ccn] == 8:
					bal[p] += 20
					await self.bot.say('You now have $'+str(bal[p]))
				elif ccorder[ccn] == 9 or ccorder[ccn] == 15:
					bal[p] += 10
					await self.bot.say('You now have $'+str(bal[p]))
				elif ccorder[ccn] == 11:
					bal[p] -= 100
					await self.bot.say('You now have $'+str(bal[p]))
				elif ccorder[ccn] == 12:
					bal[p] -= 150
					await self.bot.say('You now have $'+str(bal[p]))
				elif ccorder[ccn] == 13:
					bal[p] += 25
					await self.bot.say('You now have $'+str(bal[p]))
				elif ccorder[ccn] == 14:
					await housepay(40, 115)
				ccn += 1
				if ccn > 16:
					shuffle(ccorder)
					ccn = 0

			async def chance(): #get a chance card
				global chancen
				await self.bot.say('Your card reads:\n'+chancename[chanceorder[chancen]])
				if chanceorder[chancen] == 0:
					tile[p] = 0
					bal[p] += 200
					await bprint()
					await self.bot.say('You now have $'+str(bal[p]))
				elif chanceorder[chancen] == 1:
					if tile[p] > 24:
						bal[p] += 200
						await self.bot.say('You passed go, you now have $'+str(bal[p]))
					tile[p] = 24 
					await cchanceland()
				elif chanceorder[chancen] == 2:
					if tile[p] > 11:
						bal[p] += 200
						await self.bot.say('You passed go, you now have $'+str(bal[p]))
					tile[p] = 11
					await cchanceland()
				elif chanceorder[chancen] == 3:
					if tile[p] <= 12:
						tile[p] = 12
					elif 12 < tile[p] <= 28:
						tile[p] = 28
					else:
						bal[p] += 200
						await self.bot.say('You passed go, you now have $'+str(bal[p]))
						tile[p] = 12 
					await bprint()
					await self.bot.say('You are now at '+tilename[tile[p]])
					if ownedby[tile[p]] == 0 and bal[p] >= pricebuy[tile[p]]:
						await self.bot.say('Would you like to buy '+tilename[tile[p]]+' for $'+str(pricebuy[tile[p]])+'? (y/n) You have $'+str(bal[p])+'.')
						a = 0
						while a == 0:
							response = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
							response = response.content
							if response == 'y': #buy property
								bal[p] -= pricebuy[tile[p]]
								ownedby[tile[p]] = p
								await self.bot.say(name[p]+' now owns '+tilename[tile[p]]+' and has $'+str(bal[p]))
								a = 1
							elif response == 'n': #pass on property
								a = 1
							else:
								await self.bot.say('Please select y or n')
								continue
					elif ownedby[tile[p]] == 0 and bal[p] < pricebuy[tile[p]]:
						await self.bot.say('You cannot afford '+tilename[tile[p]]+', you only have $'+str(bal[p])+' of $'+str(pricebuy[tile[p]])+'.')
					elif ownedby[tile[p]] == p: #player is owner
						await self.bot.say('You own this property already.')
					elif ismortgaged[tile[p]] == 1:
						await self.bot.say('This property is mortgaged.')
					elif ownedby[tile[p]] > 0: #pay rent
						await roll()
						bal[p] -= ((d1 + d2)*10)
						bal[ownedby[tile[p]]] += ((d1 + d2)*10)
						await self.bot.say('You paid $'+str((d1 + d2)*10)+' of rent to '+name[ownedby[tile[p]]]+'. You now have $'+str(bal[p])+'. '+name[ownedby[tile[p]]]+' now has $'+str(bal[ownedby[tile[p]]])+'.')
				elif chanceorder[chancen] == 4:
					if tile[p] <= 5:
						tile[p] = 5
					elif tile[p] <= 15:
						tile[p] = 15
					elif tile[p] <= 25:
						tile[p] = 25
					elif tile[p] <= 35:
						tile[p] = 35
					else:
						bal[p] += 200
						await self.bot.say('You passed go, you now have $'+str(bal[p]))
						tile[p] = 5
					await bprint()
					await self.bot.say('You are now at '+tilename[tile[p]])
					if ownedby[tile[p]] == 0 and bal[p] >= pricebuy[tile[p]]:
						await self.bot.say('Would you like to buy '+tilename[5]+' for $'+str(pricebuy[5])+'? (y/n) You have $'+str(bal[p])+'.')
						a = 0
						while a == 0:
							response = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
							response = response.content
							if response == 'y': #buy property
								bal[p] -= pricebuy[tile[p]]
								ownedby[tile[p]] = p
								await bprint()
								await self.bot.say(name[p]+' now owns '+tilename[5]+' and has $'+str(bal[p]))
								a = 1
							elif response == 'n': #pass on property
								a = 1
							else:
								await self.bot.say('Please select y or n')
								continue
					elif ownedby[tile[p]] == 0 and bal[p] < pricebuy[tile[p]]:
						await self.bot.say('You cannot afford '+tilename[tile[p]]+', you only have $'+str(bal[p])+' of $'+str(pricebuy[tile[p]])+'.')
					elif ownedby[tile[p]] == p:
						await self.bot.say('You own this property already.')
					elif ismortgaged[tile[p]] == 1:
						await self.bot.say('This property is mortgaged.')
					else:
						rr = 0
						if ownedby[5] == ownedby[tile[p]]:
							rr += 1
						if ownedby[15] == ownedby[tile[p]]:
							rr += 1
						if ownedby[25] == ownedby[tile[p]]:
							rr += 1
						if ownedby[35] == ownedby[tile[p]]:
							rr += 1
						bal[p] -= rrprice[rr]*2
						bal[ownedby[tile[p]]] += rrprice[rr]*2
						await self.bot.say('You paid $'+str(rrprice[rr]*2)+' of rent to '+name[ownedby[tile[p]]]+'. You now have $'+str(bal[p])+'. '+name[ownedby[tile[p]]]+' now has $'+str(bal[ownedby[tile[p]]])+'.')
				elif chanceorder[chancen] == 5:
					bal[p] += 50
					await self.bot.say('You now have $'+str(bal[p]))
				elif chanceorder[chancen] == 6:
					goojf[p] += 1
					if goojf[p] == 1:
						await self.bot.say('You now have '+str(goojf[p])+' get out of jail free card.')
					else:
						await self.bot.say('You now have '+str(goojf[p])+' get out of jail free cards.')
				elif chanceorder[chancen] == 7:
					tile[p] -= 3
					await landnd()
				elif chanceorder[chancen] == 8:
					tile[p] = 10
					await bprint()
					injail[p] = True
					global wd
					wd = 0
				elif chanceorder[chancen] == 9:
					await housepay(25, 100)
				elif chanceorder[chancen] == 10:
					bal[p] -= 15
					await self.bot.say('You now have $'+str(bal[p]))
				elif chanceorder[chancen] == 11:
					if tile[p] > 5:
						bal[p] += 200
						await self.bot.say('You passed go, you now have $'+str(bal[p]))
					tile[p] = 5
					await bprint()
					if ownedby[5] == 0 and bal[p] >= pricebuy[5]:
						await self.bot.say('Would you like to buy '+tilename[5]+' for $'+str(pricebuy[5])+'? (y/n) You have $'+str(bal[p])+'.')
						a = 0
						while a == 0:
							response = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
							response = response.content
							if response == 'y': #buy property
								bal[p] -= pricebuy[5]
								ownedby[5] = p
								await bprint()
								await self.bot.say(name[p]+' now owns '+tilename[5]+' and has $'+str(bal[p]))
								a = 1
							elif response == 'n': #pass on property
								a = 1
							else:
								await self.bot.say('Please select y or n')
								continue
					elif ownedby[5] == 0 and bal[p] < pricebuy[5]:
						await self.bot.say('You cannot afford '+tilename[5]+', you only have $'+str(bal[p])+' of $'+str(pricebuy[5])+'.')
					elif ownedby[5] == p:
						await self.bot.say('You own this property already.')
					elif ismortgaged[5] == 1:
						await self.bot.say('This property is mortgaged.')
					else:
						rr = 0
						if ownedby[5] == ownedby[5]:
							rr += 1
						if ownedby[15] == ownedby[5]:
							rr += 1
						if ownedby[25] == ownedby[5]:
							rr += 1
						if ownedby[35] == ownedby[5]:
							rr += 1
						bal[p] -= rrprice[rr]
						bal[ownedby[5]] += rrprice[rr]
						await self.bot.say('You paid $'+str(rrprice[rr])+' of rent to '+name[ownedby[5]]+'. You now have $'+str(bal[p])+'. '+name[ownedby[5]]+' now has $'+str(bal[ownedby[5]])+'.')
				elif chanceorder[chancen] == 12:
					tile[p] = 39
					await cchanceland()
				elif chanceorder[chancen] == 13:
					bal[p] -= 50*numalive
					for i in range(1,num+1):
						if alive[i]:
							bal[i] += 50
							await self.bot.say(name[i]+' now has $'+str(bal[i]))
				elif chanceorder[chancen] == 14:
					bal[p] += 150
					await self.bot.say('You now have $'+str(bal[p]))
				elif chanceorder[chancen] == 15:
					bal[p] += 100
					await self.bot.say('You now have $'+str(bal[p]))
				chancen += 1
				if chancen > 16:
					shuffle(chanceorder)
					chancen = 0

			async def cchanceland(): #reduced land() code for cchance moves
				await bprint()
				if ownedby[tile[p]] == 0 and bal[p] >= pricebuy[tile[p]]:
					await self.bot.say('Would you like to buy '+tilename[tile[p]]+' for $'+str(pricebuy[tile[p]])+'? (y/n) You have $'+str(bal[p])+'.')
					a = 0
					while a == 0:
						response = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
						response = response.content
						if response == 'y': #buy property
							bal[p] -= pricebuy[tile[p]]
							ownedby[tile[p]] = p
							await bprint()
							await self.bot.say(name[p]+' now owns '+tilename[tile[p]]+' and has $'+str(bal[p]))
							a = 1
						elif response == 'n': #pass on property
							a = 1
						else:
							await self.bot.say('Please select y or n')
							continue
				elif ownedby[tile[p]] == 0 and bal[p] < pricebuy[tile[p]]:
					await self.bot.say('You cannot afford '+tilename[tile[p]]+', you only have $'+str(bal[p])+' of $'+str(pricebuy[tile[p]])+'.')
				elif ownedby[tile[p]] == p: #player is owner
					await self.bot.say('You own this property already.')
				elif ismortgaged[tile[p]] == 1:
					await self.bot.say('This property is mortgaged.')
				elif ownedby[tile[p]] > 0: #pay rent
					if monopolytest(tile[p], 'm') and numhouse[tile[p]] == 0:
						bal[p] -= 2*(rentprice[tile[p]*6+numhouse[tile[p]]])
						bal[ownedby[tile[p]]] += 2*(rentprice[tile[p]*6+numhouse[tile[p]]])
						await self.bot.say('You paid $'+str(2*(rentprice[tile[p]*6+numhouse[tile[p]]]))+' of rent to '+name[ownedby[tile[p]]]+'. You now have $'+str(bal[p])+'. '+name[ownedby[tile[p]]]+' now has $'+str(bal[ownedby[tile[p]]])+'.')
					else:
						bal[p] -= rentprice[tile[p]*6+numhouse[tile[p]]]
						bal[ownedby[tile[p]]] += rentprice[tile[p]*6+numhouse[tile[p]]]
						await self.bot.say('You paid $'+str(rentprice[tile[p]*6+numhouse[tile[p]]])+' of rent to '+name[ownedby[tile[p]]]+'. You now have $'+str(bal[p])+'. '+name[ownedby[tile[p]]]+' now has $'+str(bal[ownedby[tile[p]]])+'.')

			async def housepay(h1, h2): #pay for houses and hotels in cchance cards
				pay = 0
				for i in range(40):
					if ownedby[i] == p:
						if numhouse[i] == 0:
							pass
						elif numhouse[i] == 5:
							pay += h2
						else:
							pay += h1*numhouse[i]
				bal[p] -= pay
				await self.bot.say('You pay $'+str(pay)+' in repairs. You now have $'+str(bal[p]))

			async def land(): #move player
				tile[p] += d1 + d2
				if tile[p] >= 40: #going past go
					tile[p] -= 40
					bal[p] += 200
					await self.bot.say('You passed go! You now have $'+str(bal[p]))
				await landnd()

			async def landnd(): #affecting properties
				await bprint()
				await self.bot.say(name[p]+' landed at '+tilename[tile[p]])
				if ownedby[tile[p]] == 0 and bal[p] >= pricebuy[tile[p]]: #unowned and can afford
					await self.bot.say('Would you like to buy '+tilename[tile[p]]+' for $'+str(pricebuy[tile[p]])+'? (y/n) You have $'+str(bal[p])+'.')
					a = 0
					while a == 0:
						response = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
						response = response.content
						if response == 'y': #buy property
							bal[p] -= pricebuy[tile[p]]
							ownedby[tile[p]] = p
							await bprint()
							await self.bot.say(name[p]+' now owns '+tilename[tile[p]]+' and has $'+str(bal[p]))
							a = 1
						elif response == 'n': #pass on property
							a = 2
						else:
							await self.bot.say('Please select y or n')
							continue
				elif ownedby[tile[p]] == 0 and bal[p] < pricebuy[tile[p]]: #unowned can't afford
					await self.bot.say('You cannot afford '+tilename[tile[p]]+', you only have $'+str(bal[p])+' of $'+str(pricebuy[tile[p]])+'.')
				elif ownedby[tile[p]] == p: #player is owner
					await self.bot.say('You own this property already.')
				elif ismortgaged[tile[p]] == 1:
					await self.bot.say('This property is mortgaged.')
				elif ownedby[tile[p]] > 0 and rentprice[tile[p]*6] == -1: #rr and utilities
					if tile[p] in (12, 28): #utility
						if ownedby[12] == ownedby[28]: #own both
							bal[p] -= ((d1 + d2)*10)
							bal[ownedby[tile[p]]] += ((d1 + d2)*10)
							await self.bot.say('You paid $'+str((d1 + d2)*10)+' of rent to '+name[ownedby[tile[p]]]+'. You now have $'+str(bal[p])+'. '+name[ownedby[tile[p]]]+' now has $'+str(bal[ownedby[tile[p]]])+'.')
						else: #own only one
							bal[p] -= ((d1 + d2)*4)
							bal[ownedby[tile[p]]] += ((d1 + d2)*4)
							await self.bot.say('You paid $'+str((d1 + d2)*4)+' of rent to '+name[ownedby[tile[p]]]+'. You now have $'+str(bal[p])+'. '+name[ownedby[tile[p]]]+' now has $'+str(bal[ownedby[tile[p]]])+'.') 
					elif tile[p] in (5, 15, 25, 35):
						rr = 0
						if ownedby[5] == ownedby[tile[p]]:
							rr += 1
						if ownedby[15] == ownedby[tile[p]]:
							rr += 1
						if ownedby[25] == ownedby[tile[p]]:
							rr += 1
						if ownedby[35] == ownedby[tile[p]]:
							rr += 1
						bal[p] -= rrprice[rr]
						bal[ownedby[tile[p]]] += rrprice[rr]
						await self.bot.say('You paid $'+str(rrprice[rr])+' of rent to '+name[ownedby[tile[p]]]+'. You now have $'+str(bal[p])+'. '+name[ownedby[tile[p]]]+' now has $'+str(bal[ownedby[tile[p]]])+'.')
				elif ownedby[tile[p]] > 0: #pay rent
					if monopolytest(tile[p], 'm') and numhouse[tile[p]] == 0:
						bal[p] -= 2*(rentprice[tile[p]*6+numhouse[tile[p]]])
						bal[ownedby[tile[p]]] += 2*(rentprice[tile[p]*6+numhouse[tile[p]]])
						await self.bot.say('You paid $'+str(2*(rentprice[tile[p]*6+numhouse[tile[p]]]))+' of rent to '+name[ownedby[tile[p]]]+'. You now have $'+str(bal[p])+'. '+name[ownedby[tile[p]]]+' now has $'+str(bal[ownedby[tile[p]]])+'.')
					else:
						bal[p] -= rentprice[tile[p]*6+numhouse[tile[p]]]
						bal[ownedby[tile[p]]] += rentprice[tile[p]*6+numhouse[tile[p]]]
						await self.bot.say('You paid $'+str(rentprice[tile[p]*6+numhouse[tile[p]]])+' of rent to '+name[ownedby[tile[p]]]+'. You now have $'+str(bal[p])+'. '+name[ownedby[tile[p]]]+' now has $'+str(bal[ownedby[tile[p]]])+'.')
				elif ownedby[tile[p]] == -1: #other spaces
					if tile[p] in (0, 20):
						pass
					elif tile[p] in (2, 17, 33): #cc
						await cc()
					elif tile[p] in (7, 22, 36): #chance
						await chance()
					elif tile[p] == 10:
						await self.bot.say('Just visiting!')
					elif tile[p] == 30:
						injail[p] = True
						tile[p] = 10
						global wd
						wd = 0
						await bprint()
						await self.bot.say('You are now in jail!')
					elif tile[p] == 4:
						bal[p] -= 200
						await self.bot.say('You paid $200 of Income Tax. You now have $'+str(bal[p]))
					elif tile[p] == 38:
						bal[p] -= 100
						await self.bot.say('You paid $100 of Super Tax. You now have $'+str(bal[p]))
				if bal[p] < 0:
					await debt() 

			async def turn(): #choices on turn
				global p
				global tile
				global bal
				nod = 0
				await bprint()
				await self.bot.say(name[p]+'\'s turn!')
				if bal[p] < 0:
					await debt()
				if injail[p] and alive[p]:
					await jail()
				else:
					global wd
					wd = 1
					while wd == 1 and alive[p]:
						r = 0
						while r == 0:
							await self.bot.say('Type r to roll, t to trade, h to manage houses, or m to mortgage.')
							choice = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
							choice = choice.content
							if choice == 'r': #normal turn, roll dice
								global d1,d2
								await roll()
								if d1 == d2:
									nod += 1
								else:
									wd = 0
								if nod == 3:
									await self.bot.say('You rolled doubles 3 times in a row, you are now in jail!')
									tile[p] = 10
									injail[p] = True
									wd = 0
								else:
									await land()
								r = 1
							elif choice == '?': #run debug code
								await debug()
							elif choice == 't': #make a trade
								await trade()
							elif choice == 'm': #mortgage
								await mortgage()
							elif choice == 'h': #manage houses
								await house()
							elif choice == 's': #print game save message
								global autosave
								await self.bot.say('Copy the following, put it in a text file called "save.txt", and relaunch monopoly.py to restart from here.\n\n```'+autosave+'```\n')
				r = 1
				while r == 1 and alive[p]:
					await self.bot.say('Type t to trade, m to mortgage, h to manage houses, or d when done.')
					choice = await self.bot.wait_for_message(timeout=60, author=id[p], channel=channel)
					choice = choice.content
					if choice == 't':
						await trade()
					elif choice == 'd':
						r = 2
					elif choice == '?':
						await debug()
					elif choice == 'm':
						await mortgage()
					elif choice == 'h':
						await house()

			async def debug(): #print debug info
				a = 0
				hold = 'id price owner ism mprice numh hprice name'
				while a < 20:
					hold += '{:2d} {:5d} {:5d} {:3d} {:6d} {:4d} {:6d} {}'.format(a,pricebuy[a],ownedby[a],ismortgaged[a],mortgageprice[a],numhouse[a],houseprice[a],tilename[a])+'\n'
					a += 1
				hold += str(bal[1:])
				await self.bot.say('```'+hold.strip()+'```')
				hold = 'id price owner ism mprice numh hprice name'
				while a < 40:
					hold += '{:2d} {:5d} {:5d} {:3d} {:6d} {:4d} {:6d} {}'.format(a,pricebuy[a],ownedby[a],ismortgaged[a],mortgageprice[a],numhouse[a],houseprice[a],tilename[a])+'\n'
					a += 1
				await self.bot.say('```'+hold.strip()+'```')

			#start of run code
			global p
			p = 1
			while numalive >= 2:
				if p > num:
					p = 1
				if alive[p]:
					autosave = ('name = '+str(name)+'\ntilename = '+str(tilename)+'\ninjail = '+str(injail)+'\ntile = '+str(tile)+'\nbal = '+str(bal)+'\np = '+str(p)+'\nownedby = '+str(ownedby)+'\nnumhouse = '+str(numhouse)+'\nismortgaged = '+str(ismortgaged)+'\ngoojf = '+str(goojf)+'\nalive = '+str(alive)+'\njailturn ='+str(jailturn))
					await turn()
				p += 1
			for o in range(1,num+1):
				if alive[o]:
					await self.bot.say(name[o]+' wins!')
			await self.bot.say('\nDebug information\n')
			await debug()
			await self.bot.say('\nSave information\n\n'+autosave)
		except asyncio.TimeoutError:
			await self.bot.say('You took too long. Shutting down.\nSave info:\n'+autosave)
		except:
			await self.bot.say(autosave)
			raise

def setup(bot):
	bot.add_cog(Monopoly(bot))
