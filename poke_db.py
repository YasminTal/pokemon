import json
import os
import re
import poke_api
import poke_db


def pokemon_save_to_db(data, filename):

    poke_db.file_exists(filename)
    if data: 
    # and 'response' in data:
        pokemon_dict = {item['name']: item['url'] for item in data['results']}
        with open(filename, 'w') as f:
            json.dump(pokemon_dict, f, indent=2)
        print(f"Saved {len(pokemon_dict)} entries to {filename}")
    else:
        print("Invalid data: cannot save to file.")


def pokemon_id_list(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    numbers = []
    for url in data.values():
        # Extract number using regex (captures digits before final '/')
        match = re.search(r'/pokemon/(\d+)/', url)
        if match:
            numbers.append(int(match.group(1)))

    return numbers

def file_exists(filename):
    if not os.path.exists(filename):
          # File doesn't exist — create it with empty dict
        with open(filename, 'w') as f:
            json.dump({}, f, indent=2)
        print(f"File '{filename}' created with empty JSON object.") 

def print_dict (filename):
    with open (filename,'r') as file:
        data=json.load(file)

        if isinstance(data, dict):
            for key, value in data.items():
                print(f"{key}: {value}")
        else:
                print("JSON is not a dictionary.")