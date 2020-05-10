import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from helpers import (get_redis_connection, append_query_to_search_history, 
                     get_recent_searches, search_on_google)
from configurations import (COMMAND_PREFIX, INCOMING_MESSAGE, REPLY)

# Load the data from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


@bot.command(name="google", help="Returns the top 5 links on Google for the searched term")
async def return_links(ctx):
    query = ctx.message.content.lstrip("!google").lstrip() # The content is of the form "!google national anthem"
    links = search_on_google(query)

    await ctx.send("The top 5 links matching the query '{}' are- ".format(query))
    await ctx.send("\n".join(links))

    # Once the top 5 links are returned to the user
    # we will append the searched term to Redis in a list
    # where the user's id will be the key for the list
    user_id = ctx.message.author.id
    append_query_to_search_history(user_id, query)


@bot.command(name="recent", help="Returns the recent searches matching the query")
async def get_recent_matches(ctx):
    query = ctx.message.content.lstrip("!recent").lstrip()
    user_id = ctx.message.author.id
    matched_searches = get_recent_searches(user_id, query)

    await ctx.send("Recent searches by the user related to '{}' are- ".format(query))
    await ctx.send(matched_searches)


@bot.event
async def on_message(message):
    if message.author == bot.user:  # We don't want the bot to reply to itself
        return

    if message.content.lower() == INCOMING_MESSAGE:
        await message.channel.send(REPLY)

    # This is required so that the bot responds to commands
    # Else the bot will only listen to the on_message event
    await bot.process_commands(message)


bot.run(TOKEN)
