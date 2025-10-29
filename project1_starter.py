"""
COMP 163 - Project 1: Character Creator & Saving/Loading
Name: Christopher Early
Date: 10/26/2025

AI Usage: AI helped me make the code/program as advanced as it is. I created a basic code format similar to the assignment we had done in the past, and told the AI to add whatever parameters I wanted, such as a advanced system class and gold system, and it changed/added to my code to fit the criteria I wanted, and that the project instructions demanded. I then document all the changes to be able to properly explain them. AI also greatly helped me properly create file systems and operations in order to pass the test cases.
"""

# project1_starter.py
import os
import random
CLASS_DEFINITIONS = {
    "Warrior": {
        "desc": "A battle-hardened fighter who relies on brute strength and endurance.",
        "base": {"strength": 15, "magic": 3, "health": 120, "agility": 8, "defense": 12, "mana": 5},
        "growth": {"strength": 3, "magic": 0.5, "health": 20, "agility": 1, "defense": 2, "mana": 0.5},
        "weapon": "Longsword",
        "equipment": ["Chainmail", "Shield"],
        "abilities": ["Power Strike", "Taunt"]
    },
    "Mage": {
        "desc": "A scholar of the arcane: fragile in body but terrifying with spells.",
        "base": {"strength": 4, "magic": 18, "health": 80, "agility": 7, "defense": 5, "mana": 40},
        "growth": {"strength": 0.5, "magic": 4, "health": 10, "agility": 0.8, "defense": 0.6, "mana": 8},
        "weapon": "Oak Staff",
        "equipment": ["Robes", "Spellbook"],
        "abilities": ["Fireball", "Arcane Shield"]
    },
    "Rogue": {
        "desc": "A nimble opportunist who relies on speed, stealth, and precision.",
        "base": {"strength": 10, "magic": 7, "health": 85, "agility": 16, "defense": 7, "mana": 10},
        "growth": {"strength": 1.8, "magic": 1.2, "health": 8, "agility": 3, "defense": 0.9, "mana": 2},
        "weapon": "Dagger",
        "equipment": ["Leather Armor", "Lockpicks"],
        "abilities": ["Backstab", "Evade"]
    },
    "Cleric": {
        "desc": "A holy guardian who blends healing magic with sturdy defenses.",
        "base": {"strength": 9, "magic": 14, "health": 110, "agility": 6, "defense": 10, "mana": 30},
        "growth": {"strength": 1.5, "magic": 2.8, "health": 16, "agility": 0.7, "defense": 1.8, "mana": 6},
        "weapon": "Mace",
        "equipment": ["Scale Armor", "Holy Symbol"],
        "abilities": ["Heal", "Smite"]
    }
}
BASE_GOLD = {
    "Warrior": 120,
    "Mage": 100,
    "Rogue": 140,
    "Cleric": 110
}
LEVEL_UP_GOLD_BASE = 30

def calculate_stats(character_class, level):
    cls = character_class.capitalize()
    if cls not in CLASS_DEFINITIONS:
        raise ValueError(f"Unknown class '{character_class}'. Valid classes: {list(CLASS_DEFINITIONS.keys())}")
    definition = CLASS_DEFINITIONS[cls]
    base = definition["base"]
    growth = definition["growth"]
    level_offset = max(1, int(level)) - 1
    strength = int(round(base["strength"] + growth["strength"] * level_offset))
    magic = int(round(base["magic"] + growth["magic"] * level_offset))
    health = int(round(base["health"] + growth["health"] * level_offset))
    return (strength, magic, health)


