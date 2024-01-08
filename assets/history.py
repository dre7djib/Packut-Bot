import os
import json
from discord.ext import commands
from assets.utils.hashmap import HashMap


class CommandHistory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.history_folder = "CommandHistory"
        self.history = HashMap()

        # Vérifier si le dossier existe, sinon le créer
        if not os.path.exists(self.history_folder):
            os.makedirs(self.history_folder)

        for fileName in os.listdir(self.history_folder):
            userId = fileName.split(".")[0]
            userCommandHistory = self.loadUserCommandHistory(userId)
            self.history.insert(userId, userCommandHistory)

    def loadUserCommandHistory(self, userId):
        fileName = f"{userId}.json"
        filePath = os.path.join(self.history_folder, fileName)
        try:
            with open(filePath, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def saveUserCommandHistory(self, userId, commandHistory):
        os.makedirs(self.history_folder, exist_ok=True)
        filePath = os.path.join(self.history_folder, f"{userId}.json")
        with open(filePath, "w") as file:
            json.dump(commandHistory, file, indent=4)

    @commands.Cog.listener()
    async def on_ready(self):
        for fileName in os.listdir(self.history_folder):
            userId = fileName.split(".")[0]
            userCommandHistory = self.loadUserCommandHistory(userId)
            self.history.insert(userId, userCommandHistory)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        """Sauvegarde la commande dans l'historique"""
        if ctx.author.bot or ctx.command.name == "history":
            return

        user_id = str(ctx.author.id)
        user_history = self.history.get(user_id)
        if user_history is None:
            user_history = []
            self.history.insert(user_id, user_history)

        user_history.append(ctx.message.content)
        self.saveUserCommandHistory(user_id, user_history)

    @commands.command(name = "lastHistory")
    async def lastCommand(self, ctx):
        """Displays the last command entered by the user"""
        if not await self.bot.checkAccess(ctx):
            return
        userId = str(ctx.author.id)
        userCommandHistory = self.history.get(userId)

        if userCommandHistory is not None and len(userCommandHistory) > 1:
            lastCommand = userCommandHistory[-2]
            await ctx.send(f"{ctx.author}, the last command was: {lastCommand}")
        else:
            await ctx.send(f"{ctx.author}, you have no command history")

    @commands.command(name= "clearHistory")
    async def clearCommandHistory(self, ctx):
        """Deletes the user's command history"""
        if not await self.bot.checkAccess(ctx):
            return

        userId = str(ctx.author.id)
        self.history.remove(userId)
        self.saveUserCommandHistory(userId, [])

        await ctx.send(f"{ctx.author.mention}, your command history has been cleared!")

    @commands.command(name="history")
    async def _commandHistory(self, ctx):
        """Displays the user's command history"""
        userId = str(ctx.author.id)
        userCommandHistory = self.history.get(userId)
        if userCommandHistory is None or len(userCommandHistory) == 0:
            await ctx.send(f"{ctx.author.mention}, there is no command history for you.")
        else:
            commandHistoryStr = "\n".join(userCommandHistory)
            await ctx.send(f"Command history for {ctx.author.mention}:\n```\n{commandHistoryStr}\n```")

def setup(bot):
    return bot.add_cog(CommandHistory(bot))
