#character_commands.py

import asyncio

from class_utils import *
from rules_utils import *
from database_utils import *
from discord.ext import commands
from character import Character
from sqlite3 import IntegrityError


DND_SKILLS = get_skills()
DND_CLASSES = get_classes()
initialize_database()

class CharacterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def _get_player_cog(self):
        return self.bot.get_cog("PlayerCommands")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if ctx.cog != self:
            return
        
        if isinstance(error, commands.MissingRequiredArgument):
            command_help = ctx.command.help.split('\n')[0]
            return await ctx.send(
                f"Missing Parameter! You missed the `{error.param.name}` argument for `!{ctx.command.name}`.\n"
                f"Usage: {command_help}")
        
        if isinstance(error, commands.BadArgument):
            return await ctx.send(
                f"Invalid Input Type! One of your parameters for `!{ctx.command.name}` was the wrong type.\n"
                f"Please check the command syntax.")
            
        if isinstance(error, commands.TooManyArguments):
            return await ctx.send(
                f"Too many arguments! If you are using a skill or subclass name with spaces, "
                f"please enclose the entire name in quotation marks.")

    @commands.command(name='create', help='Creates and saves a character. Usage: !create <name> <level> \"<class>\" [\"<subclass>\"]')
    async def create(self, ctx, char_name, level: int, char_class, subclass=None):
        owner_id = ctx.author.id

        subclass = subclass.lower() if subclass else None

        if not validate_class(char_class):
            return await ctx.send(f"Invalid character class: {char_class}. Valid classes are: {DND_CLASSES}")
            
        valid_subclasses = ", ".join(get_subclasses(char_class))
        official_class_name = char_class.title()           
        if validate_subclass_required(level, char_class) and subclass == None:
            return await ctx.send(
                f"Current level for {char_class} requires a subclass."
                f"Valid subclasses are: {valid_subclasses}")
            
        if subclass and not validate_subclass(char_class, subclass) :
            return await ctx.send(
                f"Invalid subclass: {subclass} for {official_class_name}."
                f"Valid subclasses are: {valid_subclasses}")
            
        char_name = char_name.title()
        char_class = char_class.title()
        if subclass: subclass = subclass.title()
        try:
            create_new_character(owner_id, char_name, char_class, level, subclass)
            await ctx.send(f"Character {char_name}, level {level} {subclass or ""} {char_class} created and saved!")
        except IntegrityError:
            await ctx.send(f"Creation failed. You already have a character named **{char_name}**.")
        except Exception as e: 
            await ctx.send(f"An error occurred while saving the character {e}")

    @commands.command(name="attributes", help="Updates all 6 ability scores (STR, DEX, CON, WIS, INT, CHA). Usage: !attributes <char_name> <STR> <DEX> <CON> <WIS> <INT> <CHA>")
    async def attributes(self, ctx, char_name, strength: int, dexterity: int, constitution: int, wisdom: int, intelligence: int, charisma: int):
        owner_id = ctx.author.id
        char_name = char_name.title()

        if not check_character_exist(owner_id, char_name):
            return await ctx.send(f"Character '{char_name}' not found. Use `!create` first or check the name.")
            
        try:
            update_character_stats(owner_id, char_name, strength, dexterity, constitution, wisdom, intelligence, charisma)
            await ctx.send(
                f"{char_name}'s ability scores updated successfully:\n"
                f"STR:{strength}, DEX:{dexterity}, CON:{constitution}, WIS:{wisdom}, INT:{intelligence}, CHA:{charisma}")
        except Exception as e:
            await ctx.send(f"An error occurred while updating stats: {e}")

    @commands.command(name="set_skill", help="Sets proficiency level for a skill on a specific character")
    async def set_skill(self, ctx, char_name: str, skill_name: str, proficiency_level: str):
        owner_id = ctx.author.id
        char_name = char_name.title()
        skill_name = skill_name.title()
        proficiency_level = proficiency_level.upper()

        if proficiency_level not in ('N', 'P', 'E'):
            return await ctx.send("Invalid proficiency level. Use 'N' (None), 'P' (Proficient), or 'E' (Expertise).")
            
        if skill_name.lower() not in [item.lower() for item in DND_SKILLS]:
            skill_list_str = ", ".join(sorted(DND_SKILLS))
            return await ctx.send(
                f"**Invalid Skill Name!** The skill '**{skill_name}**' does not exist in the official list. "
                f"Valid skills are: {skill_list_str}")

        if not check_character_exist(owner_id, char_name):
            return await ctx.send(f"Character '{char_name}' not found. Use `!create` first or check the name.")
            
        try:
            set_character_skill(owner_id, char_name, skill_name, proficiency_level)
            await ctx.send(f"Character {char_name}'s skill {skill_name} proficiency set to {proficiency_level}.")
        except Exception as e:
            await ctx.send(f"An error occurred while setting proficiency: {e}")

    @commands.command(name='character', help='Shows your saved character.')
    async def view_character(self, ctx, char_name = None):
        owner_id = ctx.author.id
        if char_name is None or char_name.lower() == 'list':
            all_chars = get_all_characters(owner_id)
            if not all_chars:
                return await ctx.send("You haven't created any characters yet! Use `!create <name> <level> <class> [subclass]`.")
            
            list_output = f"**{ctx.author.display_name}'s Characters:**\n"
            for char_name_iter, level, char_class, subclass in all_chars:
                list_output += f"- {char_name_iter}: Level {level} {subclass or ''} {char_class}\n"
            return await ctx.send(list_output)

        char_name = char_name.title()
        try:
            data = get_character_atributes(owner_id, char_name)

        except Exception as e:
            print(f"Error during get character <name> {e}")

        if data is None:
            return await ctx.send(f"Character '{char_name}' not found. Use `!character list` to see your saved characters.")
        
        name, level, char_class, subclass, ac, hp, str_s, dex_s, con_s, wis_s, int_s, cha_s = data

        skills_data = get_character_skills(owner_id, char_name)
        skill_list = []
        if skills_data:
            for skill_name, prof_level in skills_data:
                skill_list.extend([f"{skill_name}: {prof_level}"])
            skill_list_str = ", ".join(skill_list)
        else:
            skill_list_str = "No skills set. Use `!set_skill`."

        features = get_class_features(level, char_class)
        features_list = ""
        for feature in features.split(","):
            features_list += f"- {feature}\n"

        output = (
            f"**{name}**\n"
            f"Level {level} {subclass or ''} {char_class} \n"
            f"AC: {ac}, Max hit points: {hp} \n"
            f"Ability Scores:\n"
            f"STR: {str_s}, DEX: {dex_s}, CON: {con_s}, WIS: {wis_s}, INT: {int_s}, CHA: {cha_s}\n"
            f"Skills:\n"
            f"{skill_list_str}\n"
            f"Features:\n"
            f"{features_list}"
        )
        await ctx.send(output)
       
    @commands.command(name="delete", help="Deletes a character and all related data. Usage: !delete <char_name>")
    async def delete(self, ctx, char_name: str):
        owner_id = ctx.author.id
        char_name = char_name.title()

        try:
            if not check_character_exist(owner_id, char_name):
                return await ctx.send(f"Character '{char_name}' not found among your saved characters.")
        except Exception as e:
            print(f"Error during deletion: {e}")
            
        await ctx.send(
            f"WARNING: You are about to permanently delete the character **{char_name}** and all associated skill data. \n\n"
            f"To confirm, reply with `delete` within 30 seconds.")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == 'delete'

        try:
            await self.bot.wait_for('message', check=check, timeout=30.0)
            delete_character(owner_id, char_name)
            await ctx.send(f"Successfully deleted character **{char_name}**.")
        except asyncio.TimeoutError:
            await ctx.send(f"Deletion of **{char_name}** cancelled due to timeout (30 seconds elapsed).")

    @commands.command(name='activate', help='Activates a character for gameplay')
    async def activate(self, ctx, char_name: str):
        owner_id = ctx.author.id
        char_name = char_name.title()

        if not check_character_exist(owner_id, char_name):
            return await ctx.send(f"Character '{char_name}' not found among your saved characters.")
        try:
            set_active_character(owner_id, char_name)
            await ctx.send(f"Your character **{char_name}** is now active for gameplay")
            player_cog = self._get_player_cog()
            player_cog._sync_cache(owner_id, char_name)
        except Exception as e:
            print(f"Error during activation: {e}")
            return
        

async def setup(bot):
    await bot.add_cog(CharacterCommands(bot))