def create_character(name, character_class):
    if not isinstance(name, str) or not name.strip():
        print("Invalid name provided. Using default name 'Unknown Hero'.")
        name = "Unknown Hero"
    cls = character_class.capitalize()
    if cls not in CLASS_DEFINITIONS:
        print(f"Unknown class '{character_class}'. Defaulting to Warrior.")
        cls = "Warrior"

    level = 1
    strength, magic, health = calculate_stats(cls, level)
    random.seed()
    base_gold = BASE_GOLD.get(cls, 100)
    gold_variance = random.randint(-10, 25)
    gold = max(0, base_gold + gold_variance)
    definition = CLASS_DEFINITIONS[cls]
    pathways = {
        "Warrior": ["Guardian", "Berserker"],
        "Mage": ["Elementalist", "Scholar"],
        "Rogue": ["Assassin", "Scout"],
        "Cleric": ["Apostle", "Templar"]
    }
    pathways = {
        "Warrior": ["Guardian", "Berserker"],
        "Mage": ["Elementalist", "Scholar"],
        "Rogue": ["Assassin", "Scout"],
        "Cleric": ["Apostle", "Templar"]
    }
    pathway = random.choice(pathways.get(cls, ["Adventurer"]))
    if cls == "Warrior":
        origin = "blacksmith's apprentice"
        interest = "battle"
    elif cls == "Mage":
        origin = "library's ward"
        interest = "arcane mysteries"
    elif cls == "Rogue":
        origin = "street urchin"
        interest = "shadows and quick gains"
    else:
        origin = "temple acolyte"
        interest = "healing the wounded"
    backstory = (
        f"{name} grew up as a {origin} and chose the path of the {cls.lower()}. "
        f"As a {pathway}, {name} has always been drawn to {interest}."
    )

    character = {
        "name": name,
        "class": cls,
        "level": level,
        "strength": strength,
        "magic": magic,
        "health": health,
        "gold": gold,
        "weapon": definition["weapon"],
        "equipment": list(definition["equipment"]),
        "abilities": list(definition["abilities"]),
        "pathway": pathway,
        "backstory": backstory,
        "xp": 0,
        "xp_to_next": 100
    }
    return character
import os

def save_character(character, filename):
    dirpath = os.path.dirname(filename)
    if (
        (dirpath and not os.path.isdir(dirpath))
        or filename.startswith("/")
        or filename.startswith("\\")
    ):
        print(f"Invalid directory path: {filename}")
        return False
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Character Name: {character['name']}\n\n")
            f.write(f"Class: {character['class']}\n\n")
            f.write(f"Level: {character['level']}\n\n")
            f.write(f"Strength: {character['strength']}\n\n")
            f.write(f"Magic: {character['magic']}\n\n")
            f.write(f"Health: {character['health']}\n\n")
            f.write(f"Gold: {character['gold']}\n")
        return True
    except Exception as e:
        print(f"Error saving character to '{filename}': {e}")
        return False


def load_character(filename):
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        data = {}
        for line in lines:
            if ":" not in line:
                continue
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            data[key] = val
        required = ["Character Name", "Class", "Level", "Strength", "Magic", "Health", "Gold"]
        if not all(k in data for k in required):
            print(f"Save file '{filename}' missing required fields.")
            return None
        character = {
            "name": data["Character Name"],
            "class": data["Class"],
            "level": int(data["Level"]),
            "strength": int(data["Strength"]),
            "magic": int(data["Magic"]),
            "health": int(data["Health"]),
            "gold": int(data["Gold"])
        }
        try:
            strength, magic, health, agility, defense, mana = calculate_stats(character["class"], character["level"])
            character.setdefault("agility", agility)
            character.setdefault("defense", defense)
            character.setdefault("mana", mana)
        except Exception:
            pass
        cls = character["class"].capitalize()
        if cls in CLASS_DEFINITIONS:
            definition = CLASS_DEFINITIONS[cls]
            character.setdefault("weapon", definition["weapon"])
            character.setdefault("equipment", list(definition["equipment"]))
            character.setdefault("abilities", list(definition["abilities"]))
            character.setdefault("pathway", "Unknown")
            character.setdefault("backstory", "")
            character.setdefault("xp", 0)
            character.setdefault("xp_to_next", 100)
        return character
    except Exception as e:
        print(f"Error loading character from '{filename}': {e}")
        return None
