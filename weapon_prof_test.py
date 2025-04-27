#for future potential character field entry updates

import json

with open('data/characters.json', 'r') as file:
    characters = json.load(file)


for i, char in enumerate(characters):
    print(f"\nCharacter: {char.get('name', 'Unknown')} ({i+1}/{len(characters)})")
    
    current_value = char.get("weapon_prof", "None")
    print(f"Current weapon proficiency: {current_value}")
    
    new_value = input(f"Enter weapon proficiency for {char.get('name', 'Unknown')} (or press Enter to keep '{current_value}'): ")
    
    if new_value:
        char["weapon_prof"] = new_value
    elif "weapon_prof" not in char:
        char["weapon_prof"] = "Novice"
        
    characters[i] = char
    
    if i < len(characters) - 1:
        continue_input = input("Continue to next character? (y/n): ").lower()
        if continue_input != 'y':
            print("Exiting early. Saving progress...")
            break

with open('data/characters.json', 'w') as file:
    json.dump(characters, file, indent=2)

print("Character weapon proficiencies updated successfully!")