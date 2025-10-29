"""
COMP 163 - Project 1: Character Creator & Saving/Loading
Name: Christopher Early
Date: 10/26/2025

AI Usage: AI helped me make the code/program as advanced as it is. I created a basic code format similar to the assignment we had done in the past, and told the AI to add whatever parameters I wanted, such as a advanced system class and gold system, and it changed/added to my code to fit the criteria I wanted, and that the project instructions demanded. I then document all the changes to be able to properly explain them.
Example: AI helped with file I/O error handling logic in save_character function
"""

# project1_starter.py
import os
import random

CLASS_DEFINITIONS = {
    "Warrior": {
        "desc": "A battle-hardened fighter who relies on brute strength and endurance.",
        "base": {"strength": 15, "magic": 3, "health": 120},
        "growth": {"strength": 3, "magic": 0.5, "health": 20},
        "weapon": "Longsword",
        "equipment": ["Chainmail", "Shield"],
        "abilities": ["Power Strike", "Taunt"]
    },
    "Mage": {
        "desc": "A scholar of the arcane: fragile in body but terrifying with spells.",
        "base": {"strength": 4, "magic": 18, "health": 80},
        "growth": {"strength": 0.5, "magic": 4, "health": 10},
        "weapon": "Oak Staff",
        "equipment": ["Robes", "Spellbook"],
        "abilities": ["Fireball", "Arcane Shield"]
    },
    "Rogue": {
        "desc": "A nimble opportunist who relies on speed, stealth, and precision.",
        "base": {"strength": 10, "magic": 7, "health": 85},
        "growth": {"strength": 1.8, "magic": 1.2, "health": 8},
        "weapon": "Dagger",
        "equipment": ["Leather Armor", "Lockpicks"],
        "abilities": ["Backstab", "Evade"]
    },
    "Cleric": {
        "desc": "A holy guardian who blends healing magic with sturdy defenses.",
        "base": {"strength": 9, "magic": 14, "health": 110},
        "growth": {"strength": 1.5, "magic": 2.8, "health": 16},
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
    return strength, magic, health


def create_character(name, character_class):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Name must be a non-empty string.")

    cls = character_class.capitalize()
    if cls not in CLASS_DEFINITIONS:
        raise ValueError(f"Unknown class '{character_class}'. Choose from: {list(CLASS_DEFINITIONS.keys())}")

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


def save_character(character, filename):
    try:
        dirpath = os.path.dirname(filename)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
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
            data[key.strip()] = val.strip()

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
        strength, magic, health = calculate_stats(character["class"], new_level)
    except Exception:
        strength = int(character.get("strength", 5) + 2)
        magic = int(character.get("magic", 2) + 1)
        health = int(character.get("health", 10) + 10)

    character["strength"] = strength
    character["magic"] = magic
    character["health"] = health

    character["xp"] = max(0, character.get("xp", 0) - character.get("xp_to_next", 100))
    character["xp_to_next"] = int(round(character.get("xp_to_next", 100) * 1.35))

    gold_reward = LEVEL_UP_GOLD_BASE + random.randint(0, 20)
    character["gold"] = int(character.get("gold", 0) + gold_reward)

    if character.get("abilities") and new_level in (3, 5, 10):
        new_ability = f"Advanced {random.choice(character['abilities'])}" if character['abilities'] else "New Skill"
        character["abilities"].append(new_ability)
    return None


if __name__ == "__main__":
    print("=== CHARACTER CREATOR DEMO ===")
    player_name = input("Enter your character's name: ").strip() or "Hero"
    print("\nChoose your class:")
    for c in CLASS_DEFINITIONS:
        print(f"- {c}")
    player_class = input("\nEnter class name: ").capitalize()
    if player_class not in CLASS_DEFINITIONS:
        print("Invalid class. Defaulting to Warrior.")
        player_class = "Warrior"

    char = create_character(player_name, player_class)
    display_character(char)
    save_character(char, f"{player_name.lower()}_save.txt")
