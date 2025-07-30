import discord
import requests
import asyncio
from datetime import datetime

TOKEN = "YourBotTokenInHere"
CHANNEL_ID = "Your channel Id"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def weather_task():
    city = "Mostaganem"
    url = f"https://wttr.in/{city}?format=j1"
    previous_weather = None

    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            current = data["current_condition"][0]
            temp_c = current["temp_C"]
            desc = current["weatherDesc"][0]["value"]
            current_weather = f"{temp_c}°C, {desc}"

            if current_weather != previous_weather:
                await channel.send(f"Weather in {city} changed: {current_weather}")
                previous_weather = current_weather

        await asyncio.sleep(60)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    asyncio.create_task(weather_task())

client.run(TOKEN)
