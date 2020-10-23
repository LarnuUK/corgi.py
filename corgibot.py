#!/usr/bin/env python3
import discord, discord.utils, random, os, re, json, sys, time, secrets, pyodbc
from os import path
from datetime import datetime, timedelta
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

from rulewordings import throwrules, slamrules
import pairings
import access
import teams 
import events

directory = os.path.dirname(os.path.realpath(__file__))

load_dotenv()
key = os.getenv('DISCORD_KEY')
status = os.getenv('DISCORD_STATUS')
owner = os.getenv('DISCORD_OWNER')
debugon = os.getenv('DEBUG')

#SQLServer = os.getenv('SQL_SERVER')
#SQLDatabase = os.getenv('SQL_DATABASE')
#SQLLogin = os.getenv('SQL_LOGIN')
#SQLPassword = os.getenv('SQL_PASSWORD')
#
#SQLConnString = 'Driver={ODBC Driver 17 for SQL Server};Server=' + SQLServer+ ';Database=' + SQLDatabase + ';UID='+ SQLLogin +';PWD=' + SQLPassword
#
#sqlConn = pyodbc.connect(SQLConnString)

#Bad way to do it, I know.
colours = ["default","teal","dark teal","green","dark green","blue","dark blue","purple","dark purple","magenta","dark magenta","gold","dark gold","orange","dark orange","red","dark red","lighter grey", "dark grey", "light grey", "darker grey", "blurple", "greyple"]
colourings = {"default":discord.Colour.default(),"teal":discord.Colour.teal(),"dark teal":discord.Colour.dark_teal(),"green":discord.Colour.green(),"dark green":discord.Colour.dark_green(),"blue":discord.Colour.blue(),"dark blue":discord.Colour.dark_blue(),"purple":discord.Colour.purple(),"dark purple":discord.Colour.dark_purple(),"magenta":discord.Colour.magenta(),"dark magenta":discord.Colour.dark_magenta(),"gold":discord.Colour.gold(),"dark gold":discord.Colour.dark_gold(),"orange":discord.Colour.orange(),"dark orange":discord.Colour.dark_orange(),"red":discord.Colour.red(),"dark red":discord.Colour.dark_red(),"lighter grey":discord.Colour.lighter_grey(),"dark grey":discord.Colour.dark_grey(),"light grey":discord.Colour.light_grey(),"darker grey":discord.Colour.darker_grey(),"blurple":discord.Colour.blurple(),"greyple":discord.Colour.greyple()}

