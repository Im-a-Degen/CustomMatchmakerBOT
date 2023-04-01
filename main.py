import discord
import os
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
    "Top": [],
    "Jungle": [],
    "Mid": [],
    "Bot": [],
    "Support": []
}
roles_per_player = {}

# Test data with: Rob, Clom, Tien, Kasai, Jake, Freddie, Fishes, Jamie, Shiggy, Ticker
players_per_role = {
    "Top": ["Tien", "Rob", "Clom", "Freddie", "Jake", "Fishes", "Jamie"],
    "Jungle": ["Rob", "Kasai", "Clom", "Tien", "Freddie", "Fishes"],
    "Mid": ["Rob", "Kasai", "Clom", "Fishes", "Shiggy"],
    "Bot": ["Kasai", "Clom", "Jake", "Jamie"],
    "Support": ["Clom", "Kasai", "Fishes", "Ticker"]
}


@custom_bot.command()
async def custom(ctx):
    global role_message
    role_message = await ctx.send("Select Roles")
    for i in range(5):
        await role_message.add_reaction(role_emote[i])


@custom_bot.command()
async def sort(ctx):
    global role_message
    get_updated_message = await ctx.fetch_message(role_message.id)
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

    for k, v in players_per_role.items():
        for player in v:
            if player in roles_per_player:
                roles_per_player[player].append(k)
            else:
                roles_per_player[player] = [k]
    print(players_per_role)
    print(roles_per_player)

custom_bot.run(key)

