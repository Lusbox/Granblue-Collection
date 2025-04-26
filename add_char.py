import json
import os

json_file = "data/characters.json"

with open(json_file, 'r') as f:
    characters = json.load(f)

print("=== Add New Character ===")

name = input("Character Name: ")
element = input("Element (fire/water/earth/wind/light/dark): ")
rarity = input("Rarity (SSR/SR/R): ")
race = input("Race (human/erune/draph/harvin/primal/other): ")

image_path = f"assets/characters/{element}/{name.capitalize()}{element[0].capitalize()}.jpg"
big_pic_path = f"assets/characters/{element}/{name.capitalize()}{element[0].capitalize()}_pic.png"

obtained = False

new_character = {
    "name": name.capitalize(),
    "image": image_path,
    "element": element.capitalize(),
    "rarity": rarity.upper(),
    "big_pic": big_pic_path,
    "race": race.capitalize(),
    "obtained": obtained

}

characters.append(new_character)

with open(json_file, 'w') as f:
    json.dump(characters, f, indent=2)

print(f"Added {name} to character database")