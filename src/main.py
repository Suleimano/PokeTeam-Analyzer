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
  



while True:
    choice = input("Select 'create' to create a team, 'view' to view existing teams, 'clear' to clear existing teams"
    "'AI' to set up your API key, or 'analyze' to analyze your pokemon team.\n").strip().lower()
    
    if choice == 'create':

        poketeam = []
        count = 1

        print("Enter the names (or dex numbers) of the pokemon you wish to add to the team: ")

        while count <= 6:

            query = input(f"{count}: ")
            
            pokemon = get_pokemon(query)

            if pokemon is not None:
                if pokemon['name'] not in poketeam:

                    poketeam.append(pokemon['name'])
                    print(f"{pokemon['name']} has been added to the team!")
                    count += 1

                else:

                    print("That pokemon is already in the team!")
            else:
                print("That pokemon does not exist!")
        
        saved_teams.append(poketeam)

        with open(file_path, "w") as f:
            json.dump(saved_teams, f)

        print("Team successfuly built!\n")
        print(f"Team {len(saved_teams)}")
        for index, teammember in enumerate(poketeam, start=1):
            print(f"{index}: {teammember}")

    elif choice == 'view':
        if not saved_teams:
            print("There are no teams available!")

        print("Pokemon teams available:")
        for i, team in enumerate(saved_teams, start=1):
            print(f"\nTeam {i}")
            for j in range(len(team)):
                
                print(f"{(j+1)}: {team[j]}", end=" ")
            print() 

    elif choice == 'ai':

        api_key = input("Enter your Groq API key: ").strip()

        with open(key_path, "w") as f:
            f.write(api_key)
        print("API key saved!")

    elif choice == 'clear':

        saved_teams = []

        with open(file_path, "w") as f:
            json.dump(saved_teams, f)

        print("Team sheets have been cleared!")

    elif choice == 'analyze':
        if not api_key:
            print("No API key set! Select 'AI' from the main menu to add one.")
        elif not saved_teams:
            print("No teams available! Select 'create' from the main menu to build one.")
        else:
            print("Pokemon teams available:")
            for i, team in enumerate(saved_teams, start=1):
                print(f"\nTeam {i}")
                for j in range(len(team)):
                    print(f"{(j+1)}: {team[j]}", end=" ")
            print()

            while True:
                pick = input("\nEnter the team number to analyze: ").strip()
                if pick.isdigit() and 1 <= int(pick) <= len(saved_teams):
                    break
                print("Invalid team number! Try again.")

            chosen_team = saved_teams[int(pick) - 1]
            print(f"\nAnalyzing Team {pick}...\n")
            try:
                stream_team_analysis(chosen_team, api_key)
            except urllib.error.HTTPError as e:
                print(f"\nHTTP {e.code}: {e.read().decode()}")   # Prints error message as is for debugging.
    else:
        print("Invalid option! Try again.")               
    print()
