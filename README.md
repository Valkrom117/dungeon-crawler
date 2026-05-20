# Dungeon Crawler Discord Bot

A Python-based Discord bot for Dungeons & Dragons (5e) character creation, management, and gameplay mechanics.

This is a personal project for boot.dev.

## Features

- **Character Management:** Create and store D&D characters, including classes, subclasses, attributes, and skills.
- **Gameplay Mechanics:** Set an active character to perform skill checks, equip weapons, and roll attacks/damage.
- **Dice Rolling:** Built-in command for arbitrary dice rolls.
- **Database Persistence:** Character data is safely stored in a database (SQLite).

## Setup and Installation

1. Clone the repository.
2. Install the required dependencies (`discord.py` and `python-dotenv`):
   ```bash
   pip install discord.py python-dotenv
   ```
3. Create a `.env` file in the root directory and add your Discord Bot Token:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

## Bot Commands

### Character Commands
- `!create <name> <level> "<class>" ["<subclass>"]` - Creates and saves a new character.
- `!attributes <char_name> <STR> <DEX> <CON> <WIS> <INT> <CHA>` - Updates all 6 ability scores.
- `!set_skill <char_name> <skill_name> <proficiency_level>` - Sets skill proficiency ('N' for None, 'P' for Proficient, or 'E' for Expertise).
- `!character [char_name | list]` - Shows a specific saved character's sheet or lists all your characters.
- `!delete <char_name>` - Permanently deletes a character (requires replying with `delete` within 30 seconds).
- `!activate <char_name>` - Sets a character as active for gameplay commands.

### Player Gameplay Commands
- `!attack` - Rolls an attack and damage based on the active character's equipped weapon and strength.
- `!skill <Skill>` - Rolls a skill check based on the active character's modifiers and proficiency.
- `!equip "<Weapon name>"` - Equips a weapon to your active character.

### Dice Commands
- `!roll <number_of_dice> <number_of_sides>` - Simulates rolling custom dice (e.g., `!roll 2 20`).
