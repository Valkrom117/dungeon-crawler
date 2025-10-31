#character_commands.py

import discord
import sqlite3
import asyncio

from dnd_data_utils import *
from discord.ext import commands
from character import Character

DND_SKILLS = get_skills()
DND_CLASSES = get_classes()

class CharacterCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('characters.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                owner_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                char_class TEXT,
                level INTEGER,
                subclass TEXT,
                strength INTEGER,
                dexterity INTEGER,
                constitution INTEGER,
                wisdom INTEGER,
                intelligence INTEGER,
                charisma INTEGER,
                PRIMARY KEY (owner_id, name)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                owner_id INTEGER NOT NULL,
                char_name TEXT NOT NULL,
                skill_name TEXT NOT NULL,
                proficiency_level TEXT,
                
                PRIMARY KEY (owner_id, char_name, skill_name),
                FOREIGN KEY (owner_id, char_name) REFERENCES characters (owner_id, name)
            )
        ''')
        self.conn.commit()

    def cog_unload(self):
        self.conn.close()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if ctx.cog != self:
            return
        
        if isinstance(error, commands.MissingRequiredArgument):
            command_help = ctx.command.help.split('\n')[0]
            await ctx.send(
                f"Missing Parameter! You missed the `{error.param.name}` argument for `!{ctx.command.name}`.\n"
                f"Usage: {command_help}"
            )
            return
        
        if isinstance(error, commands.BadArgument):
            await ctx.send(
                f"Invalid Input Type! One of your parameters for `!{ctx.command.name}` was the wrong type.\n"
                f"Please check the command syntax."
            )
            return
        
        if isinstance(error, commands.TooManyArguments):
            await ctx.send(
                f"Too many arguments! If you are using a skill or subclass name with spaces, "
                f"please enclose the entire name in quotation marks."
            )
            return
        
        print(f"An unhandled error occurred in {ctx.command.name}: {error}")

    @commands.command(name='create_character', help='Creates and saves a character. Usage: !create_character <name> <level> \"<class>\" [\"<subclass>\"]')
    async def create_character(self, ctx, char_name, level: int, char_class, subclass=None):
        owner_id = ctx.author.id

        subclass = subclass.lower() if subclass else None

        if not validate_class(char_class):
            await ctx.send(f"Invalid character class: {char_class}. Valid classes are: {DND_CLASSES}")
            return

        if not validate_subclass(char_class, subclass) and subclass:
            official_class_name = char_class.title()           
            valid_subclasses = get_subclasses(char_class)
            valid_subclasses = [item.lower() for item in valid_subclasses]
            
            if subclass not in valid_subclasses:
                valid_subclasses = ", ".join(valid_subclasses)
                await ctx.send(
                    f"Invalid subclass: {subclass} for {official_class_name}."
                    f"Valid subclasses are: {valid_subclasses}"
                )
                return

        char_name = char_name.title()
        char_class = char_class.title()
        if subclass: subclass = subclass.title()
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO characters 
                (owner_id, name, char_class, level, subclass, strength, dexterity, constitution, wisdom, intelligence, charisma)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (owner_id, char_name, char_class, level, subclass, 0, 0, 0, 0, 0, 0))
            
            self.conn.commit()

            await ctx.send(f"Character {char_name}, level {level} {subclass or None} {char_class} created and saved!")

        except sqlite3.Error as e:
            await ctx.send(f"An error occurred while saving the character: {e}")

    @commands.command(name="update_stats", help="Updates all 6 ability scores (STR, DEX, CON, WIS, INT, CHA). Usage: !update_stats <char_name> <STR> <DEX> <CON> <WIS> <INT> <CHA>")
    async def update_stats(self, ctx, char_name, strength: int, dexterity: int, constitution: int, wisdom: int, intelligence: int, charisma: int):
        owner_id = ctx.author.id
        char_name = char_name.title()

        self.cursor.execute('SELECT owner_id FROM characters WHERE owner_id = ? AND name = ?', (owner_id, char_name))
        if self.cursor.fetchone() is None:
            await ctx.send(f"Character '{char_name}' not found. Use `!create_character` first or check the name.")
            return
        try:
            self.cursor.execute('''
                UPDATE characters
                SET strength = ?, dexterity = ?, constitution = ?, wisdom = ?, intelligence = ?, charisma = ?
                WHERE owner_id = ? AND name = ?
            ''', (strength, dexterity, constitution, wisdom, intelligence, charisma, owner_id, char_name))
            
            self.conn.commit()

            await ctx.send(
                f"{char_name}'s ability scores updated successfully:\n"
                f"STR:{strength}, DEX:{dexterity}, CON:{constitution}, WIS:{wisdom}, INT:{intelligence}, CHA:{charisma}"
            )

        except sqlite3.Error as e:
            print(f"Database error during update: {e}")
            await ctx.send(f"An error occurred while updating stats: {e}")

    @commands.command(name="update_skill", help="Sets proficiency level for a skill on a specific character")
    async def update_skill(self, ctx, char_name: str, skill_name: str, proficiency_level: str):
        owner_id = ctx.author.id
        char_name = char_name.title()
        skill_name = skill_name.title()
        proficiency_level = proficiency_level.upper()

        if proficiency_level not in ('N', 'P', 'E'):
            await ctx.send("Invalid proficiency level. Use 'N' (None), 'P' (Proficient), or 'E' (Expertise).")
            return
        
        if skill_name.lower() not in [item.lower() for item in DND_SKILLS]:
            skill_list_str = ", ".join(sorted(DND_SKILLS))
            await ctx.send(
                f"**Invalid Skill Name!** The skill '**{skill_name}**' does not exist in the official list. "
                f"Valid skills are: {skill_list_str}"
            )
            return
        
        self.cursor.execute('SELECT owner_id FROM characters WHERE owner_id = ? AND name = ?', (owner_id, char_name))
        if self.cursor.fetchone() is None:
            await ctx.send(f"Character '{char_name}' not found. Use `!create_character` first or check the name.")
            return

        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO skills 
                (owner_id, char_name, skill_name, proficiency_level)
                VALUES (?, ?, ?, ?)
            ''', (owner_id, char_name, skill_name, proficiency_level ))

            self.conn.commit()

            await ctx.send(f"Character {char_name}'s skill {skill_name} proficiency set to {proficiency_level}.")

        except sqlite3.Error as e:
            print(f"Database error during proficiency update: {e}")
            await ctx.send(f"An error occurred while setting proficiency: {e}")

    @commands.command(name='character', help='Shows your saved character.')
    async def view_character(self, ctx, char_name = None):
        owner_id = ctx.author.id
        if char_name is None or char_name.lower() == 'list':
            self.cursor.execute(
                'SELECT name, level, char_class, subclass FROM characters WHERE owner_id = ?',
                (owner_id,)
            )
            all_chars = self.cursor.fetchall()
            if not all_chars:
                return await ctx.send("You haven't created any characters yet! Use `!create_character <name> <level> <class> [subclass]`.")
            
            list_output = f"**{ctx.author.display_name}'s Characters:**\n"
            for char_name_iter, level, char_class, subclass in all_chars:
                list_output += f"- {char_name_iter}: Level {level} {subclass or 'No Subclass'} {char_class}\n"
            return await ctx.send(list_output)

        char_name = char_name.title()
        self.cursor.execute(
            'SELECT name, level, char_class, subclass, strength, dexterity, constitution, wisdom, intelligence, charisma FROM characters WHERE owner_id = ? and name = ?', 
            (owner_id, char_name)
        )
        data = self.cursor.fetchone()

        if data is None:
            return await ctx.send(f"Character '{char_name}' not found. Use `!character list` to see your saved characters.")
        
        name, level, char_class, subclass, str_s, dex_s, con_s, wis_s, int_s, cha_s = data

        self.cursor.execute(
            'SELECT skill_name, proficiency_level FROM skills WHERE owner_id = ? AND char_name = ? ORDER BY skill_name',
            (owner_id, name) 
        )

        skills_data = self.cursor.fetchall()
        skill_list = []
        skill_list_str = ""
        if skills_data:
            for skill_name, prof_level in skills_data:
                skill_list.extend([f"{skill_name}: {prof_level}"])
            skill_list_str = ", ".join(skill_list)
        else:
            skill_list_str += "No skills set. Use `!update_skill`."

        features = get_character_features(level, char_class)
        features_list = ""
        for feature in features.split(","):
            features_list += f"- {feature}\n"

        output = (
            f"**{name}**\n"
            f"Level {level} {subclass or 'No Subclass'} {char_class} \n\n"
            f"Ability Scores:\n"
            f"STR: {str_s}, DEX: {dex_s}, CON: {con_s}, WIS: {wis_s}, INT: {int_s}, CHA: {cha_s}\n\n"
            f"Skills:\n"
            f"{skill_list_str}\n\n"
            f"Features:\n"
            f"{features_list}"
        )
        await ctx.send(output)
       
    @commands.command(name="delete_character", help="Deletes a character and all related data. Usage: !delete_character <char_name>")
    async def delete_character(self, ctx, char_name: str):
        owner_id = ctx.author.id
        char_name = char_name.title()

        self.cursor.execute(
            'SELECT name FROM characters WHERE owner_id = ? and name = ?', 
            (owner_id, char_name)
        )
        if self.cursor.fetchone() is None:
            await ctx.send(f"Character '{char_name}' not found among your saved characters.")
            return
        
        await ctx.send(
            f"WARNING: You are about to permanently delete the character **{char_name}** and all associated skill data. \n\n"
            f"To confirm, reply with `delete` within 30 seconds."
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == 'delete'

        try:
            await self.bot.wait_for('message', check=check, timeout=30.0)
            try:

                self.cursor.execute(
                    'DELETE FROM skills WHERE owner_id = ? AND char_name = ?',
                    (owner_id, char_name)
                )
                self.cursor.execute(
                    'DELETE FROM characters WHERE owner_id = ? AND name = ?',
                    (owner_id, char_name)
                )
                self.conn.commit()
                await ctx.send(f"Successfully deleted character **{char_name}**.")

            except sqlite3.Error as e:
                self.conn.rollback()
                print(f"Database error during deletion: {e}")
                await ctx.send(f"An error occurred while deleting {char_name}: {e}. Deletion rolled back.")

        except asyncio.TimeoutError:
            # 5. Timeout - Cancellation
            await ctx.send(f"Deletion of **{char_name}** cancelled due to timeout (30 seconds elapsed).")

async def setup(bot):
    await bot.add_cog(CharacterCommands(bot))