import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def fetch_data(session, id):
    url = f"https://nuforc.org/sighting/?id={id}"
    print(id)
    async with session.get(url) as resp:
        content_type = resp.headers.get('Content-Type', '').lower()
        if 'application/json' in content_type:
            return await resp.json()  # JSON response
        elif 'text/html' in content_type:
            html_content = await resp.text()
            soup = BeautifulSoup(html_content, 'html.parser')
            # Parse HTML as needed
            return soup
        else:
            # Handle other content types or raise an error
            raise ValueError(f'Unexpected content type: {content_type}')

async def main():
    async with aiohttp.ClientSession() as session:
        # Fetch data for each ID concurrently
        results = await asyncio.gather(
            *[fetch_data(session, id) for id in range(16000, 17000)]
        )
        # Process results as needed
        for result in results:
            print(result)

# Execute the async function
asyncio.run(main())
