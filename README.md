# Dungeon Crawler Discord Bot

A Python-based Discord bot for Dungeons & Dragons (5e) character creation, management, and gameplay mechanics.

## Motivation

Many tabletop RPG players on Discord rely on generic dice rollers or bots confined to a single system, such as Avrae. The goal of this project is to provide a flexible foundation that allows users to customize their own systems or seamlessly use the ones they already know. Ultimately, it aims to facilitate playing TTRPGs with friends over the internet in a format that is less time-demanding than scheduling dedicated four-hour sessions each week, making it ideal for play-by-post or asynchronous campaigns.

I have participated in several communities that use play-by-post formats, and I noticed they often lose momentum due to the heavy setup and workload required on the GM's part. I created this bot to run my own play-by-post adventures with friends, providing a smoother experience by automating the parts of the game system I need to track.

## Quick Start

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

## Usage

### Features

- **Character Management:** Create and store D&D characters, including classes, subclasses, attributes, and skills.
- **Gameplay Mechanics:** Set an active character to perform skill checks, equip weapons, and roll attacks/damage.
- **Dice Rolling:** Built-in command for arbitrary dice rolls.
- **Database Persistence:** Character data is safely stored in a database (SQLite).

### Bot Commands

#### Character Commands
- `!create <name> <level> "<class>" ["<subclass>"]` - Creates and saves a new character. (e.g., `!create Bob 5 "Fighter" "Battle Master"`)
- `!attributes <char_name> <STR> <DEX> <CON> <WIS> <INT> <CHA>` - Updates all 6 ability scores. (e.g., `!attributes Bob 16 14 15 10 12 8`)
- `!set_skill <char_name> <skill_name> <proficiency_level>` - Sets skill proficiency ('N' for None, 'P' for Proficient, or 'E' for Expertise). (e.g., `!set_skill Bob Athletics P`)
- `!character [char_name | list]` - Shows a specific saved character's sheet or lists all your characters. (e.g., `!character Bob` or `!character list`)
- `!delete <char_name>` - Permanently deletes a character (requires replying with `delete` within 30 seconds). (e.g., `!delete Bob`)
- `!activate <char_name>` - Sets a character as active for gameplay commands. (e.g., `!activate Bob`)

#### Player Gameplay Commands
- `!attack` - Rolls an attack and damage based on the active character's equipped weapon and strength.
- `!skill <Skill>` - Rolls a skill check based on the active character's modifiers and proficiency. (e.g., `!skill Athletics`)
- `!equip "<Weapon name>"` - Equips a weapon to your active character. (e.g., `!equip "Longsword"`)

#### Dice Commands
- `!roll <number_of_dice> <number_of_sides>` - Simulates rolling custom dice (e.g., `!roll 2 20`).

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request if you'd like to help improve the project.

### How to Contribute

1. Fork the project repository on GitHub.
2. Clone your forked repository locally:
   ```bash
   git clone https://github.com/your-username/dungeon-crawler.git
   ```
3. Navigate to the project directory and create a new branch:
   ```bash
   cd dungeon-crawler
   git checkout -b feature/your-feature-name
   ```
4. Install the required dependencies:
   ```bash
   pip install discord.py python-dotenv
   ```
5. Create a `.env` file and add your Discord Bot Token for testing:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   ```
6. Run the bot to test your changes:
   ```bash
   python bot.py
   ```
7. Commit your changes, push your branch to your fork, and submit a pull request.
