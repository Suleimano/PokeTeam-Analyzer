# PokeTeam Analyzer V1.1

PokeTeam Analyzer lets you build competitive pokemon teams, save them locally, and get an AI generated competitive analysis of your team composition. Pokemon data is pulled from [PokeAPI](https://pokeapi.co/) with in-memory caching. Groq's API is used for competitive analysis.

# What's new
- **Held-items** can now be set in team creation
- **Competitive formats** can now be set in team analysis

## Features

- **Build teams** of 6 pokemon, by name or by PokeDex number, including held-items
- **Save and view** teamsheets
- **AI team analysis** streamed token-by-token — covering strengths, weaknesses, competitive viability, and suggested replacements for your chosen competitive format
- **Zero third-party dependencies** — runs on the Python standard library alone

## How it works

The project is built entirely on Python's standard library: `urllib` for HTTP, `json` for storage, and `functools.lru_cache` for caching. Caching is used in accordance with the [rules of PokeAPI](https://pokeapi.co/docs/v2).

AI analysis uses Groq's API with SSE streaming, so analysis is printed as it's generated rather than all at once..

## Setup

Requires **Python 3.10+**. No dependencies to install.

```bash
git clone https://github.com/Suleimano/PokeTeam-Analyzer.git
cd poketeam-analyzer
python src/main.py
```

## Getting an API key (for analysis)

The `analyze` feature needs a free Groq API key:

1. Sign up at [console.groq.com](https://console.groq.com) — no credit card required
2. Generate an API key
3. Run the tool, select **`AI`** from the menu, and paste your key

Your key is stored locally in `src/data/api_key.txt`.



## License

[MIT](LICENSE)