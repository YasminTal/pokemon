
from urllib.parse import urljoin
import random

import poke_api
import poke_db
import constans

BASE_URL=constans.BASE_URL
ENDPOINT=constans.ENDPOINT
FILE_NAME=constans.ENDPOINT



data =poke_api.getApi(BASE_URL,ENDPOINT)
poke_api.pokemon_save_to_db (data,FILE_NAME)
rand_poke_id=random.choice(poke_db.pokemon_id_list(FILE_NAME))
print (rand_poke_id)
partial_url = f"{ENDPOINT}/{rand_poke_id}/"
poke_recored=poke_api.get_pokemon_details(BASE_URL,partial_url)
poke_db.print_dict(FILE_NAME)
