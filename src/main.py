import functools, urllib.request, urllib.error, json, os

@functools.lru_cache(maxsize=None)
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


def stream_team_analysis(team, api_key):
    prompt = (
        "You are a competitive Pokémon analyst. Given this team, briefly highlight its strengths "
        "(if any notable), identify its competitive weaknesses, consider competitive viability, "
        f"and suggest replacements if needed:\nTeam: {', '.join(team)}"
    )

    payload = json.dumps({
        "model": "openai/gpt-oss-120b",                  # <-- Best free model available
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",   # Groq API link
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",             # Groq key
            "User-Agent": "PokeTeamAnalyzer/0.1",
        },
    )

    with urllib.request.urlopen(req) as r:
        for line in r:
            line = line.decode("utf-8").strip()
            if not line.startswith("data: "):
                continue
            data = line[6:]
            if data == "[DONE]":                          # This is sent by the API to end the message.
                break
            chunk = json.loads(data)
            try:
                text = chunk["choices"][0]["delta"]["content"]
            except (KeyError, IndexError):
                continue
            if text:
                print(text, end="", flush=True)
    print()


file_path = "src/data/teams.json"

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        saved_teams = json.load(f)
else:
    saved_teams = []

key_path = "src/data/api_key.txt"

if os.path.exists(key_path):
    with open(key_path, "r") as f:
        api_key = f.read().strip()
else:
    api_key = None
  



