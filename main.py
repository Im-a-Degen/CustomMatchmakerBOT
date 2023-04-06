import discord
import os
from sortPlayers import PlayerSorter
from discord.ext import commands

# Not very secure, but works for this
with open("botKey.txt", "r") as key_file:
    key = key_file.read().rstrip()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
custom_bot = commands.Bot(command_prefix=">>", intents=intents)

bot_name = "Customs Bossman"
role_message = ""
role_emote = ["<:Top:1091420818552147978>", "<:Jungle:1091420814433321060>", "<:Mid:1091420815582580857>",
              "<:Bot:1091420812201959434>", "<:Support:1091420816392073259>"]
players_per_role = {
    "Jungle": [],
    "Support": [],
    "Mid": [],
    "Bot": [],
    "Top": []
}

# Test data with: Rob, Clom, Tien, Kasai, Jake, Freddie, Fishes, Jamie, Shiggy, Ticker
players_per_role = {
    "Jungle": ["Rob", "Kasai", "Clom", "Tien", "Freddie"],
    "Mid": ["Rob", "Kasai", "Clom", "Fishes", "Shiggy"],
    "Support": ["Clom", "Kasai", "Fishes", "Ticker"],
    "Bot": ["Jake"],
    "Top": ["Tien", "Rob", "Clom", "Freddie", "Jake", "Fishes", "Jamie"]
}


@custom_bot.command()
async def custom(ctx):
    global role_message
    role_message = await ctx.send("Select Roles")
    for i in range(5):
        await role_message.add_reaction(role_emote[i])


@custom_bot.command()
async def sort(ctx):
    # global role_message
    # get_updated_message = await ctx.fetch_message(role_message.id)
    # for r in get_updated_message.reactions:
    #     if str(r) == "<:Top:1091420818552147978>":
    #         players_per_role["Top"] = [user.name async for user in r.users()]
    #         players_per_role["Top"].remove(bot_name)
    #     elif str(r) == "<:Jungle:1091420814433321060>":
    #         players_per_role["Jungle"] = [user.name async for user in r.users()]
    #         players_per_role["Jungle"].remove(bot_name)
    #     elif str(r) == "<:Mid:1091420815582580857>":
    #         players_per_role["Mid"] = [user.name async for user in r.users()]
    #         players_per_role["Mid"].remove(bot_name)
    #     elif str(r) == "<:Bot:1091420812201959434>":
    #         players_per_role["Bot"] = [user.name async for user in r.users()]
    #         players_per_role["Bot"].remove(bot_name)
    #     elif str(r) == "<:Support:1091420816392073259>":
    #         players_per_role["Support"] = [user.name async for user in r.users()]
    #         players_per_role["Support"].remove(bot_name)

    sorter = PlayerSorter(players_per_role)
    sorted_players = sorter.resultant_roles
    await ctx.send(f"{sorted_players['Top'][0]}<:Top:1091420818552147978>{sorted_players['Top'][1]}\n"
                   f"{sorted_players['Jungle'][0]}<:Jungle:1091420814433321060>{sorted_players['Jungle'][1]}\n"
                   f"{sorted_players['Mid'][0]}<:Mid:1091420815582580857>{sorted_players['Mid'][1]}\n"
                   f"{sorted_players['Bot'][0]}<:Bot:1091420812201959434>{sorted_players['Bot'][1]}\n"
                   f"{sorted_players['Support'][0]}<:Support:1091420816392073259>{sorted_players['Support'][1]}")
    if len(sorter.error_message) != 0:
        await ctx.send("Failed to sort players:")
        for item in sorter.error_message:
            await ctx.send(item)

custom_bot.run(key)
