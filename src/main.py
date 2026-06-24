import urllib.request, urllib.error, json


def get_pokemon(query):
    query = str(query).strip().lower()
    req = urllib.request.Request(
        f"https://pokeapi.co/api/v2/pokemon/{query}",
        headers={"User-Agent": "PokeTeamAnalyzer/0.1"}, 
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None          # signals that the pokemon does not exist
        raise                    # raises any error which is NOT from an invalid pokemon 






  



