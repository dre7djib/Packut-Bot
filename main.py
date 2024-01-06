import discord
import json
import sqlite3
import os
import csv
import random
import functions.playersDB as playerDB
import functions.userDB as userDB
import functions.db as db
import functions.playersViewDB as playersViewDB
from discord.ext.commands import cooldown, BucketType
from discord.ext import commands
from reactionmenu import ViewMenu, ViewButton
from read_csv import readcsv
from read_csv import insertCSV


# Import Token and Prefix
with open("config.json", "r") as read_file:
    config = json.load(read_file)

file = open("archive/male_players.csv", "r")
m_players = list(csv.reader(file, delimiter=","))
file.close()

if os.path.exists("data.db"):
    conn = db.create_connection("data.db") # Create connection between db and code
else:
    db.createDb()
    conn = db.create_connection("data.db")
    insertCSV(conn,"archive/male_players.csv")





intents = discord.Intents.all()
client = commands.Bot(command_prefix=config['prefix'], intents = intents, help_command=None)


# Bot
@client.event
async def on_guild_join(guild):  # When Bot Added, it create a category with 2 text channel for the Bot

    channelRules = "Rules and Commands" # Channel Rules 
    channelPlay = "Play FutPack" # Channel Play
    category_name = "FutPack"  # Category

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
@client.command(name="delete") # Temp Command to delete message in channel
async def clear(ctx, amount=30):
	await ctx.channel.purge(limit=amount)

@client.command(name="pack") # Pack players to get them in your team
@commands.cooldown(1, 30, commands.BucketType.user) # Get 6 random players in your team
async def pack(ctx):
        userCrix = int(userDB.getCrix(conn,ctx.author.id))
        if userCrix < 100:
            return await ctx.send("Can't open a pack because you don't have enough crix")

        rmCrix = userCrix - 100
        str(userDB.setCrix(conn,rmCrix,ctx.author.id))
        for i in range(6): 
            userId = ctx.author.id
            res = True
            while res:
                player = readcsv(m_players)
                playerId = str(player[0])
                getPlayerId = playerDB.getPlayerId(conn, playerId)
                
                if not getPlayerId:
                    res = False

            valCrix = float(player[10]) / 100000
            if valCrix < 1:
                valCrix = 1
            
            PlayerUserId = playerDB.getUserIdByPlayerId(conn,playerId)
            userName = userDB.getUserNameById(conn,PlayerUserId)
            if userName == False:
                userName = " "

            playerName = player[5]
            position = player[7]
            version = player[2]
            photoLink = "https://cdn.sofifa.net/players/"+str(player[0])[:3]+"/"+str(player[0])[3:]+"/23_240.png"
            
            playerDB.createPlayer(conn,playerId,playerName,round(valCrix),position,photoLink,userId)

            # Créez un embed
            embed = discord.Embed(
                title = player[5],
                description = position,
                color = discord.Color.purple()
            )
            embed.add_field(name=userName,value=" ")
            embed.set_image(url=photoLink)
            embed.set_thumbnail(url=ctx.author.avatar)
            embed.set_footer(text=str(round(valCrix)) + " ◊" + " FIFA " + version)
            await ctx.channel.send(embed=embed)

@client.command(name="start") # Init Player 
async def crix(ctx):
    discordId = ctx.author.id
    discordName = ctx.author.name
    if userDB.getUserId(conn,discordId):
        await ctx.channel.send("You already start playing")
    else:
        userDB.createUser(conn, discordName, discordId)

@client.command(name="team") # Show player of a user
async def team(ctx,  userName : discord.Member):
    discordId = userName.id
    players = playerDB.getAllPlayers(conn,discordId)
    userName = str(userName)
    countPlayers = int(playerDB.getCountPlayers(conn,discordId))
    menu = ViewMenu(ctx, menu_type=ViewMenu.TypeEmbed)
    
    nbPage = (countPlayers - 1) // 10 + 1
    count = 0
    temp = 0
    for i in range(nbPage):
        embed = discord.Embed(title = "Team of "+ userName, color = discord.Color.purple())
        for player in players[temp:temp + 10]:
            vCrix = playerDB.getValueCrix(conn,player)
            position = playerDB.getPosition(conn,player)
            embed.add_field(name=f"{player:<50} {vCrix} ◊ {position:>50}", value='', inline=False)
        
        menu.add_page(embed)
        temp += 10
    menu.add_button(ViewButton.go_to_first_page())
    menu.add_button(ViewButton.back())
    menu.add_button(ViewButton.next())
    menu.add_button(ViewButton.go_to_last_page())
    menu.add_button(ViewButton.go_to_page())

    await menu.start()

