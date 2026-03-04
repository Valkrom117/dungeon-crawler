#character.py
from dataclasses import dataclass
from typing import Dict, Optional, List
from weapon import Weapon

@dataclass(kw_only=True) 
class Creature:
    name: int
    level: int
    
    armor_class: int = 0
    hit_points: int = 0

    strength: int = 0
    dexterity: int = 0
    constitution: int = 0
    wisdom: int = 0
    intelligence: int = 0
    charisma: int = 0

    skills: Dict[str, str] = None
    saving_throws: List[str] = None
    speeds: List[str] = None
    senses: List[str] = None
    immunities: List[str] = None

    def __post_init__(self):
        if self.skills is None:
            self.skills = {}
        if self.saving_throws is None:
            self.saving_throws = []
        if self.speeds is None:
            self.speeds = []
        if self.senses is None:
            self.senses = []
        if self.immunities is None:
            self.immunities = []

@dataclass(kw_only=True) 
class Character(Creature):
    owner: int

    char_class: str
    subclass: Optional[str] = None

    weapon: Optional[Weapon] = None

    def __post_init__(self):
        super().__post_init__()


@dataclass(kw_only=True) 
class NonPlayableCharacter(Creature):
    attack: Optional[Weapon] = None

    def __post_init__(self):
        super().__post_init__()