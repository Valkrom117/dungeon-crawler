# rules_utils.py

import json
from weapon import Weapon

with open("weapon_data.json", 'r') as file:
    DND_WEAPONS_DATA = json.load(file)

def get_weapon(weapon_name: str) -> Weapon | None:
    weapon_dict = DND_WEAPONS_DATA.get(weapon_name.title())
    if weapon_dict is None:
        return None
    
    weapon_dict["name"] = weapon_name.title()
    return Weapon(**weapon_dict)
