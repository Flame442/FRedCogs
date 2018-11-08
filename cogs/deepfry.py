import discord
from discord.ext import commands
from __main__ import send_cmd_help
from PIL import Image, ImageEnhance
from random import randint
import requests
from io import BytesIO



class Deepfry:
	"""Deepfries memes"""
	def __init__(self, bot):
		self.bot = bot
		self.f = 0

	@commands.command(pass_context=True)
	async def deepfry(self, ctx, amount: float=0):
		"""Deepfries images"""
		response = requests.get(ctx.message.attachments[0]['url'])
		img = Image.open(BytesIO(response.content))
		e = ImageEnhance.Sharpness(img)
		img = e.enhance(100)
		e = ImageEnhance.Contrast(img)
		img = e.enhance(100)
		e = ImageEnhance.Brightness(img)
		img = e.enhance(.27)
		try:
			r, g, b, a = img.split()
		except:
			r, g, b = img.split()
		e = ImageEnhance.Brightness(r)
		r = e.enhance(4)
		e = ImageEnhance.Brightness(g)
		g = e.enhance(1.75)
		e = ImageEnhance.Brightness(b)
		b = e.enhance(.6)
		e = ImageEnhance.Contrast(b)
		img = e.enhance(2)
		img = Image.merge("RGB", (r, g, b))
		e = ImageEnhance.Brightness(img)
		img = e.enhance(1.5)
		e = ImageEnhance.Sharpness(img)
		img = e.enhance((amount*99)+1)	
		img.save('data/deepfry/temp.jpg')
		await self.bot.send_file(ctx.message.channel, 'data/deepfry/temp.jpg')
		
	@commands.command(pass_context=True)
	async def nuke(self, ctx):
		"""Demolishes images"""
		response = requests.get(ctx.message.attachments[0]['url'])
		img = Image.open(BytesIO(response.content))
		w, h = img.size[0], img.size[1]
		dx = ((w+200)//200)*2
		dy = ((h+200)//200)*2
		img = img.resize((w//dx,h//dy))
		e = ImageEnhance.Sharpness(img)
		img = e.enhance(100)
		e = ImageEnhance.Contrast(img)
		img = e.enhance(100)
		e = ImageEnhance.Brightness(img)
		img = e.enhance(.27)
		try:
			r, g, b, a = img.split()
		except:
			r, g, b = img.split()
		e = ImageEnhance.Brightness(r)
		r = e.enhance(4)
		e = ImageEnhance.Brightness(g)
		g = e.enhance(1.75)
		e = ImageEnhance.Brightness(b)
		b = e.enhance(.6)
		e = ImageEnhance.Contrast(b)
		img = e.enhance(2)
		img = Image.merge("RGB", (r, g, b))
		e = ImageEnhance.Brightness(img)
		img = e.enhance(1.5)
		e = ImageEnhance.Sharpness(img)
		img = e.enhance(100)
		img = img.resize((w,h),Image.BILINEAR)
		img.save('data/deepfry/temp.jpg', quality=1)
		await self.bot.send_file(ctx.message.channel, 'data/deepfry/temp.jpg')
		
	async def run(self, t):
		"""Passively deepfries random images"""
		if t.author.id != self.bot.user.id:
			if t.attachments != [] and t.content.find('!deepfry') == -1 and t.content.find('!nuke') == -1:
				l = randint(1,10)
				print(l,self.f)
				if l == 4:
					response = requests.get(t.attachments[0]['url'])
					img = Image.open(BytesIO(response.content))
					e = ImageEnhance.Sharpness(img)
					img = e.enhance(100)
					e = ImageEnhance.Contrast(img)
					img = e.enhance(100)
					e = ImageEnhance.Brightness(img)
					img = e.enhance(.27)
					try:
						r, g, b, a = img.split()
					except:
						r, g, b = img.split()
					e = ImageEnhance.Brightness(r)
					r = e.enhance(4)
					e = ImageEnhance.Brightness(g)
					g = e.enhance(1.75)
					e = ImageEnhance.Brightness(b)
					b = e.enhance(.6)
					e = ImageEnhance.Contrast(b)
					img = e.enhance(2)
					img = Image.merge("RGB", (r, g, b))
					e = ImageEnhance.Brightness(img)
					img = e.enhance(1.5)
					e = ImageEnhance.Sharpness(img)
					img = e.enhance((self.f*99)+1)
					img.save('data/deepfry/temp.jpg', quality=10)
					await self.bot.send_file(t.channel, 'data/deepfry/temp.jpg')
					self.f = 0
					print('--')
				else:
					self.f += 0.07

def setup(bot):
	n = Deepfry(bot)
	bot.add_listener(n.run, "on_message")
	bot.add_cog(n)
