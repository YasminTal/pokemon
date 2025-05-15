from urllib.parse import urljoin
import requests



def get_pokemon_details(BASE_URL,id):
    url = urljoin(BASE_URL, id)
    print (url)
    print (id)

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Extract height
        height = data.get("height")

        # Extract abilities (as a list of ability names)
        abilities = [a["ability"]["name"] for a in data.get("abilities", [])]

        # Extract species name from nested URL
        species_url = data.get("species", {}).get("url")
        species_name = None
        if species_url:
            species_resp = requests.get(species_url)
            if species_resp.status_code == 200:
                species_data = species_resp.json()
                species_name = species_data.get("name")

        # Print or return results
        print(f"Species: {species_name}")
        print(f"Height: {height}")
        print(f"Abilities: {abilities}")

        return {
            "species": species_name,
            "height": height,
            "abilities": abilities
        }
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None


def getApi (BASE_URL,ENDPOINT):
    url = urljoin(BASE_URL, ENDPOINT)
    response=requests.get(url)
    
    if response.status_code == 200:
     data = response.json()
     print(data)
     return data
    else:
        print(f"Error {response.status_code}: {response.text}")