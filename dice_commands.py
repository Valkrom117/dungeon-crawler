#dice_commands.py
import discord
import random
from discord.ext import commands

class DiceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll', help='Simulates rolling dice.')
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
        dice = [str(random.choice(range(1, number_of_sides + 1))) for _ in range(number_of_dice)]
        await ctx.send(', '.join(dice))

async def setup(bot):
    await bot.add_cog(DiceCommands(bot))