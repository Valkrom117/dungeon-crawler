#weapon.py
from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class Weapon:
    name: str
    type: str 
    dice_sides: int = 0
    dice_amount: int = 0
    damage_type: str = "None"
    range: str = "5 ft."
    cost: str = "0 cp"
    weight: float = 0.0
    properties: list[str] = field(default_factory=list)


