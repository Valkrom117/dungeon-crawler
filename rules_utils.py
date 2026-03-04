# rules_utils.py

import json

with open("dnd_rules.json", 'r') as file:
    DND_RULES_DATA = json.load(file)

def get_proficiency_bonus(level: int) -> int:
    level_str = str(level)
    return DND_RULES_DATA.get("proficiency_bonus", {}).get(level_str, 0)

def get_skills():
    return list(DND_RULES_DATA["skill_to_ability"].keys())

def get_skill_attribute(skill:int) -> str:
    return DND_RULES_DATA["skill_to_ability"][skill]