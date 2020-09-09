#!/usr/bin/env python3
import discord, discord.utils, random, os, re, json, sys, time, secrets
from os import path
from datetime import datetime, timedelta
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from rulewordings import throwrules, slamrules

directory = os.path.dirname(os.path.realpath(__file__))

load_dotenv()
key = os.getenv('DISCORD_KEY')
status = os.getenv('DISCORD_STATUS')

#Bad way to do it, I know.
colours = ["default","teal","dark teal","green","dark green","blue","dark blue","purple","dark purple","magenta","dark magenta","gold","dark gold","orange","dark orange","red","dark red","lighter grey", "dark grey", "light grey", "darker grey", "blurple", "greyple"]
colourings = {"default":discord.Colour.default(),"teal":discord.Colour.teal(),"dark teal":discord.Colour.dark_teal(),"green":discord.Colour.green(),"dark green":discord.Colour.dark_green(),"blue":discord.Colour.blue(),"dark blue":discord.Colour.dark_blue(),"purple":discord.Colour.purple(),"dark purple":discord.Colour.dark_purple(),"magenta":discord.Colour.magenta(),"dark magenta":discord.Colour.dark_magenta(),"gold":discord.Colour.gold(),"dark gold":discord.Colour.dark_gold(),"orange":discord.Colour.orange(),"dark orange":discord.Colour.dark_orange(),"red":discord.Colour.red(),"dark red":discord.Colour.dark_red(),"lighter grey":discord.Colour.lighter_grey(),"dark grey":discord.Colour.dark_grey(),"light grey":discord.Colour.light_grey(),"darker grey":discord.Colour.darker_grey(),"blurple":discord.Colour.blurple(),"greyple":discord.Colour.greyple()}

timezones = {"PST":{"Name":"Pacific Standard Time", "Offset":-8, "Hours":-8, "Minutes":0},"PDT":{"Name":"Pacific Daylight Time", "Offset":-7, "Hours":-8, "Minutes":0},
             "MST":{"Name":"Mountain Standard Time", "Offset":-7, "Hours":-7, "Minutes":0},"MDT":{"Name":"Mountain Daylight Time", "Offset":-6, "Hours":-6, "Minutes":0},
             "CST":{"Name":"Central Standard Time", "Offset":-6, "Hours":-6, "Minutes":0},"CDT":{"Name":"Central Daylight Time", "Offset":-5, "Hours":-5, "Minutes":0},
             "EST":{"Name":"Eastern Standard Time", "Offset":-5, "Hours":-5, "Minutes":0},"EDT":{"Name":"Eastern Daylight Time", "Offset":-4, "Hours":-4, "Minutes":0},
             "UTC":{"Name":"Universal Time Constant", "Offset":0, "Hours":0, "Minutes":0},
             "GMT":{"Name":"Greenwich Mean Time", "Offset":0, "Hours":0, "Minutes":0},"BST":{"Name":"British Summer Time", "Offset":1, "Hours":1, "Minutes":0},
             "CET":{"Name":"Central European Time", "Offset":1, "Hours":1, "Minutes":0},"CEST":{"Name":"Central Europe Summer Time", "Offset":2, "Hours":2, "Minutes":0},
             "EET":{"Name":"Eastern European Time", "Offset":2, "Hours":2, "Minutes":0},"EEST":{"Name":"Eastern Europe Summer Time", "Offset":3, "Hours":3, "Minutes":0},
             "WST":{"Name":"(Australian) Western Standard Time", "Offset":8, "Hours":8, "Minutes":0},
             "ACST":{"Name":"Australian Central Standard Time", "Offset":9.5, "Hours":9, "Minutes":30},"ACDT":{"Name":"Australian Central Daylight Saving Time", "Offset":10.5, "Hours":10, "Minutes":30},
             "AEST":{"Name":"Australian Eastern Standard Time", "Offset":10, "Hours":10, "Minutes":0},"AEDT":{"Name":"Australian Eastern Daylight Saving Time", "Offset":11, "Hours":11, "Minutes":0},
             "NZST":{"Name":"New Zealand Standard Time", "Offset":12, "Hours":12, "Minutes":0},"NZDT":{"Name":"New Zealand Daylight Time", "Offset":13, "Hours":13, "Minutes":0}}
             


client = discord.Client()

def randomcolour():
    colour = secrets.token_hex(3)
    return colour

