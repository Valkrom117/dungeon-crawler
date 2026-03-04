# database_utils.py

import sqlite3

from constants import *

def execute_sql(sql_command:str, params:tuple = None, fetch_method:str = None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_command, params or ())
        if fetch_method == "one":
            data = cursor.fetchone()
            return data
        elif fetch_method == "all":
            data = cursor.fetchall()
            return data
        else:
            conn.commit()
            return True

    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def initialize_database():
    for sql in SQL_COMMANDS["INIT"]:
        execute_sql(sql)

def create_new_character(owner_id:int, char_name:str, char_class:str, level:int, subclass:str):
    params = (owner_id, char_name.title(), char_class, level, subclass)
    execute_sql(SQL_COMMANDS["CREATE_CHARACTER"], params)

def check_character_exist(owner_id:int, char_name:str):
    params = (owner_id, char_name.title())
    result = execute_sql(SQL_COMMANDS["CHARACTER_EXISTS"], params, "one") is not None
    return result

def update_character_stats(owner_id, char_name, strength, dexterity, constitution, wisdom, intelligence, charisma):
    params = (strength, dexterity, constitution, wisdom, intelligence, charisma, owner_id, char_name.title())
    execute_sql(SQL_COMMANDS["UPDATE_CHARACTER_ATTRIBUTES"], params)

def set_character_skill(owner_id:int, char_name:str, skill_name:str, proficiency_level:str ):
    params = (owner_id, char_name.title(), skill_name, proficiency_level )
    execute_sql(SQL_COMMANDS["SET_CHARACTER_SKILL"], params)

def get_all_characters(owner_id:int):
    params = (owner_id,)
    result = execute_sql(SQL_COMMANDS["GET_ALL_CHARACTERS"], params, "all")
    return result

def get_character_atributes(owner_id:int, char_name:str):
    params = (owner_id, char_name.title())
    result = execute_sql(SQL_COMMANDS["GET_CHARACTER_ATRIBUTES"], params, "one")
    return result

def get_character_skills(owner_id:int, char_name:str):
    params = (owner_id, char_name.title())
    result = execute_sql(SQL_COMMANDS["GET_CHARACTER_SKILLS"], params, "all")
    return result

def delete_character(owner_id:int, char_name:str):
    params = (owner_id, char_name.title())
    for sql in SQL_COMMANDS["DELETE_CHARACTER"]:
        execute_sql(sql, params)

def set_active_character(owner_id:int, char_name:str):
    params = (owner_id, char_name.title())
    execute_sql(SQL_COMMANDS["ACTIVATE_CHARACTER"], params)

def get_character_data(owner_id:int, char_name:str):
    core_data = get_character_atributes(owner_id, char_name)
    if core_data is None:
        return None
    skills = get_character_skills(owner_id, char_name)

    (name, level, char_class, subclass, armor_class, hit_points, strength, dexterity, constitution, 
     wisdom, intelligence, charisma) = core_data
    
    data = {
        "owner": owner_id,
        "name": name,
        "level": level,
        "char_class": char_class,
        "subclass": subclass,
        "armor_class": armor_class,
        "hit_points": hit_points,
        "strength": strength,
        "dexterity": dexterity,
        "constitution": constitution,
        "wisdom": wisdom,
        "intelligence": intelligence,
        "charisma": charisma,
    }
    data["skills"] = {name: prof for name, prof in skills}
    return data

def get_active_character_name(owner_id: int):
    params = (owner_id,)
    result = execute_sql(SQL_COMMANDS["GET_ACTIVE_CHARACTER"], params, "one")
    return result[0] if result else None