@client.command(name="sell") # Sell a player to another user
async def sell(ctx, *playerName):
    discordId = ctx.author.id
    name = ' '.join(playerName)
    userId = playerDB.getUserIdByPlayerName(conn, name)
    if userId == False or discordId != userId[0]:
        em = discord.Embed(title="You can't sell this player because it's not yours", color=discord.Color.red())
        await ctx.send(embed=em)
    else:
        valueCrix = playerDB.getValueCrix(conn,name)
        crix = valueCrix + userDB.getCrix(conn, discordId)
        userDB.setCrix(conn,crix, discordId)
        playerId = playerDB.getPlayerIdByName(conn,name)
        playerDB.removePlayer(conn,playerId)
        em = discord.Embed(title=f"You sold {name} for {valueCrix}",description=f"You now have {crix} crix", color=discord.Color.green())
        await ctx.send(embed=em)

@client.command(name="player") # Show a specific player  
async def player(ctx, *playerName):
    name = ' '.join(playerName)
    players = playersViewDB.getPlayersByName(conn, name)
    userDiscord = list(playerDB.getUserIdByPlayerName(conn,name))
    userName = ["None"]
    if userDiscord[0] != "0":
        userName = list(userDB.getUserNameById(conn,userDiscord[0]))

    menu = ViewMenu(ctx, menu_type=ViewMenu.TypeEmbed)
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
        embed.add_field(name=userName[0],value="",inline=True)
        embed.add_field(name="FIFA " + player[2],value="",inline=True)
        embed.add_field(name=player[6],value="",inline=True)
        embed.set_image(url=photoLink)
        embed.set_footer(text=str(round(valCrix)) + " ◊")
        menu.add_page(embed)

    if len(players) > 1:
        menu.add_button(ViewButton.back())
        menu.add_button(ViewButton.next())
        await menu.start()
    else:
        await ctx.send(embed = embed)

@client.command(name="fut") #Every 30min the user can use this command to win crix
@commands.cooldown(1, 30*60, commands.BucketType.user)
async def fut(ctx):
    userCrix = int(userDB.getCrix(conn,ctx.author.id))
    nbCrix = random.randint(30,120)
    addCrix = userCrix + nbCrix
    str(userDB.setCrix(conn,addCrix,ctx.author.id))

    if nbCrix > 80:
        em = discord.Embed(title=f"WOW, you won {nbCrix} crix",description=" ", color=discord.Color.green())

    else:
        em = discord.Embed(title=f"You won {nbCrix} crix",description=" ", color=discord.Color.green())
    await ctx.send(embed=em)
    
@client.command(name="crix") # Show how much crix the user have
async def crix(ctx):
    discordId = ctx.author.id
    nbCrix = str(userDB.getCrix(conn,discordId))
    em = discord.Embed(title=f"You have {nbCrix} crix",description=" ", color=discord.Color.purple())
    await ctx.send(embed=em)

@client.command(name="giveP") # Give a Player to another user
async def giveP(ctx,userName : discord.Member, *playerName):
    name = ' '.join(playerName)
    discordId = userName.id
    playerId = str(playerDB.getPlayerIdByName(conn, name))
    userId = playerDB.getUserIdByPlayerId(conn, playerId)
    userId = userId[0]
    if userId != ctx.author.id:
        em = discord.Embed(title=f"You don't have {name} in your team",description=" ", color=discord.Color.red())
        await ctx.send(embed=em)
    playerDB.setUserId(conn,playerId,str(discordId))
    em = discord.Embed(title=f"You gave {name}",description=f"The player is now in {userName} team", color=discord.Color.green())
    await ctx.send(embed=em)

@client.command(name="giveC") # Give crix to another user
async def giveC(ctx,userName : discord.Member, crix ):
    discordId = userName.id
    giverCrix = userDB.getCrix(conn,ctx.author.id)
    userGetCrix = userDB.getCrix(conn,discordId)
    if giverCrix < int(crix):
        em = discord.Embed(title=f"You can't give {crix} ◊ to {userName} because you have less than {crix} crix",description=f"", color=discord.Color.red())
        await ctx.send(embed=em)
        return
    giverCrix -= int(crix)
    userGetCrix += int(crix)
    userDB.setCrix(conn,giverCrix,ctx.author.id)
    userDB.setCrix(conn,userGetCrix,discordId)
    em = discord.Embed(title=f"{ctx.author.name} gave {crix} ◊ to {userName}",description=f"", color=discord.Color.purple())
    await ctx.send(embed=em)


# Event
@client.event
async def on_ready(): # Send message in terminal
    print("Bot ready!")

@client.event
async def on_member_join(member):  # Welcome User in the Server
    general_channel = client.get_channel(1167794216248823818)
    await general_channel.send("Bienvenue sur le serveur ! "+ member.name)


# Error
@pack.error
async def pack_error(ctx, error): # Cooldown for Command pack
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"You have done too much command",description=f"Try again in {error.retry_after:.2f}s.", color=discord.Color.red())
        await ctx.send(embed=em)

@fut.error
async def fut_error(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        em = discord.Embed(title=f"You can't do more than 1 command every 30min",description=f"Try again in {error.retry_after:.2f}s.", color=discord.Color.red())
        await ctx.send(embed=em)

client.run(config['token'])