#!/usr/bin/env python3
import discord, discord.utils, random, os, re, json, sys, time
from os import path
from datetime import datetime, timedelta
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('DISCORD_KEY')

#Bad way to do it, I know.
colours = ["default","teal","dark teal","green","dark green","blue","dark blue","purple","dark purple","magenta","dark magenta","gold","dark gold","orange","dark orange","red","dark red","lighter grey", "dark grey", "light grey", "darker grey", "blurple", "greyple"]
colourings = {"default":discord.Colour.default(),"teal":discord.Colour.teal(),"dark teal":discord.Colour.dark_teal(),"green":discord.Colour.green(),"dark green":discord.Colour.dark_green(),"blue":discord.Colour.blue(),"dark blue":discord.Colour.dark_blue(),"purple":discord.Colour.purple(),"dark purple":discord.Colour.dark_purple(),"magenta":discord.Colour.magenta(),"dark magenta":discord.Colour.dark_magenta(),"gold":discord.Colour.gold(),"dark gold":discord.Colour.dark_gold(),"orange":discord.Colour.orange(),"dark orange":discord.Colour.dark_orange(),"red":discord.Colour.red(),"dark red":discord.Colour.dark_red(),"lighter grey":discord.Colour.lighter_grey(),"dark grey":discord.Colour.dark_grey(),"light grey":discord.Colour.light_grey(),"darker grey":discord.Colour.darker_grey(),"blurple":discord.Colour.blurple(),"greyple":discord.Colour.greyple()}