def validatetz(tz):
    try:
        offset = timezones[tz]
        return True
    except:
        return False

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))
    game = discord.Game(status)
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
    isThom = False
    for role in roles:
        #As people, by design, can't have multiple rules, then we can safely break and not loop around 40~ roles
        if role.name == "Thom":
            isThom = True
        if role.name == "VTC Committee" or role.name == "Thom":
            isCommittee = True
        if role.name == "Head Judge":
            isHeadJudge = True
        if role.name == "Judge":
            isJudge = True
        if role.name == "Team Captain":
            isCaptain = True

    #random sticks     
    rng = random.randint(1,100)
    #stick = discord.utils.get(message.guild.emojis, name='corgistick') 
    stick = client.get_emoji(735827082151723029)
    lurk = client.get_emoji(736190606254145548)
    if rng == 50:        
        if stick:
            await message.add_reaction(stick)
    
    if rng == 100:        
        image = directory + "/Images/corgilurk.gif"
        await message.channel.send(file=discord.File(image))

    if "corgistick" in message.content:
        response = "No take! *Only* throw."
        await message.channel.send(response.format(message))

    if message.clean_content.lower() == "time for bed @corgi":
        response = "*Stretches and gets into bed.*"
        await message.channel.send(response.format(message))
        sys.exit()
        return

    if message.content.lower() == "how i throw":
        rules = throwrules()
        for rule in rules:
            await message.channel.send(rule.format(message))
        return

    if message.content.lower() == "how i slam":
        rules = slamrules()
        for rule in rules:
            await message.channel.send(rule.format(message))
        return

    for mentions in message.mentions:
        if mentions.id == message.guild.me.id:
            await message.channel.send("Woof?")
            break;

    if message.content.lower() == ("$github"):
        response = "You can find my master's github here: https://github.com/LarnuUK"
        await message.channel.send(response.format(message))
        return

    if message.content.lower() == "$timezones":
        response = ""
        embed = discord.Embed(title="Available Timezones", description="Timezones available for the `$CEST` command", color=colourings["dark gold"])
        for tz in timezones:
            tzdata = timezones[tz]
            tzname = tzdata["Name"]
            tzoffset = tzdata["Offset"]
            #tzhours = tzdata["Hours"]
            #tzminutes = tzdata["Minutes"]
            if tzoffset < 0:
                offset = str(tzoffset)
            else:
                offset = "+" + str(tzoffset)
            response = response + "\n**" + tz + "**: " + tzname + " (UTC " + offset + ")"
            #embed.add_field(name=tz, value=tzname + " (UTC" + offset + ")", inline=False)
        # await message.channel.send(response.format(message))
        embed.add_field(name="Timezones", value=response, inline=False)
        await message.channel.send(embed=embed)
        return

    """
    #We don't need this any more
    if message.content.lower().startswith("$cest "):
        time = message.content[6:11]
        hours = message.content[6:8]
        minutes = message.content[9:11]
        timezone = message.content.upper()[12:]
        if re.match("[0-9][0-9]:[0-5][0-9]",time):
            try:
                offset = timezones[timezone]
            except:
                response = "Invalid or unrecognised timezone. Use $Timezones for a full list of timezones I can convert from CEST."
                await message.channel.send(response.format(message))
                return
            newhours = int(hours) - 2 + int(offset["Offset"])
            day = ""
            if not(int(offset["Offset"]) == offset["Offset"]):
                newminutes = int(minutes) + 30
            else:
                newminutes = int(minutes)
            if newminutes > 59:
                newminutes = newminutes - 30
                newhours = newhours + 1
            elif newminutes < 0:
                newminutes = newminutes + 30
                newhours = newhours - 1
            if newhours > 23:
                newhours = newhours - 24
                day = " (+1 day)"
            elif newhours < 0:
                newhours = newhours + 24
                day = " (-1 day)"
            response = time + " CEST is " +  ("00" + str(newhours))[-2:] + ":" + ("00" + str(newminutes))[-2:] + " " + timezone + day + "."
            await message.channel.send(response.format(message))
        else:
            response = "Invalid Time format. Must be in format `hh:mm`."
            await message.channel.send(response.format(message))
        return
    """

    if message.content.lower().startswith("$") and validatetz(message.content.upper()[1:message.content.index(" ")]):
        spaceindex = message.content.index(" ")
        sourcetz = message.content.upper()[1:spaceindex]
        time = message.content[spaceindex+1:spaceindex+6]
        hours = message.content[spaceindex+1:spaceindex+3]
        minutes = message.content[spaceindex+4:spaceindex+6]
        desttz = message.content.upper()[spaceindex+7:]
        if re.match("[0-9][0-9]:[0-5][0-9]",time):
            try:
                tzdestination = timezones[desttz]
                tzsource = timezones[sourcetz]
            except:
                response = "Invalid or unrecognised timezone. Use $Timezones for a full list of timezones I can convert from CEST."
                await message.channel.send(response.format(message))
                return
            tzdesthours = tzdestination["Hours"]
            tzdestminutes = tzdestination["Minutes"]
            tzdestname = tzdestination["Name"]
            tzsourcehours = tzsource["Hours"]
            tzsourceminutes = tzsource["Minutes"]
            tzsourcename = tzsource["Name"]
            newhours = int(hours) - tzsourcehours + tzdesthours
            newminutes = int(minutes) - tzsourceminutes + tzdestminutes
            day = ""
            if newminutes > 59:
                newminutes = newminutes - 30
                newhours = newhours + 1
            elif newminutes < 0:
                newminutes = newminutes + 30
                newhours = newhours - 1
            if newhours > 23:
                newhours = newhours - 24
                day = " (+1 day)"
            elif newhours < 0:
                newhours = newhours + 24
                day = " (-1 day)"
            response = time + " " + sourcetz + " (" + tzsourcename + ") is " +  ("00" + str(newhours))[-2:] + ":" + ("00" + str(newminutes))[-2:] + " " + desttz +" (" + tzdestname + ")" + day + "."
            await message.channel.send(response.format(message))
        else:
            response = "Invalid Time format. Must be in format `hh:mm`."
            await message.channel.send(response.format(message))
        return

    if message.content.lower() == ("$roll"):
        i = random.randint(1,6)
        response = "You rolled a " + str(i) + " {0.author.mention}."
        await message.channel.send(response.format(message))
        return

    if message.content.lower().startswith("$roll "):
        dice = message.content[6:]
        if re.match("[0-9]+d[0-9]+",dice):
            die = int(dice[0:dice.find("d")])
            sides = int(dice[dice.find("d")+1:])
            if die > 20:
                response = "Cannot roll more than 20 die at a time."
                await message.channel.send(response.format(message))
            elif sides > 100 or sides < 1:
                response = "Sides cannot be greater than 100."
                await message.channel.send(response.format(message))
            else:
                rolls = []
                r = 0
                total = 0
                rollstr = ""
                while r < die:
                    i = random.randint(1,sides)
                    rolls.append(i)
                    total = total + i
                    rollstr = rollstr + ", " + str(i)
                    r = r+1
                response = "You rolled a total of " + str(total) + " {0.author.mention}: (" + rollstr[2:] + ")"
                await message.channel.send(response.format(message))
            return
        else:
            response = "Unrecognised die format. Use `{{n}}d{{s}}`. For example 2d6 or 1d3."
            await message.channel.send(response.format(message))
            return

    if message.content.lower() == ("$flip"):
        i = random.randint(0,1)
        if i == 0:
            response = "It's Heads!"
        else:
            response = "It's Tails!"
        await message.channel.send(response.format(message))
        return

    #Find Bot-logs channel. There is probably a better way than this though.
    for channel in message.guild.channels:
        if channel.name == "corgi-logs":
            logchannel = channel
            break

    #Timer commands
    if message.content.lower() == "$timer":
        await message.channel.send("The $timer command must be followed by a time period, and optionally a reason. For example: `$timer 03:00` will set a timer for 3 hours. If you wish, you can include a reason afterwards. For example: `$timer 01:30 Ryan and Thom's game` will set a timer for 1 hour 30 minutes with the reason *\"Ryan and Thom's game\"*.")
        return

    if message.content.lower().startswith("$timer "):
        timer = message.content[7:12]
        hours = message.content[7:9]
        minutes = message.content[10:12]
        seconds = "00"
        reason = message.clean_content[13:]
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

        if message.content.lower() == "$rolestats":
            if isCommittee == False and isHeadJudge == False:
                await message.channel.send("Only Committee members can use that command.")
            else:
                embed = discord.Embed(title="Role Statistics", color=discord.Colour.green())
                guild = message.guild
                guildroles = guild.roles
                members = guild.members
                for guildrole in guildroles:
                    print("Getting count for " + guildrole.name)
                    membercount = 0
                    for member in members:
                        for memberrole in member.roles:
                            if memberrole.name == guildrole.name:
                                membercount += 1
                    embed.add_field(name=guildrole.name, value=membercount, inline=False)
                now = datetime.utcnow()
                embed.set_footer(text="Reported: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                await logchannel.send(embed=embed)
                response = "Role stats have been sent to the Log Channel"
                await message.channel.send(response.format(message))
                    
            return

        if message.content.lower() == "$colours":
            response = "You can choose from any of the following colours: *" + ", ".join(colours) + "*. Alternatively you can use random for a random colour, or provide your own 6 digit hex code."
            await message.channel.send(response.format(message))
            return

        #Give someone the Team Captain Rank
        if message.content.lower().startswith("$addcaptain"):
            if isCommittee == False and isHeadJudge == False:
                await message.channel.send("Only Committee members can use that command.")
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to give Team Captain role.")
            elif len(message.mentions[0].roles) > 1:
                await message.channel.send("User already has a server role and cannot be made a captain.")
            else:
                role = discord.utils.get(message.guild.roles, name="Team Captain")
                await message.mentions[0].add_roles(role)
                response = "{0.mentions[0].display_name} has been given the Team Captain Role."
                await message.channel.send(response.format(message))
                dm = """Hi, you've been given the Team Captain role in the Warmachine and Hordes Virtual Team Championship!

To get started, you'll want to create your team using the `$teamname` command in the bot-commands channel. Once you've done that, you'll have access to all the table channels, and your team will have it's own channel category created. If you''re not completely decided on a name yet, don't worry, you can change it again later using the same command.

Once your team has been created, you can start adding people to the team using the `$addplayer` command. You can also choose the colour of your team's role using $teamcolour. To get your team members in the server, please use this link: https://discord.gg/Xq7fwjF

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
        
        #Remove Captain Role from a User
        if message.content.lower().startswith("$removecaptain"):
            if isCommittee == False and isHeadJudge == False:
                await message.channel.send("Only Committee members can use that command.")
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to give Team Captain role.")
            elif len(message.mentions[0].roles) > 2:
                if message.mentions[0].roles[1].name == "Team Captain":
                    teamrole = message.mentions[0].roles[2]
                else:
                    teamrole = message.mentions[0].roles[1]
                response = "User has already created a Team. Do you want to delete the team, or make a different member of the Team the captain? To delete the team, respond with \"`DELETE " + teamrole.name.upper() + "`\" (*this action cannot be undone*). To change the captain to a different member, please ping the new captain."
                await message.channel.send(response.format(message))
                def sameuserchannel(m):
                    return m.channel == message.channel and m.author == message.author
                reply = await client.wait_for('message',check=sameuserchannel)
                if reply.content == "DELETE " + teamrole.name.upper():
                    response = "Deleting Team " + teamrole.name + "."
                    await message.channel.send(response.format(message))
                    guildcategories = message.guild.categories
                    for category in guildcategories:
                        if category.name.lower() == teamrole.name.lower():
                            channels = category.channels
                            for channel in channels:
                                await channel.delete()
                            await category.delete()
                            break
                    response = "The team " + teamrole.name + " has been deleted."
                    await message.channel.send(response.format(message))
                    colour = teamrole.color
                    embed = discord.Embed(title="Team Deleted", color=colour) #description=message.mentions[0].display_name
                    embed.add_field(name="Removed By", value=message.author.display_name, inline=False)
                    embed.add_field(name="Removed ID", value=message.author.id, inline=False)
                    embed.add_field(name="Team Name", value=teamrole.name, inline=False)
                    now = datetime.utcnow()
                    embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                    await logchannel.send(embed=embed)
                    await teamrole.delete()
                    role = discord.utils.get(message.guild.roles, name="Team Captain")
                    await message.mentions[0].remove_roles(role)
                    response = "{0.mentions[0].display_name} has been removed from the Team Captain Role."
                    await message.channel.send(response.format(message))
                    embed = discord.Embed(title="Remove Team Captain", color=0xa551be) #description=message.mentions[0].display_name
                    embed.add_field(name="Removed By", value=message.author.display_name, inline=False)
                    embed.add_field(name="Removed ID", value=message.author.id, inline=False)
                    embed.add_field(name="Captain Removed", value=message.mentions[0].display_name, inline=False)
                    embed.add_field(name="Captain ID", value=message.mentions[0].id, inline=False)
                    now = datetime.utcnow()
                    embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                    await logchannel.send(embed=embed)
                elif len(reply.mentions) == 1:
                    inteam = False;
                    for replyrole in reply.mentions[0].roles:
                        if replyrole.name == teamrole.name:
                            inteam = True;
                            break
                    if inteam == True:
                        response = "{0.mentions[0].display_name} has been removed from the Team Captain Role."
                        await message.channel.send(response.format(message))
                        role = discord.utils.get(message.guild.roles, name="Team Captain")
                        await message.mentions[0].remove_roles(role)
                        response = "{0.mentions[0].display_name} has been removed from the Team Captain Role."
                        embed = discord.Embed(title="Remove Team Captain", color=0xa551be) #description=message.mentions[0].display_name
                        embed.add_field(name="Removed By", value=message.author.display_name, inline=False)
                        embed.add_field(name="Removed ID", value=message.author.id, inline=False)
                        embed.add_field(name="Captain Removed", value=message.mentions[0].display_name, inline=False)
                        embed.add_field(name="Captain ID", value=message.mentions[0].id, inline=False)
                        now = datetime.utcnow()
                        embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                        await logchannel.send(embed=embed)
                        response = reply.mentions[0].display_name + " has been added to the Team Captain Role."
                        await message.channel.send(response.format(message))
                        await reply.mentions[0].add_roles(role)
                        embed = discord.Embed(title="Add Team Captain", color=0xa551be) #description=message.mentions[0].display_name
                        embed.add_field(name="Added By", value=message.author.display_name, inline=False)
                        embed.add_field(name="Added ID", value=message.author.id, inline=False)
                        embed.add_field(name="Captain Added", value=reply.mentions[0].display_name, inline=False)
                        embed.add_field(name="Captain ID", value=reply.mentions[0].id, inline=False)
                        now = datetime.utcnow()
                        embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                        await logchannel.send(embed=embed)
                    else:
                        response = "User is not in the same team. YOu can only promote a member in the same team. Aborted removing {0.mentions[0].display_name} from the Team Captain Role."
                        await message.channel.send(response.format(message))
                else:
                    response = "Aborted removing {0.mentions[0].display_name} from the Team Captain Role."
                    await message.channel.send(response.format(message))
            else:
                role = discord.utils.get(message.guild.roles, name="Team Captain")
                await message.mentions[0].remove_roles(role)
                response = "{0.mentions[0].display_name} has been removed from the Team Captain Role."
                embed = discord.Embed(title="Remove Team Captain", color=0xa551be) #description=message.mentions[0].display_name
                embed.add_field(name="Removed By", value=message.author.display_name, inline=False)
                embed.add_field(name="Removed ID", value=message.author.id, inline=False)
                embed.add_field(name="Captain Removed", value=message.mentions[0].display_name, inline=False)
                embed.add_field(name="Captain ID", value=message.mentions[0].id, inline=False)
                now = datetime.utcnow()
                embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                await logchannel.send(embed=embed)
            return

        #Give someone the Judge Rank
        if message.content.lower().startswith("$addjudge"):
            if isCommittee == False:
                await message.channel.send("Only Committee members can use that command.")
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to give Judge role.")
            else:
                roles = message.mentions[0].roles
                inteam = False
                for role in roles:
                    if role.name.lower() == "judge":
                        await message.channel.send("User is already a Judge...")    
                        return
                    elif role.name.lower() not in ("head judge","vtc committee","@everyone"):
                        inteam = True
                        break
                if inteam == True:
                    await message.channel.send("User is in a team and cannot be made a Judge.")
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
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to give Head Judge role.")
            else:
                roles = message.mentions[0].roles
                inteam = False
                for role in roles:
                    if role.name.lower() == "head judge":
                        await message.channel.send("User is already a Head Judge...")    
                        return
                    elif role.name.lower() not in ("judge","vtc committee","@everyone"):
                        inteam = True
                        break
                if inteam == True:
                    await message.channel.send("User is in a team and cannot be made a Judge.")
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
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to give Streamer role.")
            elif len(message.mentions[0].roles) > 1:
                await message.channel.send("User already has a server role and cannot be made a Streamer.")
            else:
                role = discord.utils.get(message.guild.roles, name="Streamer")
                await message.mentions[0].add_roles(role)
                response = "{0.mentions[0].display_name} has been given the Streamer Role."
                await message.channel.send(response.format(message))
                #Log details
                embed = discord.Embed(title="Add Streamer", color=0x9147ff) 
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
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to remove Streamer role.")
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
                if len(teamname.replace(" ","")) == 0:
                    response = "You need a name for your team, you silly!"
                    await message.channel.send(response)
                    return
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
                        break #Don't forget to get rid of this if we expand in the future.
                    #elif guildrole.name == "VTC Committee":
                    #    CommitteeRole = guildrole
                    #elif guildrole.name == "Judge":
                    #    JudgeRole = guildrole
                    #elif guildrole.name == "Head Judge":
                    #    HeadJudgeRole = guildrole
                guildcategories = guild.categories
                for category in guildcategories:
                    if category.name.lower() == teamname.lower():
                        response = "A category with the name " + category.name +" already exists. Please choose a different name."
                        await message.channel.send(response)
                        return
                #Check Team Captain is already in a Team
                if len(message.author.roles) == 2:
                    newrole = await guild.create_role(name=teamname, hoist=True)
                    colour = int("0x"+str(randomcolour()),16)
                    await newrole.edit(colour=discord.Colour(colour))
                    await newrole.edit(position=2) 
                    await CaptainRole.edit(position=1)
                    response = "Created role " + teamname +"."
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
                    await newcategory.edit(position=6) 
                    botrole = discord.utils.get(message.guild.roles, name="Bots")
                    talkrights = {guild.default_role: discord.PermissionOverwrite(read_messages=False),botrole: discord.PermissionOverwrite(read_messages=True)}
                    newtalk = await guild.create_text_channel(name="Team Chat",category=newcategory,overwrites=talkrights)
                    await newtalk.set_permissions(newrole, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True)
                    await newtalk.set_permissions(CaptainRole, manage_messages=True)
                    #await newtalk.set_permissions(CommitteeRole, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True)
                    #await newtalk.set_permissions(HeadJudgeRole, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True)
                    chatrights = {guild.default_role: discord.PermissionOverwrite(view_channel=False)}
                    newchat = await guild.create_voice_channel(name="Team Talk",category=newcategory,overwrites=chatrights)
                    await newchat.set_permissions(newrole,view_channel=True,connect=True,speak=True)
                    #await newchat.set_permissions(CommitteeRole,view_channel=True,connect=True,speak=True)
                    #await newchat.set_permissions(HeadJudgeRole,view_channel=True,connect=True,speak=True)
                    await message.channel.send("New Team created.")
                    #Log details
                    embed = discord.Embed(title="Create New Team", color=colour) 
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
            else:
                teamcolour = message.content[12:].lower()
                if len(message.author.roles) == 2:
                    await message.channel.send("You need to have created your team before you can set their colour.")
                elif message.content.lower() == "$teamcolour":
                    await message.channel.send("You must supply a colour. Either provide a colour hex, ask for a random colour, or use one of the preprogrammed colours. See `$colours` or <https://htmlcolorcodes.com/color-picker/> for ideas.")
                elif not re.match("[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]",teamcolour) and colours.count(teamcolour) == 0 and not teamcolour == "random":
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
                    elif teamcolour == "random":
                        colour = int("0x"+str(randomcolour()),16)
                        await teamrole.edit(colour=discord.Colour(colour))
                        embed = discord.Embed(title="Change Team Colour", color=colour) 
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
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to give Team role.")
            elif len(message.mentions[0].roles) > 1:
                await message.channel.send("User already has a server role and cannot be added to a team.")
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
                embed.add_field(name="Team Name", value=teamrole.name, inline=False)
                embed.add_field(name="Added By", value=message.author.display_name, inline=False)
                embed.add_field(name="Added ID", value=message.author.id, inline=False)
                embed.add_field(name="New Player", value=message.mentions[0].display_name, inline=False)
                embed.add_field(name="NewID", value=message.mentions[0].id, inline=False)
                now = datetime.utcnow()
                embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                await logchannel.send(embed=embed)
            return

        if message.content.lower().startswith("$removeplayer"):
            if isCaptain == False:
                await message.channel.send("Only Team Captains can use that command.")
            elif len(message.mentions) == 0:
                await message.channel.send("Needs a user to remove Team role.")
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
            return

        if message.content.lower() == "$openserver":
            if isThom == False:
                await message.channel.send("Only Thom can use that command.")
            else:
                #get everyone role
                guild = message.guild
                for role in guild.roles:
                    if role.name == "@everyone":
                        everyone = role
                        break
                await message.channel.send("Setting table permissions... Please hold.")
                guildchannels = guild.channels
                for guildchannel in guildchannels:
                        print(guildchannel.name)
                        if guildchannel.type.name == "text" and "game" in guildchannel.name.lower():
                            print("Setting read and send message permissions")
                            await guildchannel.set_permissions(everyone, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True,add_reactions=True)
                        elif guildchannel.type.name == "voice" and "game" in guildchannel.name.lower():
                            print("Setting connect and speak permissions")
                            await guildchannel.set_permissions(everyone,view_channel=True,connect=True,speak=True)
                await message.channel.send("Server is now open to everyone.")
                embed = discord.Embed(title="Open Server to Public", color=0x22cc22) 
                embed.add_field(name="Opened By", value=message.author.display_name, inline=False)
                embed.add_field(name="Opened ID", value=message.author.id, inline=False)
                now = datetime.utcnow()
                embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                await logchannel.send(embed=embed)
            return

        if message.content.lower() == "$closeserver":
            if isThom == False:
                await message.channel.send("Only Thom can use that command.")
            else:
                #get everyone role
                guild = message.guild
                for role in guild.roles:
                    if role.name == "@everyone":
                        everyone = role
                        break
                await message.channel.send("Setting table permissions... Please hold.")
                guildchannels = guild.channels
                for guildchannel in guildchannels:
                    if guildchannel.name.lower().startswith('table') and not guildchannel.name.lower().endswith('chat') and not guildchannel.name.lower().endswith('talk'):
                        print(guildchannel.name)
                        if guildchannel.type.name == "text" and "game" in guildchannel.name.lower():
                            print("Setting read and send message permissions")
                            await guildchannel.set_permissions(everyone, read_messages=False, send_messages=False, embed_links=False, attach_files=False, read_message_history=False, use_external_emojis=False,add_reactions=False)
                        elif guildchannel.type.name == "voice" and "game" in guildchannel.name.lower():
                            print("Setting connect and speak permissions")
                            await guildchannel.set_permissions(everyone,view_channel=False)
                await message.channel.send("Server is now closed to everyone.")
                embed = discord.Embed(title="Close Server to Public", color=0xcc2222) 
                embed.add_field(name="Opened By", value=message.author.display_name, inline=False)
                embed.add_field(name="Opened ID", value=message.author.id, inline=False)
                now = datetime.utcnow()
                embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                await logchannel.send(embed=embed)
            return

        if message.content.lower() == "$limitvcs":
            if isThom == False:
                await message.channel.send("Only Thom can use that command.")
            else:
                await message.channel.send("Limiting Game VCs to 4 users.")
                guild = message.guild
                guildchannels = guild.channels
                for guildchannel in guildchannels:
                    if guildchannel.name.lower().startswith('table'):
                        print(guildchannel.name)
                        if guildchannel.type.name == "voice" and "game" in guildchannel.name.lower():
                            print("Changing max connected users.")
                            await guildchannel.edit(user_limit=4)
                await message.channel.send("Game VCs are now limited to 4 users.")
                embed = discord.Embed(title="Limit Game VC Connections", color=colourings["orange"]) 
                embed.add_field(name="Limited By", value=message.author.display_name, inline=False)
                embed.add_field(name="Limiting ID", value=message.author.id, inline=False)
                now = datetime.utcnow()
                embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                await logchannel.send(embed=embed)
            return

        if message.content.lower() == "$unlimitvcs":
            if isThom == False:
                await message.channel.send("Only Thom can use that command.")
            else:
                await message.channel.send("Removing Limit on Game VCs.")
                guild = message.guild
                guildchannels = guild.channels
                for guildchannel in guildchannels:
                    if guildchannel.name.lower().startswith('table'):
                        print(guildchannel.name)
                        if guildchannel.type.name == "voice" and "game" in guildchannel.name.lower():
                            print("Changing max connected users.")
                            await guildchannel.edit(user_limit=0)
                await message.channel.send("Game VCs can now have unlimited users.")
                embed = discord.Embed(title="Unlimit Game VC Connections", color=colourings["gold"]) 
                embed.add_field(name="Unlimited By", value=message.author.display_name, inline=False)
                embed.add_field(name="Unlimiting ID", value=message.author.id, inline=False)
                now = datetime.utcnow()
                embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                await logchannel.send(embed=embed)
            return
                            

client.run(key)