import discord
import asyncio
import aiohttp

TOKEN = ""

FIVEM_SERVER_IP = "127.0.0.1"   
FIVEM_SERVER_PORT = "30120"     


intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def check_fivem_server():
    url = f"http://{FIVEM_SERVER_IP}:{FIVEM_SERVER_PORT}/info.json"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    return True
    except:
        return False
    return False


async def status_task():
    await client.wait_until_ready()
    while not client.is_closed():
        online = await check_fivem_server()
        if online:
            activity = discord.Game("✅ FiveM Server online")
        else:
            activity = discord.Game("❌ Server nicht erreichbar")

        await client.change_presence(status=discord.Status.online, activity=activity)
        await asyncio.sleep(30)  


@client.event
async def on_ready():
    print(f"Eingeloggt als {client.user}")


@client.event
async def setup_hook():
    client.loop.create_task(status_task())



client.run(TOKEN)
