import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv 
import os
from pixivapi import Client

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
client = Client()
#---

async def pixivImageGetter(id):
  client.login("user_xhru3788", "severminecraft")
  

#botloop
@bot.event 
async def on_ready(): 
  print(f'Logged in as {bot.user}') #prints to log ('logged in as momobot #whatever')

@bot.event
async def on_message(message):
    if message.author == bot.user: #*should* be temp
        return
    if "gay" in message.content.lower():
        await message.channel.send(message.author.avatar)
        await message.channel.send(message.author.mention)      

@bot.hybrid_command(name="test", with_app_command=True, description="Testes")
@discord.app_commands.guilds(discord.Object(id=1390176544210550935)) #AZUREYAKO SERVER REPLACE
async def test(ctx: commands.Context):
    #await ctx.defer(ephemeral=True)
    await ctx.reply()

bot.run(token, log_handler = handler, log_level = logging.INFO) #yeah idk