timezones = {"PST":{"Name":"Pacific Standard Time", "Offset":-8, "Hours":-8, "Minutes":0},"PDT":{"Name":"Pacific Daylight Time", "Offset":-7, "Hours":-8, "Minutes":0},
             "MST":{"Name":"Mountain Standard Time", "Offset":-7, "Hours":-7, "Minutes":0},"MDT":{"Name":"Mountain Daylight Time", "Offset":-6, "Hours":-6, "Minutes":0},
             "CST":{"Name":"Central Standard Time", "Offset":-6, "Hours":-6, "Minutes":0},"CDT":{"Name":"Central Daylight Time", "Offset":-5, "Hours":-5, "Minutes":0},
             "EST":{"Name":"Eastern Standard Time", "Offset":-5, "Hours":-5, "Minutes":0},"EDT":{"Name":"Eastern Daylight Time", "Offset":-4, "Hours":-4, "Minutes":0},
             "UTC":{"Name":"Universal Time Constant", "Offset":0, "Hours":$addeventdetail
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
    if not(debugon is None):
        print('Message from {0.author}: {0.content}'.format(message))

    if message.channel.type == discord.ChannelType.private:
        return

    serverRoles = message.guild.roles

    roles = message.author.roles

    ##This is the old way

    ##isCommittee = False
    ##isCaptain = False
    ##isJudge = False
    ##isThom = False
    ##for role in roles:
    ##    #As people, by design, can't have multiple rules, then we can safely break and not loop around 40~ roles
    ##    if role.name == "Thom":
    ##        isThom = True
    ##    if role.name == "VTC Committee" or role.name == "Thom":
    ##        isCommittee = True
    ##    if role.name == "Head Judge":
    ##        isHeadJudge = True
    ##    if role.name == "Judge":
    ##        isJudge = True
    ##    if role.name == "Team Captain":
    ##        isCaptain = True

    #random sticks     
    rng = random.randint(1,500)
    stick = client.get_emoji(735827082151723029)
    #print("Random Number was: " + str(rng))
    if rng % 50 == 0:        
        if stick:
            await message.add_reaction(stick)
    
    if rng == 100:        
        image = directory + "/images/corgilurk.gif"
        await message.channel.send(file=discord.File(image))

    if "corgistick" in message.content:
        response = "No take! *Only* throw."
        await message.channel.send(response.format(message))

    if "wednesday" in message.content.lower():
        day_name= ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"]
        day = datetime.utcnow().weekday()
        if day_name[day] == "Wednesday":
            image = directory + "/images/wednesday.jpg"
            await message.channel.send(file=discord.File(image))

    if message.clean_content.lower() == "time for bed @corgi" and message.author.id == owner:
        response = "*Stretches and gets into bed.*"
        await message.channel.send(response.format(message))
        sys.exit()
        return

    if message.content.lower() == "$help":
        response = "Please visit the following link for help on my available commands: <https://fishcord.larnu.uk/corgi-help/>"
        await message.channel.send(response.format(message))
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
            break

    if message.content.lower() == ("$github"):
        response = "You can find my master's github here: https://github.com/LarnuUK"
        await message.channel.send(response.format(message))
        return

    if message.content.lower() == "$timezones":
        response = ""
        embed = discord.Embed(title="Available Timezones", description="Timezones available for the conversion commands (such as `$CEST` and `$NZDT`)", color=colourings["dark gold"])
        for tz in timezones:
            tzdata = timezones[tz]
            tzname = tzdata["Name"]
            tzoffset = tzdata["Offset"]
            if tzoffset < 0:
                offset = str(tzoffset)
            else:
                offset = "+" + str(tzoffset)
            response = response + "\n**" + tz + "**: " + tzname + " (UTC " + offset + ")"
        embed.add_field(name="Timezones", value=response, inline=False)
        await message.channel.send(embed=embed)
        return

    if message.content.lower().startswith("$") and " " in message.content:
        if validatetz(message.content.upper()[1:message.content.index(" ")]):
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
            import time
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
        response = "The $heret command must be followed by a time period and a reason. For example: `$heret 03:00 dice down` will set a timer for 3 hours the reason *\"dice down\"*."
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
        if access.isowner(message.guild,message.author) or access.isadmin(message.guild,message.author) or access.isheadjudge(message.guild,message.author): 
            
            if re.match("[0-9][0-9]:[0-5][0-9]",timer):
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
                import time
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
                embed.set_field_at(1,name="Remaining", value="`00:00:00`", inline=True) 
                await timermsg.edit(embed=embed)
                response = "".join(["@here , the timer has finished! ", reason]).format(message)
                await message.channel.send(response)
            else:
                await message.channel.send("That isn't a valid time!")
        else:
            await message.channel.send("You must be a Judge to use Here Timers.")
        return

    if message.content.lower().startswith("$germanpairing"):
        if str(message.channel).lower().startswith("table"):
            if len(message.mentions) == 1:
                await pairings.german(client,message)
            else:
                response = "You must mention your opponent to begin a pairing process."
                await message.channel.send(response.format(message))
        else:
            response = "You can only use this command in a table channel."
            await message.channel.send(response.format(message))
        return

    if message.content.lower() == "$events":
        await events.events(message)
        return

    if message.content.lower().startswith("$eventdetails"):
        if not(message.content[14:].isdecimal()):
            response = "Invalid event ID."
            await message.channel.send(response.format(message))
            return
        await events.eventdetails(message,message.content[14:])
        return

    #Want these commands in the right channel
    if str(message.channel).lower().startswith("bot"):

        if message.content.lower().startswith("$addroleaccess"):
            await access.addaccess(client,message)
            return
        
        if message.content.lower().startswith("$removeroleaccess"):
            await access.removeaccess(message)
            return
        
        if message.content.lower().startswith("$checkroleaccess"):
            await access.checkaccess(message)
            return

        if message.content.lower() == "$colours":
            response = "You can choose from any of the following colours: *" + ", ".join(colours) + "*. Alternatively you can use *random* for a random colour, or provide your own 6 digit hex code."
            await message.channel.send(response.format(message))
            return

        if message.content.lower().startswith("$addcaptain"):
            await teams.addcaptain(message)
            return

        if message.content.lower().startswith("$addeventdetail"):
            await events.adddetail(client,message)
            return

        if message.content.lower().startswith("$addevent"):
            await events.addevent(client,message)
            return

        if message.content.lower().startswith("$editevent"):
            await events.editevent(client,message)
            return        

        if message.content.lower().startswith("$deleteevent"):
            await events.deleteevent(client,message)
            return        

        if message.content.lower().startswith("$deletedetail"):
            await events.deletedetail(client,message)
            return

        if message.content.lower().startswith("$createteam"):
            await teams.createteam(message)
            return

        if message.content.lower().startswith("$registerteam"):
            await teams.registerteam(client,message)
            return

        if message.content.lower().startswith("$deregisterteam"):
            await teams.deregisterteam(client,message)
            return

        if message.content.lower().startswith("$addplayer"):
            await teams.addplayer(client,message)
            return

        if message.content.lower().startswith("$removeplayer"):
            await teams.removeplayer(client,message)
            return

        if message.content.lower().startswith("$teamcolour"):
            await teams.changecolour(client,message)
            return

        if message.content.lower().startswith("$renameteam"):
            await teams.renameteam(client,message)
            return

        if message.content.lower() == "$deleteteam":
            await teams.deleteteam(client,message)
            return

        if message.content.lower() == "$leaveteam":
            await teams.leaveteam(client,message)
            return

        if message.content.lower().startswith("$assigncaptain"):
            await teams.assigncaptain(client,message)
            return

        if message.content.lower().startswith("$removecaptain"):
            await teams.removecaptain(client,message)
            return

@client.event
async def on_guild_role_delete(role):
    await access.removeaccesslevel(role.guild,role)
    await teams.removeteam(role)

@client.event
async def on_member_remove(member):
    await teams.reassigncaptain(member,None)
    await teams.clearcaptain(member)

client.run(key)