import discord, discord.utils, os, re, json, sys, time, secrets, pyodbc,random, quantumrandom, math, datetime
from decimal import Decimal

import access

async def synctables(message):
    if access.isowner(message.guild,message.author):
        channels = message.guild.channels
        response = "Syncing table permissions to category."
        await message.channel.send(response.format(message))
        for channel in channels:
            if "table" in channel.name.lower():
                time.sleep(0.5)
                print("Syncing permissions for channel " + channel.name + ".")
                await channel.edit(sync_permissions=True)
        response = "All table permissions synced to category."
        await message.channel.send(response.format(message))
        embed = discord.Embed(title="Sync Table Permission to Category", color=discord.Colour.orange()) #description=message.mentions[0].display_name
        now = datetime.datetime.utcnow()
        embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
        logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
        await logchannel.send(embed=embed)

#Cause Ryan is an ass
async def purgeroles(message):
    if access.isowner(message.guild,message.author):
        if len(message.mentions) == 1:
            for role in message.mentions[0].roles:
                if role.name.lower() != "@everyone":
                    try:
                        await message.mentions[0].remove_roles(role)
                    except:
                        response = "Unable to remove role " + role.name + "."
                        await message.channel.send(response.format(message))
            response = "All roles removed from user."
            await message.channel.send(response.format(message))
            embed = discord.Embed(title="Removed roles from User", color=discord.Colour.orange()) #description=message.mentions[0].display_name
            now = datetime.datetime.utcnow()
            embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
            logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
            await logchannel.send(embed=embed)