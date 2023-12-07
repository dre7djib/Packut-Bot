import discord
import json
import csv
import db
from discord.ext.commands import cooldown, BucketType
from read_csv import readcsv
from discord.ext import commands

# Import Token and Prefix
with open("config.json", "r") as read_file:
    config = json.load(read_file)

file = open("archive/male_players.csv", "r")
m_players = list(csv.reader(file, delimiter=","))
file.close()

conn = db.create_connection("data.db")

intents = discord.Intents.all()
client = commands.Bot(command_prefix=config['prefix'], intents = intents)



# Command
@client.command(name="delete")
async def clear(ctx, amount=30):
	await ctx.channel.purge(limit=amount)

@client.command(name="pack")
@commands.cooldown(1, 30, commands.BucketType.user) # Get 6 random players in your team
async def pack(ctx):
        userCrix = int(db.getCrix(conn,ctx.author.id))
        if userCrix == 0:
            return "Can't open a pack because you are out of crix"
        else:
            rmCrix = userCrix - 100
            str(db.setCrix(conn,rmCrix,ctx.author.id))
            for i in range(6): 
                player = readcsv(m_players)
                while db.getPlayerId == True:
                    player = readcsv(m_players)

                valCrix = float(player[10]) / 100000
                if valCrix < 1:
                    valCrix = 1
                
                playerId = player[0]
                playerName = player[5]
                position = player[7]
                photoLink = "https://cdn.sofifa.net/players/"+str(player[0])[:3]+"/"+str(player[0])[3:]+"/23_240.png"
                userId = ctx.author.id

                db.createPlayer(conn,playerId,playerName,round(valCrix),position,photoLink,userId)

                # Créez un embed
                embed = discord.Embed(
                    title = player[5],
                    description = position,
                    color = discord.Color.purple()
                )
                embed.set_image(url=photoLink)
                embed.set_thumbnail(url=ctx.author.avatar)
                embed.set_footer(text=str(round(valCrix)) + " ◊")
                await ctx.channel.send(embed=embed)


@client.command(name="start") # Init Player 
async def crix(ctx):
    discordId = ctx.author.id
    discordName = ctx.author.name
    if db.getUserId(conn,discordId):
        bot_channel = client.get_channel(1167402766352793620)
        await bot_channel.send("You already start playing")
    else:
        db.createUser(conn, discordName, discordId)

@client.command(name="team") # Show player of a user
async def team(ctx,  userName : discord.Member):
    discordId = userName.id
    players = db.getAllPlayers(conn,discordId)
    userName = str(userName)
    
    embed = discord.Embed(
    title = "Team of "+ userName,
    color = discord.Color.purple()
    )
    for name in players:
        embed.add_field(name=name, value='')
    embed.set_thumbnail(url=ctx.author.avatar)
    await ctx.channel.send(embed=embed)
    
@client.command(name="sell") # Sell a player to another user
async def sell(ctx, userName : discord.Member, *playerName):
    discordId = userName.id
    name = ' '.join(playerName)
    userId = db.getUserIdByPlayerName(conn, name)
    if discordId != userId:
        return "You can't sell that player because it's not yours"



# Event
@client.event
async def on_ready():
    print("Bot ready!")

@client.event
async def on_member_join(member):
    general_channel = client.get_channel(1167794216248823818)
    await general_channel.send("Bienvenue sur le serveur ! "+ member.name)

# Error
@pack.error
async def pack_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"You have done too much command",description=f"Try again in {error.retry_after:.2f}s.", color=discord.Color.purple())
        await ctx.send(embed=em)



client.run(config['token'])