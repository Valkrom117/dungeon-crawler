# player_commands.py

from character import Character
from constants import RollType
from database_utils import get_character_data, get_active_character_name
from dice_utils import *
from class_utils import *
from weapon_utils import *
from discord.ext import commands

class PlayerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_characters = {}
        self.active_npcs = {}

    def _sync_cache(self, owner_id:int, char_name:str):
        data = get_character_data(owner_id, char_name)
        if data is None:
            self.active_characters.pop(owner_id, None)
            return None
        new_char = Character(**data)
        self.active_characters[owner_id] = new_char
        return new_char

    def get_active_character(self, ctx) -> Character | None:
        owner_id = ctx.author.id
        
        if owner_id in self.active_characters:
            return self.active_characters[owner_id]
            
        active_name = get_active_character_name(owner_id)
        
        if active_name:
            self._sync_cache(owner_id, active_name)
            return self._sync_cache(owner_id, active_name)

        return None

    @commands.command(name="attack", help="Rolls an attack based on currently equiped weapon. Usage: !attack")
    async def weapon_attack(self, ctx):
        active_char = self.get_active_character(ctx)
        if active_char is None:
            return await ctx.send(f'No active character found. Activate one using `!activate "<characte_name>"`')
        
        attack_roll, attack_total, attack_message = roll_d20_dice(active_char.strength, RollType.ADVANTAGE)
        attack_rolls_str = ', '.join([str(roll) for roll in attack_roll])

        if active_char.weapon is None:
            damage_rolls, damage_total, damage_message = roll_damage_dice(1, 1, active_char.strength)
        else:
            damage_rolls, damage_total, damage_message = roll_damage_dice(active_char.weapon.dice_amount, active_char.weapon.dice_sides, active_char.strength)

        damage_rolls_str = ', '.join([str(roll) for roll in damage_rolls])

        await ctx.send(
            f"{active_char.weapon.name} {attack_message}: {attack_rolls_str} = {attack_total}\n"
            f"{active_char.weapon.damage_type}: {damage_message}: {damage_rolls_str} = {damage_total}")
        
    @commands.command(name="skill", help="Rolls a skill check based on active character modifiers and attributes. Usage: !skill <Skill>")
    async def skill_check(self, ctx, char_skill:str):
        char_skill = char_skill.title()

        active_char = self.get_active_character(ctx)
        if active_char is None:
            return await ctx.send(f'No active character found. Activate one using `!activate "<characte_name>"`')
        
        skill_att = get_skill_attribute(char_skill)
        ability_score = getattr(active_char, skill_att)
        proficiency = active_char.skills.get(char_skill,"N")
        proficiency_mod = get_proficiency_bonus(active_char.level)

        if proficiency == "E":
            proficiency_mod *= 2
        elif proficiency == "N":
            proficiency_mod = 0
        
        skill_roll, skill_total, skill_message = roll_d20_dice(ability_score, RollType.NORMAL, proficiency_mod, skill=True)
        skill_rolls_str = ', '.join([str(roll) for roll in skill_roll])

        await ctx.send(f"{active_char.name} {char_skill} check: {skill_message}: {skill_rolls_str} = {skill_total}")

    @commands.command(name="equip", help='Equips a weapon from active\'s character inventory. Usage: !equip "<Weapon name>"')
    async def equip_weapon(self, ctx, weapon_name:str):
        active_char = self.get_active_character(ctx)
        if active_char is None:
            return await ctx.send(f'No active character found. Activate one using `!activate "<characte_name>"`')
        
        new_weapon = get_weapon(weapon_name.title())
        if new_weapon is None:
            return await ctx.send(f'Could not find weapon: {weapon_name.title()} in the available options')
            
        active_char.weapon = new_weapon
        await ctx.send(f"{active_char.name} equiped {new_weapon.name}!")

async def setup(bot):
    await bot.add_cog(PlayerCommands(bot))
