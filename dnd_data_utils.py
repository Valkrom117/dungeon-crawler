# dnd_data_utils.py

import json

with open("dnd_rules.json", 'r') as file:
    DND_RULES_DATA = json.load(file)

with open("class_data.json", 'r') as file:
    DND_CLASS_DATA = json.load(file)

def get_skills():
    return list(DND_RULES_DATA["skill_to_ability"].keys())

def get_classes():
    return list(DND_CLASS_DATA.keys())

def get_subclasses(char_class: str):
    char_class = char_class.title()
    return list(DND_CLASS_DATA[char_class]["subclasses"])

def get_character_features(char_level, char_class: str, subclass=None):
    features_list = []
    char_class = char_class.title()
    for level in DND_CLASS_DATA[char_class]["class_progression"]:
        value = DND_CLASS_DATA[char_class]["class_progression"][level]
        if int(level) <= char_level: features_list.extend(value)
    return ", ".join(features_list)

def validate_class(char_class: str):
    char_class = char_class.lower()
    available_classes = get_classes()
    return char_class in [item.lower() for item in available_classes]

def validate_subclass(char_class: str, subclass: str):
    subclass = subclass.lower()
    available_subclasses = get_subclasses(char_class)
    return subclass in [item.lower() for item in available_subclasses]

def validate_skill(skill: str):
    skill = skill.lower()
    available_skills = get_skills()
    return skill not in [item.lower() for item in available_skills]