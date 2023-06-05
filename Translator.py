import discord
from discord.ext import commands
from deep_translator import GoogleTranslator
from langdetect import detect
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        print()
    else:
        try:
            translated = GoogleTranslator(source='auto', target='en').translate(text = str(message.content))
            print(f"{translated}{message.content}")
            if translated != message.content:
                author = message.author
                avatars = await author.display_avatar.read()
                webhook = await message.channel.create_webhook(name=message.author.name,avatar=avatars)
                await webhook.send(content=translated, username=message.author.name)
                await webhook.delete() # then delete based on variable
                await message.delete()
        except Exception as e:
            await message.channel.send(f"An error occurred during translation.\n {e}")

    await bot.process_commands(message)
    
bot.run(BOT_TOKEN)
