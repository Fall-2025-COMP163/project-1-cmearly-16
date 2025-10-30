import os

def calculate_stats(char_class, level=1):
    """Return (strength, magic, health) for a given class and level."""
    if char_class == "Warrior":
        strength = 10 + 5 * level
        magic = 3 * level
        health = 100 + 20 * level
    elif char_class == "Mage":
        strength = 3 * level
        magic = 10 + 5 * level
        health = 70 + 10 * level
    elif char_class == "Rogue":
        strength = 7 * level
        magic = 5 * level
        health = 80 + 15 * level
    elif char_class == "Cleric":
        strength = 6 * level
        magic = 8 * level
        health = 90 + 12 * level
    else:
        strength = 5 * level
        magic = 5 * level
        health = 80 + 10 * level
    return strength, magic, health


def create_character(name=None, char_class=None):
    """Create and return a character dictionary."""
    if name is None:
        name = ""
    if char_class is None:
        char_class = "Warrior"

    valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]
    if char_class not in valid_classes:
        print("Invalid class. Character not created.")
        return None

    strength, magic, health = calculate_stats(char_class, 1)
    gold = 100
    level = 1
    xp = 0

    if char_class == "Warrior":
        weapon = "Longsword"
        gear = ["Chainmail", "Shield"]
        abilities = ["Power Strike", "Taunt"]
        path = "Guardian"
        story = f"{name} trained as a blacksmith's apprentice before becoming a warrior."
    elif char_class == "Mage":
        weapon = "Staff"
        gear = ["Robe", "Spellbook"]
        abilities = ["Fireball", "Teleport"]
        path = "Scholar"
        story = f"{name} studied ancient tomes and learned the art of magic."
    elif char_class == "Rogue":
        weapon = "Dagger"
        gear = ["Leather Armor", "Lockpicks"]
        abilities = ["Backstab", "Evade"]
        path = "Scout"
        story = f"{name} grew up in the streets and mastered the shadows."
    else:  # Cleric
        weapon = "Mace"
        gear = ["Blessed Robe", "Holy Symbol"]
        abilities = ["Heal", "Smite"]
        path = "Acolyte"
        story = f"{name} devoted their life to helping others through divine power."

    return {
        "name": name,
        "class": char_class,
        "level": level,
        "xp": xp,
        "strength": strength,
        "magic": magic,
        "health": health,
        "gold": gold,
        "weapon": weapon,
        "gear": gear,
        "abilities": abilities,
        "pathway": path,
        "backstory": story
    }


def level_up(character):
    """Increase level and improve stats."""
    if not character:
        return None
    character["level"] = character["level"] + 1
    character["strength"] = character["strength"] + 2
    character["magic"] = character["magic"] + 1
    character["health"] = character["health"] + 10
    character["xp"] = 0
    print(character["name"] + " has leveled up to level " + str(character["level"]) + "!")
    return character


def display_character(character):
    """Print character info to console."""
    if not character:
        return
    print("=== CHARACTER SHEET ===")
    print("Name:", character["name"])
    print("Class:", character["class"])
    print("Level:", character["level"])
    print("Strength:", character["strength"])
    print("Magic:", character["magic"])
    print("Health:", character["health"])
    print("Gold:", character["gold"])
    print("Weapon:", character["weapon"])
    print("Gear:", ", ".join(character["gear"]))
    print("Abilities:", ", ".join(character["abilities"]))
    print("Pathway:", character["pathway"])
    print("Backstory:", character["backstory"])
    print("XP:", character["xp"], "/100")


def save_character(character, filename):
    """Save character data to a text file."""
    if not filename or not isinstance(filename, str):
        return False
    directory = os.path.dirname(os.path.normpath(filename))
    if directory and not os.path.exists(directory):
        return False
    if os.name == "nt" and filename.startswith("/"):
        return False
    if not isinstance(character, dict):
        return False

    file = open(filename, "w", encoding="utf-8")
    file.write("Character Name: " + character["name"] + "\n")
    file.write("Class: " + character["class"] + "\n")
    file.write("Level: " + str(character["level"]) + "\n")
    file.write("Strength: " + str(character["strength"]) + "\n")
    file.write("Magic: " + str(character["magic"]) + "\n")
    file.write("Health: " + str(character["health"]) + "\n")
    file.write("Gold: " + str(character["gold"]) + "\n")
    file.write("Weapon: " + character["weapon"] + "\n")
    file.write("Gear: " + str(character["gear"]) + "\n")
    file.write("Abilities: " + str(character["abilities"]) + "\n")
    file.write("Pathway: " + character["pathway"] + "\n")
    file.write("Backstory: " + character["backstory"] + "\n")
    file.close()

    return os.path.exists(filename)


def load_character(filename):
    """Load character data from a text file."""
    if not os.path.exists(filename):
        return None

    file = open(filename, "r", encoding="utf-8")
    lines = file.readlines()
    file.close()

    char = {}
    for line in lines:
        if ":" in line:
            key, value = line.strip().split(":", 1)
            key = key.strip()
            value = value.strip()

            if key == "Character Name":
                key = "name"
            elif key == "Class":
                key = "class"
            elif key == "Level":
                key = "level"
            elif key == "Strength":
                key = "strength"
            elif key == "Magic":
                key = "magic"
            elif key == "Health":
                key = "health"
            elif key == "Gold":
                key = "gold"
            elif key == "Weapon":
                key = "weapon"
            elif key == "Gear":
                key = "gear"
            elif key == "Abilities":
                key = "abilities"
            elif key == "Pathway":
                key = "pathway"
            elif key == "Backstory":
                key = "backstory"

            if key in ["level", "strength", "magic", "health", "gold"]:
                if value.isdigit():
                    value = int(value)
            elif key in ["gear", "abilities"]:
                if "[" in value and "]" in value:
                    parts = value.strip("[]").split(",")
                    fixed = []
                    for v in parts:
                        v = v.strip().strip("'").strip('"')
                        if v:
                            fixed.append(v)
                    value = fixed

            char[key] = value

    return char


if __name__ == "__main__":
    print("=== RPG Character Creator ===")
    name = input("Enter your character's name: ").strip()
    char_class = input("Choose a class (Warrior, Mage, Rogue, Cleric): ").strip().capitalize()
    player = create_character(name, char_class)
    if player:
        display_character(player)
        if input("Level up? (y/n): ").strip().lower() == "y":
            level_up(player)
            display_character(player)
        fname = input("Enter filename to save your character: ").strip()
        if save_character(player, fname):
            print("Character saved successfully!")
        else:
            print("Character could not be saved.")
