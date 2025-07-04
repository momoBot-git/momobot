import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv 
import os
from pixivapi import Client
from gppt import GetPixivToken

client = Client()

#TODO
#determine if r18 and block sending in sfw channels if true

load_dotenv() #i fucking hate ai suggestions
token = str(os.getenv('DISCORD_TOKEN'))

handler = logging.FileHandler(filename = 'discord.log', encoding = 'utf-8', mode = 'w') #for the logging

class Bot(commands.Bot): #define bot and scope
  def __init__(self):
    intents = discord.Intents.default()
    intents.message_content = True #enables bot to read most messages
    super().__init__(command_prefix = '!', intents = intents)

  async def setup_hook(self): #wait for sync before running main loop
    await self.tree.sync(guild = discord.Object(id=1390176544210550935)) #change this to mahoako server later possibly
    print(f'Synced slash commands for {self.user}')

  async def error(self, ctx, error):
    await ctx.reply(error, ephemeral=True)

#defining vars
bot = Bot()

#ive entirely given up on having readable code
def get_refresh_token() -> str:
  with open("token.txt", "w+") as f:
      if refresh_token := f.read().strip():
          return refresh_token

      g = GetPixivToken(headless=True)
      refresh_token = g.login(username="user_xhru3788", password="severminecraft")["refresh_token"]
      f.write(refresh_token)
      return refresh_token


#botloop
@bot.event 
async def on_ready(): 
  print(f'Logged in as {bot.user}') #prints to log ('logged in as momobot #whatever')
  
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "gay" in message.content.lower():
        await message.channel.send(message.author.avatar)
        await message.channel.send(message.author.mention)      
        client.authenticate(get_refresh_token()) #login to pixiv
        print(f'Logged in to Pixiv: {client.account}')
        await message.channel.send("logined")
        return

@bot.hybrid_command(name="test", with_app_command=True, description="Testes")
@discord.app_commands.guilds(discord.Object(id=1390176544210550935)) #AZUREYAKO SERVER REPLACE
async def test(ctx: commands.Context, member1: discord.Member, member2: discord.Member, id):
    #await ctx.defer(ephemeral=True)
    await ctx.send(id)
    await ctx.send(member1.display_avatar.url)
    await ctx.send(member2.display_avatar.url)
    illustration = client.fetch_illustration(id)
    await ctx.send(illustration.title)
    for i in illustration.image_urls:
      await ctx.send(str(i))

print(get_refresh_token())
print(f'Logged in to Pixiv: {client.account}')
bot.run(token, log_handler = handler, log_level = logging.INFO) #yeah idk
