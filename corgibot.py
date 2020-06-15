#!/usr/bin/env python3
import discord, discord.utils, random, os, re, json,sys
from os import path
from shutil import copyfile
from datetime import datetime, timedelta
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

client = discord.Client()

directory = os.path.dirname(os.path.realpath(__file__))

load_dotenv()
key = os.getenv('DISCORD_KEY')

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))
    game = discord.Game("See #bot-help")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print('Message from {0.author}: {0.content}'.format(message))

    #Find Bot-logs channel. There is probably a better way than this though.
    for channel in message.guild.channels:
        if channel.name == "bot-logs":
            logchannel = channel
            break

    if message.content.lower() == ("$roll"):
        i = random.randint(1,6)
        response = "You rolled a " + str(i) + " {0.author.mention}."
        await message.channel.send(response.format(message))

    #Want these commands in the right channel
    if str(message.channel).lower().startswith("bot"):
        roles = message.author.roles
        isCommittee = False
        isCaptain = False
        for role in roles:
            if role.id == "VTC Committee" or role.name == "Thom":
                isCommittee = True
            if role.name == "Team Captain":
                isCaptain = True

        #Give someone the Team Captain Rank
        if message.content.lower().startswith("$addcaptain"):
            if isCommittee == False:
                await message.channel.send("Only Committee members can use that command.")
                return
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to give Team Captain role.")
                return
            elif len(message.mentions[0].roles) > 1:
                await message.channel.send("User already has a server role and cannot be made a captain.")
                return
            else:
                role = discord.utils.get(message.guild.roles, name="Team Captain")
                await message.mentions[0].add_roles(role)
                response = "{0.mentions[0].display_name} has been given the Team Captain Role."
                await message.channel.send(response.format(message))
                #Log details
                embed = discord.Embed(title="Add Team Captain", color=0xa551be) #description=message.mentions[0].display_name
                embed.add_field(name="Added By", value=message.author.display_name, inline=False)
                embed.add_field(name="Added ID", value=message.author.id, inline=False)
                embed.add_field(name="Captain Added", value=message.mentions[0].display_name, inline=False)
                embed.add_field(name="Captain ID", value=message.mentions[0].id, inline=False)
                await logchannel.send(embed=embed)
                return

        #Give someone the Judge Rank
        if message.content.lower().startswith("$addjudge"):
            if isCommittee == False:
                await message.channel.send("Only Committee members can use that command.")
                return
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to give JUdge role.")
                return
            elif len(message.mentions[0].roles) > 1:
                await message.channel.send("User already has a server role and cannot be made a Judge.")
                return
            else:
                role = discord.utils.get(message.guild.roles, name="Judge")
                await message.mentions[0].add_roles(role)
                response = "{0.mentions[0].display_name} has been given the Judge Role."
                await message.channel.send(response.format(message))
                #Log details
                embed = discord.Embed(title="Add Judge", color=0x0033dd) #description=message.mentions[0].display_name
                embed.add_field(name="Added By", value=message.author.display_name, inline=False)
                embed.add_field(name="Added ID", value=message.author.id, inline=False)
                embed.add_field(name="Judge Added", value=message.mentions[0].display_name, inline=False)
                embed.add_field(name="Judge ID", value=message.mentions[0].id, inline=False)
                await logchannel.send(embed=embed)
                return

        #Give someone the Judge Rank
        if message.content.lower().startswith("$addheadjudge"):
            if isCommittee == False:
                await message.channel.send("Only Committee members can use that command.")
                return
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to give Head Judge role.")
                return
            elif len(message.mentions[0].roles) > 1:
                await message.channel.send("User already has a server role and cannot be made a Judge.")
                return
            else:
                role = discord.utils.get(message.guild.roles, name="Judge")
                await message.mentions[0].add_roles(role)
                role = discord.utils.get(message.guild.roles, name="Head Judge")
                await message.mentions[0].add_roles(role)
                response = "{0.mentions[0].display_name} has been given the Head Judge Role."
                await message.channel.send(response.format(message))
                #Log details
                embed = discord.Embed(title="Add Head Judge", color=0x001199) #description=message.mentions[0].display_name
                embed.add_field(name="Added By", value=message.author.display_name, inline=False)
                embed.add_field(name="Added ID", value=message.author.id, inline=False)
                embed.add_field(name="Head Judge Added", value=message.mentions[0].display_name, inline=False)
                embed.add_field(name="Head Judge ID", value=message.mentions[0].id, inline=False)
                await logchannel.send(embed=embed)
                return

        #Give someone the Judge Rank
        if message.content.lower().startswith("$addstreamer"):
            if isCommittee == False:
                await message.channel.send("Only Committee members can use that command.")
                return
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to give Streamer role.")
                return
            elif len(message.mentions[0].roles) > 1:
                await message.channel.send("User already has a server role and cannot be made a Streamer.")
                return
            else:
                role = discord.utils.get(message.guild.roles, name="Streamer")
                await message.mentions[0].add_roles(role)
                response = "{0.mentions[0].display_name} has been given the Streamer Role."
                await message.channel.send(response.format(message))
                #Log details
                embed = discord.Embed(title="Add Judge", color=0x9147ff) 
                embed.add_field(name="Added By", value=message.author.display_name, inline=False)
                embed.add_field(name="Added ID", value=message.author.id, inline=False)
                embed.add_field(name="Judge Added", value=message.mentions[0].display_name, inline=False)
                embed.add_field(name="Judge ID", value=message.mentions[0].id, inline=False)
                await logchannel.send(embed=embed)
                return


        if message.content.lower().startswith("$teamname"):
            if isCaptain == False:
                await message.channel.send("Only Team Captains can use that command.")
                return
            else:
                teamname = message.content[10:]
                #Check if the team exists
                guild = message.guild
                guildroles = guild.roles
                for guildrole in guildroles:
                    if guildrole.name.lower() == teamname.lower():
                        response = "A role with the name " + guildrole.name +" already exists. Please choose a different name."
                        await message.channel.send(response)
                        return
                    elif guildrole.name == "Team Captain":
                        CaptainRole = guildrole
                    elif guildrole.name == "VTC Committee":
                        CommitteeRole = guildrole
                    elif guildrole.name == "Head Judge":
                        HeadJudgeRole = guildrole
                #Check Team Captain is already in a Team
                if len(message.author.roles) == 2:
                    response = "Creating team " + teamname
                    await message.channel.send(response)
                    newrole = await guild.create_role(name=teamname, hoist=True)
                    await newrole.edit(position=2) 
                    await CaptainRole.edit(position=1)
                    response = "Created team " + teamname +"."
                    await message.channel.send(response)
                    role = discord.utils.get(message.guild.roles, name=teamname)
                    await message.author.add_roles(role)
                    await message.channel.send("Setting table permissions... Please hold.")
                    guildchannels = guild.channels
                    for guildchannel in guildchannels:
                        if guildchannel.name.lower().startswith('table'):
                            print(guildchannel.name)
                            if guildchannel.type.name == "text" and "game" in guildchannel.name.lower():
                                print("Setting read and send message permissions")
                                await guildchannel.set_permissions(newrole, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True)
                            elif guildchannel.type.name == "voice" and "game" in guildchannel.name.lower():
                                print("Setting connect and speak permissions")
                                await guildchannel.set_permissions(newrole,view_channel=True,connect=True,speak=True)
                    await message.channel.send("Table Permissions set. Creating team channels.")
                    #Create the Category and Channels
                    newcategory = await guild.create_category(teamname)
                    talkrights = {guild.default_role: discord.PermissionOverwrite(read_messages=False),guild.me: discord.PermissionOverwrite(read_messages=True)}
                    newtalk = await guild.create_text_channel(name="Team Talk",category=newcategory,overwrites=talkrights)
                    await newtalk.set_permissions(newrole, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True)
                    await newtalk.set_permissions(CommitteeRole, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True)
                    await newtalk.set_permissions(HeadJudgeRole, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True)
                    chatrights = {guild.default_role: discord.PermissionOverwrite(view_channel=False)}
                    newchat = await guild.create_voice_channel(name="Team Chat",category=newcategory,overwrites=chatrights)
                    await newchat.set_permissions(newrole,view_channel=True,connect=True,speak=True)
                    await newchat.set_permissions(CommitteeRole,view_channel=True,connect=True,speak=True)
                    await newchat.set_permissions(HeadJudgeRole,view_channel=True,connect=True,speak=True)
                    #Log details
                    embed = discord.Embed(title="Create New Team", color=0x999999) 
                    embed.add_field(name="Created By", value=message.author.display_name, inline=False)
                    embed.add_field(name="Created ID", value=message.author.id, inline=False)
                    embed.add_field(name="Team Name", value=teamname, inline=False)
                    await logchannel.send(embed=embed)

                #They are in one, so edit the Team's name
                else:
                    if message.author.roles[1].name == "Team Captain":
                        teamrole = message.author.roles[2]
                    else:
                        teamrole = message.author.roles[1]
                    categories = guild.categories
                    for category in categories:
                        if category.name == teamrole.name:
                            await category.edit(name=teamname)
                            break
                    embed = discord.Embed(title="Change Team Name", color=teamrole.colour) #description=message.mentions[0].display_name
                    embed.add_field(name="Changed By", value=message.author.display_name, inline=False)
                    embed.add_field(name="Changed ID", value=message.author.id, inline=False)
                    embed.add_field(name="Old Team Name", value=teamrole.name, inline=False)
                    embed.add_field(name="New Team Name", value=teamname, inline=False)
                    await logchannel.send(embed=embed)
                    await teamrole.edit(name=teamname)
                    response = "Team Name has been changed to " + teamname +"."
                    await message.channel.send(response)
                return

        if message.content.lower().startswith("$teamcolour"):
            if isCaptain == False:
                await message.channel.send("Only Team Captains can use that command.")
                return
            else:
                teamcolour = message.content[12:].lower()
                if len(message.author.roles) == 2:
                    await message.channel.send("You need to have created your team before you can set their colour.")
                elif not re.match("[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]",message.content[12:].lower()):
                    await message.channel.send("Invalid hex colour.")
                else:
                    if message.author.roles[1].name == "Team Captain":
                        teamrole = message.author.roles[2]
                    else:
                        teamrole = message.author.roles[1]
                    await teamrole.edit(colour=discord.Colour(int("0x"+teamcolour,16)))
                    await message.channel.send("Team colour has been changed.")
                    #Log details
                    embed = discord.Embed(title="Change Team Colour", color=int("0x"+teamcolour,16)) 
                    embed.add_field(name="Changed By", value=message.author.display_name, inline=False)
                    embed.add_field(name="Changed ID", value=message.author.id, inline=False)
                    await logchannel.send(embed=embed)

                return

        if message.content.lower().startswith("$addplayer"):
            if isCaptain == False:
                await message.channel.send("Only Team Captains can use that command.")
                return
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to give Team role.")
                return
            elif len(message.mentions[0].roles) > 1:
                await message.channel.send("User already has a server role and cannot be added to a team.")
                return
            else:
                if message.author.roles[1].name == "Team Captain":
                    teamrole = message.author.roles[2]
                else:
                    teamrole = message.author.roles[1]
                await message.mentions[0].add_roles(teamrole)
                response = "{0.mentions[0].display_name} has been added to the team " + teamrole.name + "."
                await message.channel.send(response.format(message))
                #Log details
                embed = discord.Embed(title="Add Player to Team", color=teamrole.color) 
                embed.add_field(name="Added By", value=message.author.display_name, inline=False)
                embed.add_field(name="Added ID", value=message.author.id, inline=False)
                embed.add_field(name="New Player", value=message.mentions[0].display_name, inline=False)
                embed.add_field(name="NewID", value=message.mentions[0].id, inline=False)
                await logchannel.send(embed=embed)

        if message.content.lower().startswith("$removeplayer"):
            if isCaptain == False:
                await message.channel.send("Only Team Captains can use that command.")
                return
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to remove Team role.")
                return
            else:
                if message.author.roles[1].name == "Team Captain":
                    teamrole = message.author.roles[2]
                else:
                    teamrole = message.author.roles[1]
                await message.mentions[0].remove_roles(teamrole)
                response = "{0.mentions[0].display_name} has been removed from the team " + teamrole.name + "."
                await message.channel.send(response.format(message))
                #Log details
                embed = discord.Embed(title="Remove Player from Team", color=teamrole.color) 
                embed.add_field(name="Removed By", value=message.author.display_name, inline=False)
                embed.add_field(name="Removed ID", value=message.author.id, inline=False)
                embed.add_field(name="Removed Player", value=message.mentions[0].display_name, inline=False)
                embed.add_field(name="Removed ID", value=message.mentions[0].id, inline=False)
                await logchannel.send(embed=embed)


client.run(key)