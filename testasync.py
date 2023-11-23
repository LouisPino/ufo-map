import aiohttp
import asyncio

# The revised asynchronous function to fetch Pokémon data
async def fetch_pokemon_data():
    async with aiohttp.ClientSession() as session:
        pokemon_url = 'https://pokeapi.co/api/v2/pokemon/151'
        async with session.get(pokemon_url) as resp:
            pokemon = await resp.json()
            return pokemon['name']

# Running the asynchronous function in the current async environment
await fetch_pokemon_data()
