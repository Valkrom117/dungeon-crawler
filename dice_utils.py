# dice_utils.py

import math
import random
from constants import RollType

def roll_damage_dice(number_of_dice:int, number_of_sides:int, attribute:int = None, modifier:int = 0) -> tuple:

    dice = [random.choice(range(1, number_of_sides + 1)) for _ in range(number_of_dice)]

    if attribute: att_mod = math.floor((attribute-10)/2)
    else: att_mod = 0

    total = sum(dice) + att_mod + modifier
    message = f"{number_of_dice}d{number_of_sides}+{att_mod + modifier}"
    return dice, total, message

def roll_d20_dice(attribute:int, roll_mode: RollType, modifier:int = 0, skill:bool = False):
    number_of_dice = 2 if roll_mode != RollType.NORMAL else 1
    dice = [random.choice(range(1, 21)) for _ in range(number_of_dice)] 

    if roll_mode == RollType.ADVANTAGE:
        result = max(dice)
        rolltype_message = "(adv) "
    elif roll_mode == RollType.DISADVANTAGE:
        result = min(dice)
        rolltype_message = "(dis) "
    else:
        result = dice[0] 
        rolltype_message = ""
        
    att_mod = math.floor((attribute - 10) / 2)
    final_modifier = att_mod + modifier
    total = result + final_modifier

    message = f"{rolltype_message}d20 + {final_modifier}"
    if result == 20 and not skill: 
        message += " **Critical Hit!**"
    elif result == 1 and not skill:
        message += " **Miss!**"

    return dice, total, message

