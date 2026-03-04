# constants.py

from enum import Enum

class RollType(Enum):
    ADVANTAGE = 1
    DISADVANTAGE = 2
    NORMAL = 3

DATABASE = "characters.db"
SQL_COMMANDS = {
    "INIT": [
        'PRAGMA foreign_keys = ON;',
        '''CREATE TABLE IF NOT EXISTS characters (
            owner_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            level INTEGER,
            char_class TEXT,
            subclass TEXT,
            armor_class INTEGER DEFAULT 0,
            hit_points INTEGER DEFAULT 0,
            strength INTEGER DEFAULT 0,
            dexterity INTEGER DEFAULT 0,
            constitution INTEGER DEFAULT 0,
            wisdom INTEGER DEFAULT 0,
            intelligence INTEGER DEFAULT 0,
            charisma INTEGER DEFAULT 0,
            saving_throws TEXT,
            speeds TEXT,
            senses TEXT,
            immunities TEXT,
            resistances TEXT,
            conditions TEXT,
            PRIMARY KEY (owner_id, name))''',
        '''CREATE TABLE IF NOT EXISTS skills (
            owner_id INTEGER NOT NULL,
            char_name TEXT NOT NULL,
            skill_name TEXT NOT NULL,
            proficiency_level TEXT,
            PRIMARY KEY (owner_id, char_name, skill_name),
            FOREIGN KEY (owner_id, char_name) REFERENCES characters (owner_id, name))''',
        '''CREATE TABLE IF NOT EXISTS active_character (
            owner_id INTEGER PRIMARY KEY,
            char_name TEXT NOT NULL)'''
    ],
    "CREATE_CHARACTER": "INSERT INTO characters (owner_id, name, char_class, level, subclass) VALUES (?, ?, ?, ?, ?)",
    "CHARACTER_EXISTS": "SELECT 1 FROM characters WHERE owner_id = ? AND name = ?",
    "UPDATE_CHARACTER_ATTRIBUTES": "UPDATE characters SET strength = ?, dexterity = ?, constitution = ?, wisdom = ?, intelligence = ?, charisma = ? WHERE owner_id = ? AND name = ?",
    "SET_CHARACTER_SKILL": "INSERT OR REPLACE INTO skills (owner_id, char_name, skill_name, proficiency_level) VALUES (?, ?, ?, ?)",
    "GET_ALL_CHARACTERS" : "SELECT name, level, char_class, subclass FROM characters WHERE owner_id = ?",
    "GET_CHARACTER_ATRIBUTES": "SELECT name, level, char_class, subclass, armor_class, hit_points, strength, dexterity, constitution, wisdom, intelligence, charisma FROM characters WHERE owner_id = ? and name = ?",
    "GET_CHARACTER_SKILLS": 'SELECT skill_name, proficiency_level FROM skills WHERE owner_id = ? AND char_name = ? ORDER BY skill_name',
    "DELETE_CHARACTER": ['DELETE FROM active_character WHERE owner_id = ? AND char_name = ?', 'DELETE FROM skills WHERE owner_id = ? AND char_name = ?', 'DELETE FROM characters WHERE owner_id = ? AND name = ?'],
    "ACTIVATE_CHARACTER": "INSERT OR REPLACE INTO active_character (owner_id, char_name) VALUES (?, ?)",
    "GET_ACTIVE_CHARACTER": "SELECT char_name FROM active_character WHERE owner_id = ?",
}