def display_character(character):
    print("=== CHARACTER SHEET ===")
    print(f"Name: {character.get('name', 'Unknown')}")
    print(f"Class: {character.get('class', 'Unknown')}")
    print(f"Level: {character.get('level', 'Unknown')}")
    print(f"Strength: {character.get('strength', 'Unknown')}")
    print(f"Magic: {character.get('magic', 'Unknown')}")
    print(f"Health: {character.get('health', 'Unknown')}")
    print(f"Gold: {character.get('gold', 0)}")
    if any(key in character for key in ("agility", "defense", "mana")):
        print("--- Extra Stats ---")
        print(f"Agility: {character.get('agility', 'N/A')}")
        print(f"Defense: {character.get('defense', 'N/A')}")
        print(f"Mana: {character.get('mana', 'N/A')}")
    weapon = character.get("weapon")
    equipment = character.get("equipment")
    abilities = character.get("abilities")
    if weapon or equipment:
        print("--- Equipment ---")
        if weapon:
            print(f"Weapon: {weapon}")
        if equipment:
            print(f"Gear: {', '.join(equipment)}")
    if abilities:
        print("--- Abilities ---")
        print(", ".join(abilities))
    pathway = character.get("pathway")
    backstory = character.get("backstory")
    if pathway:
        print(f"Pathway: {pathway}")
    if backstory:
        print("--- Backstory ---")
        print(backstory)
    xp = character.get("xp")
    xp_to_next = character.get("xp_to_next")
    if xp is not None and xp_to_next is not None:
        print(f"XP: {xp}/{xp_to_next}")
    print("=======================")
def level_up(character):
    if "level" not in character:
        raise ValueError("Character missing 'level' field; cannot level up.")
    old_level = int(character["level"])
    new_level = old_level + 1
    character["level"] = new_level
    try:
        strength, magic, health, agility, defense, mana = calculate_stats(character["class"], new_level)
    except Exception:
        strength = int(character.get("strength", 5) + 2)
        magic = int(character.get("magic", 2) + 1)
        health = int(character.get("health", 10) + 10)
        agility = int(character.get("agility", 5) + 1)
        defense = int(character.get("defense", 5) + 1)
        mana = int(character.get("mana", 0) + 2)
    bump = lambda x: int(round(x + random.choice([0, 0, 1])))
    character["strength"] = bump(strength)
    character["magic"] = bump(magic)
    character["health"] = bump(health)
    character["agility"] = bump(agility)
    character["defense"] = bump(defense)
    character["mana"] = bump(mana)
    xp = character.get("xp", 0)
    xp_to_next = character.get("xp_to_next", 100)
    xp -= xp_to_next
    xp = max(0, xp)
    character["xp"] = xp
    character["xp_to_next"] = int(round(xp_to_next * 1.35))
    gold_reward = LEVEL_UP_GOLD_BASE + random.randint(0, 20)
    character["gold"] = int(character.get("gold", 0) + gold_reward)
    if character.get("abilities") is not None:
        if new_level in (3, 5, 10):
            new_ability = f"Advanced {random.choice(character['abilities'])}" if character['abilities'] else "New Skill"
            character["abilities"].append(new_ability)
    return None
if __name__ == "__main__":
    print("=== Welcome to the Character Creator ===")
    name = input("Enter your character's name: ").strip()
    print("\nChoose your class:")
    for cls in CLASS_DEFINITIONS.keys():
        print(f"- {cls}: {CLASS_DEFINITIONS[cls]['desc']}")
    while True:
        chosen_class = input("\nEnter your class choice: ").capitalize().strip()
        if chosen_class in CLASS_DEFINITIONS:
            break
        print("Invalid class. Please choose one of the listed options.")
    player = create_character(name, chosen_class)
    display_character(player)
    save_name = f"{name.lower()}_save.txt"
    save_success = save_character(player, save_name)
    print(f"\nCharacter saved to {save_name}: {save_success}")

