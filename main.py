import discord
import json
from read_csv import readcsv
from discord.ext import commands

# Import Token and Prefix
with open("config.json", "r") as read_file:
    config = json.load(read_file)

intents = discord.Intents.all()
client = commands.Bot(command_prefix=config['prefix'], intents = intents)



# Command
@client.command(name="delete")
async def clear(ctx, amount=10):
	await ctx.channel.purge(limit=amount)

@client.command(name="pack")
async def pack(ctx):
        for i in range(6): 
          player = readcsv()
          # Créez un embed
          embed = discord.Embed(
              title = player[6],
              description = player[7],
              color = discord.Color.purple()
          )
          embed.set_image(url="https://cdn.sofifa.net/players/"+str(player[0])[:3]+"/"+str(player[0])[3:]+"/24_240.png",)
          embed.set_thumbnail(url=ctx.author.avatar)
          await ctx.channel.send(embed=embed)


# Event
@client.event
async def on_ready():
    print("Le bot est prêt !")

@client.event
async def on_member_join(member):
    general_channel = client.get_channel(1167794216248823818)
    await general_channel.send("Bienvenue sur le serveur ! "+ member.name)


client.run(config['token'])