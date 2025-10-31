#character.py
class Character ():
    def __init__ (self, owner, name, char_class, level, subclass=None,
                  strength = 0, dexterity = 0, constitution = 0, wisdom = 0, intelligence = 0, charisma = 0):
        self.name = name
        self.char_class = char_class
        self.level = level
        self.subclass = subclass
        self.owner = owner
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.wisdom = wisdom
        self.intelligence = intelligence
        self.charisma = charisma


    def __repr__(self):
        return f"Character:{self.name}\n, level {self.level} {self.char_class}, {self.subclass}"