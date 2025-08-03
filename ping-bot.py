import discord
import sqlite3
import os
from keep_alive import keep_alive  # Optional if you're using uptime pings

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Start web server to keep Railway or Replit alive
keep_alive()

def init_db():
    db = sqlite3.connect('pings.sqlite')
    cursor = db.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS pings (id INTEGER PRIMARY KEY, count INTEGER)')
    cursor.execute('INSERT OR IGNORE INTO pings (id, count) VALUES (?, ?)', (1, 0))
    db.commit()
    db.close()

init_db()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        db = sqlite3.connect('pings.sqlite')
        cursor = db.cursor()
        cursor.execute('SELECT count FROM pings WHERE id = 1')
        count = cursor.fetchone()[0] + 1
        cursor.execute('UPDATE pings SET count = ? WHERE id = 1', (count,))
        db.commit()
        db.close()
        await message.channel.send(f"I've been pinged {count} times!")

# Use the token from the Railway environment variable
client.run(os.getenv("DISCORD_TOKEN"))
