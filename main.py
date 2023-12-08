import discord
import json
import csv
import functions.playersDB as playerDB
import functions.userDB as userDB
import functions.db as db
import functions.playersViewDB as playersViewDB
from discord.ext.commands import cooldown, BucketType
from read_csv import readcsv
from read_csv import insertCSV
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


# Bot
@client.event
async def on_guild_join(guild):
    insertCSV(conn,"archive/male_players.csv")

    channelRules = "Rules and Commands"
    channelPlay = "Play FutPack"
    category_name = "FutPack"  

    category = discord.utils.get(guild.categories, name=category_name)
    if category is None:
        category = await guild.create_category(category_name)

    existing_channel = discord.utils.get(guild.channels, name=channelRules, category=category)
    if existing_channel is None:
        channel = await category.create_text_channel(channelRules)
        

        embed=discord.Embed(title="Welcome on the server, Here is the rules and commands to play FutPack", description="First of all, FutPack is a game where you can open packs with credits name crix, at the beginning you are given 500 crix. The main goal is to have the best team possible compare to your friend.", color=0x9929bd)
        embed.set_author(name="dre7djib", url="https://github.com/dre7djib")
        embed.add_field(name="&start", value="Command to start your game with the Bot", inline=False)
        embed.add_field(name="&pack", value="Command to open pack. Each pack cost 100 crix and you get 6 players in. May the luck will be with you ", inline=False)
        embed.add_field(name="&fut", value="Every 30min, you can use this commands to get 50 crix ", inline=False)
        embed.add_field(name="&crix", value="Command to see how much crix you have", inline=False)
        embed.add_field(name="&sell", value="Command to sell one of your player. In exchange you gain the value of the player you sold", inline=False)
        embed.add_field(name="&player", value="Command to see the card of a player with his value, photo, and description", inline=False)
        embed.add_field(name="&giveP", value="Command to give to another player one of your card", inline=False)
        embed.add_field(name="&giveC", value="Command to give to another player a certain amount of your crix", inline=True)
        await channel.send(embed=embed)
        
        await channel.set_permissions(client.user, send_messages=True, read_messages=True)
        await channel.set_permissions(guild.default_role, send_messages=False)  # Désactive les messages pour les autres membres
    
    existing_channel = discord.utils.get(guild.channels, name=channelPlay, category=category)
    if existing_channel is None:
        channel = await category.create_text_channel(channelPlay)





# Command
@client.command(name="delete")
async def clear(ctx, amount=30):
	await ctx.channel.purge(limit=amount)

@client.command(name="pack")
@commands.cooldown(1, 30, commands.BucketType.user) # Get 6 random players in your team
async def pack(ctx):
        userCrix = int(userDB.getCrix(conn,ctx.author.id))
        if userCrix == 0:
            return "Can't open a pack because you are out of crix"
        else:
            rmCrix = userCrix - 100
            str(userDB.setCrix(conn,rmCrix,ctx.author.id))
            for i in range(10): 
                player = readcsv(m_players)
                while playerDB.getPlayerId == True:
                    player = readcsv(m_players)

                valCrix = float(player[10]) / 100000
                if valCrix < 1:
                    valCrix = 1
                
                playerId = player[0]
                playerName = player[5]
                position = player[7]
                version = int(player[2])
                photoLink = "https://cdn.sofifa.net/players/"+str(player[0])[:3]+"/"+str(player[0])[3:]+"/23_240.png"
                userId = ctx.author.id

                playerDB.createPlayer(conn,playerId,playerName,round(valCrix),position,photoLink,userId)

                # Créez un embed
                embed = discord.Embed(
                    title = player[5],
                    description = position,
                    color = discord.Color.purple()
                )
                embed.set_image(url=photoLink)
                embed.set_thumbnail(url=ctx.author.avatar)
                embed.set_footer(text=str(round(valCrix)) + " ◊" + "    ------------------ FIFA " + version)
                await ctx.channel.send(embed=embed)

@client.command(name="start") # Init Player 
async def crix(ctx):
    discordId = ctx.author.id
    discordName = ctx.author.name
    if userDB.getUserId(conn,discordId):
        bot_channel = client.get_channel(1167402766352793620)
        await bot_channel.send("You already start playing")
    else:
        userDB.createUser(conn, discordName, discordId)

@client.command(name="team") # Show player of a user
async def team(ctx,  userName : discord.Member):
    discordId = userName.id
    players = playerDB.getAllPlayers(conn,discordId)
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
    userId = playerDB.getUserIdByPlayerName(conn, name)
    if userId == False or discordId != userId[0]:
        em = discord.Embed(title="You can't sell that player because it's not yours", color=discord.Color.red())
        await ctx.send(embed=em)
    else:
        valueCrix = playerDB.getValueCrix(conn,name)
        crix = valueCrix + userDB.getCrix(conn, discordId)
        userDB.setCrix(conn,crix, discordId)
        playerId = playerDB.getPlayerIdByName(conn,name)
        playerDB.removePlayer(conn,playerId)
        em = discord.Embed(title=f"You sold {name} for {valueCrix}",description=f"You now have {crix} crix", color=discord.Color.green())
        await ctx.send(embed=em)

@client.command(name="player")
async def player(ctx, *playerName):
    name = ' '.join(playerName)
    players = playersViewDB.getPlayersByName(conn, name)
    
    for player in players:
        photoLink = "https://cdn.sofifa.net/players/" + str(player[0])[:3] + "/" + str(player[0])[3:] + "/23_240.png"
        valCrix = float(player[10]) / 100000
        if valCrix < 1:
            valCrix = 1
        embed = discord.Embed(
            title=player[5],
            description=player[7],
            color=discord.Color.purple()
        )
        embed.set_image(url=photoLink)
        embed.set_footer(text=str(round(valCrix)) + " ◊" + "    ------------------ FIFA " + player[2])
        await ctx.channel.send(embed=embed)




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
        em = discord.Embed(title=f"You have done too much command",description=f"Try again in {error.retry_after:.2f}s.", color=discord.Color.red())
        await ctx.send(embed=em)



client.run(config['token'])