client = discord.Client()

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

    roles = message.author.roles
    isCommittee = False
    isCaptain = False
    isJudge = False
    for role in roles:
        if role.id == "VTC Committee" or role.name == "Thom":
            isCommittee = True
        if role.id == "Judge":
            isJudge = True
        if role.name == "Team Captain":
            isCaptain = True

    #Find Bot-logs channel. There is probably a better way than this though.
    for channel in message.guild.channels:
        if channel.name == "bot-logs":
            logchannel = channel
            break

    for mentions in message.mentions:
        if mentions.id == message.guild.me.id:
            await message.channel.send("Woof?")

    if message.content.lower() == ("$roll"):
        i = random.randint(1,6)
        response = "You rolled a " + str(i) + " {0.author.mention}."
        await message.channel.send(response.format(message))

    if message.content.lower() == ("$flip"):
        i = random.randint(0,1)
        if i == 0:
            response = "It's Heads!"
        else:
            response = "It's Tails!"
        await message.channel.send(response.format(message))

    #Timer commands
    if message.content.lower() == "$timer":
        await message.channel.send("The $timer command must be followed by a time period, and optionally a reason. For example: `$timer 03:00` will set a timer for 3 hours. If you wish, you can include a reason afterwards. For example: `$timer 01:30 Ryan and Thom's game` will set a timer for 1 hour 30 minutes with the reason *\"Ryan and Thom's game\"*.")
        return

    if message.content.lower().startswith("$timer "):
        timer = message.content[7:12]
        hours = message.content[7:9]
        minutes = message.content[10:12]
        seconds = "00"
        reason = message.content[13:]
        if re.match("[0-9][0-9]:[0-5][0-9]",timer):
            response = "Setting timer for " + str(int(hours)) + " hour(s) and " + str(int(minutes)) + " minute(s). Let the count down begin!"
            await message.channel.send(response.format(message))
            
            duration = int(seconds) + (int(minutes) * 60) + (int(hours) * 60 *60)
            now = datetime.utcnow()
            embed = discord.Embed(title="Timer", description=reason, color=0x4444dd)
            embed.add_field(name="Duration", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
            embed.add_field(name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
            embed.set_footer(text="Updated at: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
            timermsg = await message.channel.send(embed=embed)
            
            #Start counting down
            start = datetime.now()
            end = start + timedelta(seconds=duration)
            i = 0
            while datetime.now() < end:
                time.sleep(0.5)
                i = i+1
                remaining = int((end - datetime.now()).total_seconds())
                hours = str(int(remaining / 3600))
                minutes = str(int((remaining % 3600)/60))
                seconds = str(remaining % 60)
                if (remaining >= 600 and i == 30) or (remaining >= 30 and remaining < 600 and i >= 10) or (remaining < 30 and i >= 5) or remaining <= 5:
                    now = datetime.utcnow()
                    embed.set_field_at(1,name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                    embed.set_footer(text="Updated at: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                    await timermsg.edit(embed=embed)
                    i = 0
            
            #timer complete!
            embed.set_field_at(1,name="Remaining", value="`00:00:00` ", inline=True) 
            await timermsg.edit(embed=embed)
            response = "Your timer has finished {0.author.mention}!".format(message)
            await message.channel.send(response)
        else:
            await message.channel.send("That isn't a valid time!")
        return

    if message.content.lower() == "$heret":
        response = "The $heret command must be followed by a time period and a reason. For example: `!here 03:00 dice down` will set a timer for 3 hours the reason *\"dice down\"*."
        await message.channel.send(response.format(message))
        return

    if message.content.lower().startswith("$heret "):
        timer = message.content[7:12]
        hours = message.content[7:9]
        minutes = message.content[10:12]
        seconds = "00"
        reason = message.content[13:]
        if reason == "":
            await message.channel.send("Here timers must have a reason.")
            return
        roles =  message.author.roles
        if isJudge == False and isCommittee == False:
            await message.channel.send("You must be a Judge or Committee Member to use Here Timers.")
        elif re.match("[0-9][0-9]:[0-5][0-9]",timer):
            response = "Setting timer for " + str(int(hours)) + " hour(s) and " + str(int(minutes)) + " minute(s). Let the count down begin!"
            await message.channel.send(response.format(message))
            
            duration = int(seconds) + (int(minutes) * 60) + (int(hours) * 60 *60)
            now = datetime.utcnow()
            embed = discord.Embed(title="Here Timer", description=reason, color=0x4444dd)
            embed.add_field(name="Duration", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
            embed.add_field(name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
            embed.set_footer(text="Updated at: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
            timermsg = await message.channel.send(embed=embed)
            
            #Start counting down
            start = datetime.now()
            end = start + timedelta(seconds=duration)
            i = 0
            while datetime.now() < end:
                i = i+1
                time.sleep(0.5)
                remaining = int((end - datetime.now()).total_seconds())
                hours = str(int(remaining / 3600))
                minutes = str(int((remaining % 3600)/60))
                seconds = str(remaining % 60)
                if (remaining >= 600 and i == 30) or (remaining >= 30 and remaining < 600 and i >= 10) or (remaining < 30 and i >= 5) or remaining <= 5:
                    now = datetime.utcnow()
                    embed.set_field_at(1,name="Remaining", value="`" + '%02d' % int(hours) + ":" + '%02d' % int(minutes) + ":" + '%02d' % int(seconds) + "` ", inline=True) 
                    embed.set_footer(text="Updated at: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                    await timermsg.edit(embed=embed)
                    i = 0
            
            #timer complete!
            embed.set_field_at(1,name="Remaining", value="`00:00:00` ", inline=True) 
            await timermsg.edit(embed=embed)
            response = "".join(["@here , the timer has finished! ", reason]).format(message)
            await message.channel.send(response)
        else:
            await message.channel.send("That isn't a valid time!")
        return


    #Want these commands in the right channel
    if str(message.channel).lower().startswith("bot"):

        if message.content.lower() == "$colours":
            response = "You can choose from any of the following colours: *" + ", ".join(colours) + "*"
            await message.channel.send(response.format(message))
            return

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
                dm = """Hi, you've been given the Team Captain role in the Warmachine and Hordes Virtual Team Championship!

To get started, you'll want to create your team using the `$teamname` command in the bot-commands channel. Once you've done that, you'll have access to all the table channels, and your team will have it's own channel category created. If you''re not completely decided on a name yet, don't worry, you can change it again later using the same command.

Once your team has been created, you can start adding people to the team using the `$addplayer` command. You can also choose the colour of your team's role using $teamcolour.

If you get stuck, just visit the guide in the #bot-help channel: <https://discordapp.com/channels/721685559277256806/721693621413478420/722049487874424892>

Thanks for joining the tournament, and good luck!"""
                newcaptain = client.get_user(message.mentions[0].id)
                await newcaptain.send(dm.format(message))
                #Log details
                embed = discord.Embed(title="Add Team Captain", color=0xa551be) #description=message.mentions[0].display_name
                embed.add_field(name="Added By", value=message.author.display_name, inline=False)
                embed.add_field(name="Added ID", value=message.author.id, inline=False)
                embed.add_field(name="Captain Added", value=message.mentions[0].display_name, inline=False)
                embed.add_field(name="Captain ID", value=message.mentions[0].id, inline=False)
                now = datetime.utcnow()
                embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                await logchannel.send(embed=embed)
                return

        #Give someone the Judge Rank
        if message.content.lower().startswith("$addjudge"):
            if isCommittee == False:
                await message.channel.send("Only Committee members can use that command.")
                return
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to give Judge role.")
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
                embed = discord.Embed(title="Add Judge", color=discord.Colour.blue()) #description=message.mentions[0].display_name
                embed.add_field(name="Added By", value=message.author.display_name, inline=False)
                embed.add_field(name="Added ID", value=message.author.id, inline=False)
                embed.add_field(name="Judge Added", value=message.mentions[0].display_name, inline=False)
                embed.add_field(name="Judge ID", value=message.mentions[0].id, inline=False)
                now = datetime.utcnow()
                embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
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
                embed = discord.Embed(title="Add Head Judge", color=discord.Colour.dark_blue()) #description=message.mentions[0].display_name
                embed.add_field(name="Added By", value=message.author.display_name, inline=False)
                embed.add_field(name="Added ID", value=message.author.id, inline=False)
                embed.add_field(name="Head Judge Added", value=message.mentions[0].display_name, inline=False)
                embed.add_field(name="Head Judge ID", value=message.mentions[0].id, inline=False)
                now = datetime.utcnow()
                embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                await logchannel.send(embed=embed)
                return

        if message.content.lower().startswith("$removejudge"):
            if isCommittee == False:
                await message.channel.send("Only Committee members can use that command.")
                return
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to remove Streamer role.")
                return
            else:
                if len(message.mentions[0].roles) < 2:
                    await message.channel.send("User does not have the Judge Role to remove.")
                elif len(message.mentions[0].roles) == 2:
                    role = message.mentions[0].roles[1]
                    if role.name == "Judge":
                        await message.mentions[0].remove_roles(role)
                        response = "{0.mentions[0].display_name} has been removed from the Judge Role."
                        await message.channel.send(response.format(message))
                        #Log details
                        embed = discord.Embed(title="Remove Player as Judge", color=discord.Colour.blue()) 
                        embed.add_field(name="Removed By", value=message.author.display_name, inline=False)
                        embed.add_field(name="Removed ID", value=message.author.id, inline=False)
                        embed.add_field(name="Removed Player", value=message.mentions[0].display_name, inline=False)
                        embed.add_field(name="Removed ID", value=message.mentions[0].id, inline=False)
                        now = datetime.utcnow()
                        embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                        await logchannel.send(embed=embed)
                    else:
                        await message.channel.send("User does not have the Judge Role to remove.")
                else:
                    role1 = message.mentions[0].roles[1]
                    role2 = message.mentions[0].roles[2]
                    if role2.name == "Judge" or role2.name == "Head Judge":
                        await message.mentions[0].remove_roles(role2)
                        response = "{0.mentions[0].display_name} has been removed from the " + role2.name + " role."
                        await message.channel.send(response.format(message))
                        if role2.name == "Judge":
                            colour = discord.Colour.blue()
                        else:
                            colour = discord.Colour.dark_blue()
                        #Log details
                        embed = discord.Embed(title="Remove Player as " + role2.name, color=colour) 
                        embed.add_field(name="Removed By", value=message.author.display_name, inline=False)
                        embed.add_field(name="Removed ID", value=message.author.id, inline=False)
                        embed.add_field(name="Removed Player", value=message.mentions[0].display_name, inline=False)
                        embed.add_field(name="Removed ID", value=message.mentions[0].id, inline=False)
                        now = datetime.utcnow()
                        embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                        await logchannel.send(embed=embed)
                    if role1.name == "Judge" or role1.name == "Head Judge":
                        await message.mentions[0].remove_roles(role1)
                        response = "{0.mentions[0].display_name} has been removed from the " + role1.name + " role."
                        await message.channel.send(response.format(message))
                        if role1.name == "Judge":
                            colour = discord.Colour.blue()
                        else:
                            colour = discord.Colour.dark_blue()
                        #Log details
                        embed = discord.Embed(title="Remove Player as " + role1.name, color=colour) 
                        embed.add_field(name="Removed By", value=message.author.display_name, inline=False)
                        embed.add_field(name="Removed ID", value=message.author.id, inline=False)
                        embed.add_field(name="Removed Player", value=message.mentions[0].display_name, inline=False)
                        embed.add_field(name="Removed ID", value=message.mentions[0].id, inline=False)
                        now = datetime.utcnow()
                        embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
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
                now = datetime.utcnow()
                embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                await logchannel.send(embed=embed)
                return

        if message.content.lower().startswith("$removestreamer"):
            if isCommittee == False:
                await message.channel.send("Only Committee members can use that command.")
                return
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to remove Streamer role.")
                return
            else:
                role = message.mentions[0].roles[1]
                if role.name == "Streamer":
                    await message.mentions[0].remove_roles(role)
                    response = "{0.mentions[0].display_name} has been removed from the Streamer Role."
                    await message.channel.send(response.format(message))
                    #Log details
                    embed = discord.Embed(title="Remove Player as Streamer", color=0x9147ff) 
                    embed.add_field(name="Removed By", value=message.author.display_name, inline=False)
                    embed.add_field(name="Removed ID", value=message.author.id, inline=False)
                    embed.add_field(name="Removed Player", value=message.mentions[0].display_name, inline=False)
                    embed.add_field(name="Removed ID", value=message.mentions[0].id, inline=False)
                    now = datetime.utcnow()
                    embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                    await logchannel.send(embed=embed)
                else:
                    await message.channel.send("User does not have the Streamer Role to remove.")
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
                    elif guildrole.name == "Judge":
                        JudgeRole = guildrole
                    elif guildrole.name == "Head Judge":
                        HeadJudgeRole = guildrole
                #Check Team Captain is already in a Team
                if len(message.author.roles) == 2:
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
                                await guildchannel.set_permissions(newrole, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True,add_reactions=True)
                                #await guildchannel.set_permissions(CommitteeRole, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True,manage_messages=True,mention_everyone=True,add_reactions=True)
                                #await guildchannel.set_permissions(HeadJudgeRole, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True,manage_messages=True,mention_everyone=True,add_reactions=True)
                                #await guildchannel.set_permissions(JudgeRole, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True,mention_everyone=True,add_reactions=True)
                            elif guildchannel.type.name == "voice" and "game" in guildchannel.name.lower():
                                print("Setting connect and speak permissions")
                                await guildchannel.set_permissions(newrole,view_channel=True,connect=True,speak=True)
                                #await guildchannel.set_permissions(CommitteeRole,view_channel=True,connect=True,speak=True,mute_members=True,move_members=True,priority_speaker=True)
                                #await guildchannel.set_permissions(HeadJudgeRole,view_channel=True,connect=True,speak=True,mute_members=True,move_members=True,priority_speaker=True)
                                #await guildchannel.set_permissions(JudgeRole,view_channel=True,connect=True,speak=True,mute_members=True,move_members=True,priority_speaker=True)
                    await message.channel.send("Table Permissions set. Creating team channels.")
                    #Create the Category and Channels
                    newcategory = await guild.create_category(teamname)
                    #await newcategory.edit(position=5) #Decided against this.
                    talkrights = {guild.default_role: discord.PermissionOverwrite(read_messages=False),guild.me: discord.PermissionOverwrite(read_messages=True)}
                    newtalk = await guild.create_text_channel(name="Team Chat",category=newcategory,overwrites=talkrights)
                    await newtalk.set_permissions(newrole, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True)
                    await newtalk.set_permissions(CommitteeRole, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True)
                    await newtalk.set_permissions(HeadJudgeRole, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True)
                    chatrights = {guild.default_role: discord.PermissionOverwrite(view_channel=False)}
                    newchat = await guild.create_voice_channel(name="Team Talk",category=newcategory,overwrites=chatrights)
                    await newchat.set_permissions(newrole,view_channel=True,connect=True,speak=True)
                    await newchat.set_permissions(CommitteeRole,view_channel=True,connect=True,speak=True)
                    await newchat.set_permissions(HeadJudgeRole,view_channel=True,connect=True,speak=True)
                    await message.channel.send("New Team created.")
                    #Log details
                    embed = discord.Embed(title="Create New Team", color=0x999999) 
                    embed.add_field(name="Created By", value=message.author.display_name, inline=False)
                    embed.add_field(name="Created ID", value=message.author.id, inline=False)
                    embed.add_field(name="Team Name", value=teamname, inline=False)
                    now = datetime.utcnow()
                    embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
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
                    now = datetime.utcnow()
                    embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
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
                elif message.content.lower() == "$teamcolour":
                    await message.channel.send("You must supply a colour. Either provide a colour hex, or use one of the preprogrammed colours. See `$colours` or <https://htmlcolorcodes.com/color-picker/> for ideas.")
                elif not re.match("[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]",teamcolour) and colours.count(teamcolour) == 0:
                    await message.channel.send("Invalid hex or predefined colour.")
                else:
                    if message.author.roles[1].name == "Team Captain":
                        teamrole = message.author.roles[2]
                    else:
                        teamrole = message.author.roles[1]
                    if colours.count(teamcolour) == 1:
                        colour = colourings[teamcolour]
                        await teamrole.edit(colour=discord.Colour(colour.value))
                        embed = discord.Embed(title="Change Team Colour", color=colour.value) 
                    else:
                        colour = int("0x"+teamcolour,16)
                        await teamrole.edit(colour=discord.Colour(colour))
                        embed = discord.Embed(title="Change Team Colour", color=colour) 
                    await message.channel.send("Team colour has been changed.")
                    #Log details
                    embed.add_field(name="Changed By", value=message.author.display_name, inline=False)
                    embed.add_field(name="Changed ID", value=message.author.id, inline=False)
                    now = datetime.utcnow()
                    embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
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
                now = datetime.utcnow()
                embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
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
                now = datetime.utcnow()
                embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                await logchannel.send(embed=embed)


client.run(key)