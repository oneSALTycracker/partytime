import discord
from discord.ext import commands
import requests
import json
import subprocess 
from pavlov import PavlovRCON
import asyncio


server_rcon = ""
#rcon password 
server_ip = "127.0.0.1"
#rcon ip use 127.0.0.1 if server is on same machine as bot 
server_port = ""
#rcon port

bot_token = ""

num_iterations = 12
#how many times to run giveall

role_id_to_check = 

item = "rl_rpg""

intents = discord.Intents.all()
intents.typing = True
intents.presences = False

bot = commands.Bot(command_prefix='!!', intents=intents)




print("on")
@bot.command()
async def itspartytime(ctx):
    has_role = any(role.id == role_id_to_check for role in ctx.author.roles)
    if has_role:
        lsl_pavlov = PavlovRCON(server_ip, server_port, server_rcon)
        await asyncio.sleep(1)
        InspectAll_response = await lsl_pavlov.send("InspectAll")
        unique_ids = [player["UniqueId"] for player in InspectAll_response.get("InspectList", [])]
        await asyncio.sleep(1) 
        print(InspectAll_response)
        channel = ctx.channel
        print(unique_ids)
        for unique_id in unique_ids:
            print(unique_id)
            kill_command = f"kill {unique_id}"
            slap_command = f"slap {unique_id} -1000"
            skin_command = f"SetPlayerSkin {unique_id} clown"

            while True:
                kill_response = await lsl_pavlov.send(slap_command)
                if kill_response.get("Successful", False):
                    print(f"Successfully killed player with Unique ID: {unique_id}")
                    await channel.send(f" {unique_id} died randomly")
                    break
                else:
                    print(f"Failed to kill player with Unique ID: {unique_id}. Retrying...")
            
            while True:
                slap_response = await lsl_pavlov.send(slap_command)
                if slap_response.get("Successful", False):
                    await channel.send(f" {unique_id} was given +1000 hp")
                    break
                else:
                    print(f"Failed give +1000 hp to {unique_id}. Retrying...")
                                
            while True:
                skin_response = await lsl_pavlov.send(skin_command)
                if skin_response.get("Successful", False):
                    print(f"Successfully killed player with Unique ID: {unique_id}")
                    await channel.send(f" {unique_id} got the drip")
                    break
                else:
                    print(f"Failed to skin player with Unique ID: {unique_id}. Retrying...")

        give_all_command = f"GiveAll 0 rl_rpg {unique_id}"
        give_all_response = await lsl_pavlov.send(give_all_command)

        num_iterations = 12

        for i in range(num_iterations):
            
            give_all_command0 = f"GiveAll 0 {item}"
            give_all_command1 = f"GiveAll 1 {item}"
            await lsl_pavlov.send(give_all_command0)
            await lsl_pavlov.send(give_all_command1)
            print(f"Executed 'GiveAll' command (Iteration {i + 1})")
            await channel.send(f" {i} free {item} of {num_iterations}")
            await asyncio.sleep(1)

        InspectAll_response = await lsl_pavlov.send("InspectAll")
        for unique_id in unique_ids:
            end_slap_command = f"slap {unique_id} -1000"
            await lsl_pavlov.send(end_slap_command)
            await channel.send(f"end of party {unique_id} is super hungover \n lost the 1000 extra hp")
            lsl_pavlov.close()
    else:
        await ctx.send("why do u think u can use this ?")

                

        




@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="looking for a party "))






bot.run(bot_token)
