import discord, discord.utils, random, os, re, json, sys, time, secrets, pyodbc
from datetime import datetime, timedelta
from dotenv import load_dotenv

from access import isowner, isadmin, isheadjudge, isjudge, iscaptain, getcaptain
from events import getevent

SQLServer = os.getenv('SQL_SERVER')
SQLDatabase = os.getenv('SQL_DATABASE')
SQLLogin = os.getenv('SQL_LOGIN')
SQLPassword = os.getenv('SQL_PASSWORD')

SQLConnString = 'Driver={ODBC Driver 17 for SQL Server};Server=' + SQLServer+ ';Database=' + SQLDatabase + ';UID='+ SQLLogin +';PWD=' + SQLPassword

sqlConn = pyodbc.connect(SQLConnString)
sqlConn2 = pyodbc.connect(SQLConnString)

colours = ["default","teal","dark teal","green","dark green","blue","dark blue","purple","dark purple","magenta","dark magenta","gold","dark gold","orange","dark orange","red","dark red","lighter grey", "dark grey", "light grey", "darker grey", "blurple", "greyple"]
colourings = {"default":discord.Colour.default(),"teal":discord.Colour.teal(),"dark teal":discord.Colour.dark_teal(),"green":discord.Colour.green(),"dark green":discord.Colour.dark_green(),"blue":discord.Colour.blue(),"dark blue":discord.Colour.dark_blue(),"purple":discord.Colour.purple(),"dark purple":discord.Colour.dark_purple(),"magenta":discord.Colour.magenta(),"dark magenta":discord.Colour.dark_magenta(),"gold":discord.Colour.gold(),"dark gold":discord.Colour.dark_gold(),"orange":discord.Colour.orange(),"dark orange":discord.Colour.dark_orange(),"red":discord.Colour.red(),"dark red":discord.Colour.dark_red(),"lighter grey":discord.Colour.lighter_grey(),"dark grey":discord.Colour.dark_grey(),"light grey":discord.Colour.light_grey(),"darker grey":discord.Colour.darker_grey(),"blurple":discord.Colour.blurple(),"greyple":discord.Colour.greyple()}

greenTick = "✅"
greenCross = "❎"
digitemojis = {1:"1️⃣",2:"2️⃣",3:"3️⃣",4:"4️⃣",5:"5️⃣",6:"6️⃣",7:"7️⃣",8:"8️⃣",9:"9️⃣",10:"🔟"}
emojidigits = {"1️⃣":1,"2️⃣":2,"3️⃣":3,"4️⃣":4,"5️⃣":5,"6️⃣":6,"7️⃣":7,"8️⃣":8,"9️⃣":9,"🔟":10}

def randomcolour():
    colour = secrets.token_hex(3)
    return colour

def getcaptainrole (guild):
    cursor = sqlConn.cursor()
    cursor.execute('EXEC corgi.GetServerCaptain ?;',guild.id)
    for row in cursor:
        return row[0]
    cursor.close()
    return None

def getteams (captain):
    cursor = sqlConn.cursor()
    cursor.execute('EXEC corgi.GetCaptainTeams ?;',captain.id)
    return cursor
    

async def addcaptain (message):
    if isowner(message.guild,message.author) or isadmin(message.guild,message.author) or isheadjudge(message.guild,message.author):
        if len(message.mentions) == 1:
            teamcaptainrole = getcaptainrole(message.guild)
            if teamcaptainrole is None:
                response = "A role has not yet been given the Team Captain Access Level. Please give a role Team Captain Access using the `$AddRoleAccess` command."
                await message.channel.send(response.format(message))
                return
            teamcaptain = discord.utils.get(message.guild.roles, id=teamcaptainrole)
            await message.mentions[0].add_roles(teamcaptain)
            response = "{0.mentions[0].display_name} has been given the Team Captain Role."
            await message.channel.send(response.format(message))
            #Log details
            embed = discord.Embed(title="Add Team Captain", color=teamcaptain.colour) #description=message.mentions[0].display_name
            embed.add_field(name="Added By", value=message.author.display_name, inline=False)
            embed.add_field(name="Added ID", value=message.author.id, inline=False)
            embed.add_field(name="Captain Added", value=message.mentions[0].display_name, inline=False)
            embed.add_field(name="Captain ID", value=message.mentions[0].id, inline=False)
            now = datetime.utcnow()
            embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
            logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
            await logchannel.send(embed=embed)
        else:
            response = "You need to mention a user to give the Team Captain Role to."
            await message.channel.send(response.format(message))
    return

async def createteam(message):
    if iscaptain(message.guild,message.author):
        if message.content[12:] == "":
            response = "No team name was supplied."
            await message.channel.send(response.format(message))
            return
        teamname = message.content[12:]
        team = discord.utils.get(message.guild.roles, name=teamname)
        category = discord.utils.get(message.guild.categories, name=teamname)
        if not(team is None and category is None):
            response = "A team, role or category with that name already exists on the server. Please choose a different name."
            await message.channel.send(response.format(message))
            return
        newteam = await message.guild.create_role(name=teamname, hoist=True)
        colour = int("0x"+str(randomcolour()),16)
        await newteam.edit(colour=discord.Colour(colour))
        await newteam.edit(position=2) 
        captainroleID = getcaptain(message.guild)
        captainrole = discord.utils.get(message.guild.roles, id=captainroleID)
        await captainrole.edit(position=1)
        await message.author.add_roles(newteam)
        cursor = sqlConn.cursor()
        cursor.execute('EXEC corgi.CreateTeam ?, ?, ?, ?;',newteam.id,newteam.name,message.author.id,message.author.id)
        sqlConn.commit()
        cursor.close()
        response = "New team " + newteam.name +" created."
        await message.channel.send(response.format(message))
        embed = discord.Embed(title="New Team Created", color=colour) 
        embed.add_field(name="Created By", value=message.author.display_name, inline=False)
        embed.add_field(name="Created By ID", value=message.author.id, inline=False)
        embed.add_field(name="Team Name", value=newteam.name, inline=False)
        embed.add_field(name="Team ID", value=newteam.id, inline=False)
        now = datetime.utcnow()
        embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
        logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
        await logchannel.send(embed=embed)

    return

async def registerteam(client,message):
    def booleanResponse(r,u):
        return r.message.id == choice.id and u.id == message.author.id and r.emoji in ("✅","❎")
    def digitResponse(r,u):
        return r.message.id == choice.id and u.id == message.author.id and emojidigits[r.emoji] <= t
    if iscaptain(message.guild,message.author):
        if message.content[14:] == "":
            response = "No event id was supplied."
            await message.channel.send(response.format(message))
            return
        elif not(message.content[14:].isdecimal()):
            response = "Invalid event ID."
            await message.channel.send(response.format(message))
            return
        else:
            eventid = int(message.content[14:])
            events = getevent(message.guild,eventid)
            if events is None:
                response = "Invalid event ID; event does not exist."
                await message.channel.send(response.format(message))
                return
            for event in events:
                eventname = event[1]
                isteam = event[4]
                channels = event[5]
            events.close()
            if isteam == 0:
                response = "Event is not a team event. You cannot register teams for a team event."
                await message.channel.send(response.format(message))
                return
            teams = getteams(message.author)
            #Now because Python can't count we have to do dumb shit...
            t = 0
            teamids = []
            teamnames = []
            response = "What team do you want to register for the event " + eventname + "?"
            for team in teams:
                if discord.utils.get(message.guild.roles, id=team[0]):
                    t = t + 1
                    teamids.append(team[0])
                    teamnames.append(team[1])
                    response = response + "\n" + digitemojis[t] + ": " + team[1]                    
            teams.close()
            if t == 0:
                response = "You haven't created a team to register. Use the `$CreateTeam` command."
                await message.channel.send(response.format(message))
                return
            elif t == 1:
                response = "Register team" + teamnames[0] + " for " + eventname + "?"
                choice = await message.channel.send(response.format(message))
                await choice.add_reaction(greenTick)
                await choice.add_reaction(greenCross)
                try:
                    booleanrespond = await client.wait_for('reaction_add',check=booleanResponse,timeout=10)
                except:
                    response = "No response received. Registration cancelled."
                    await message.channel.send(response.format(message))
                    return                
                if booleanrespond[0].emoji == greenCross:
                    response = "Registration cancelled."
                    await message.channel.send(response.format(message))
                    return
                else:
                    teamid = teamids[0]
                    teamname = teamnames[0]
            else:
                choice = await message.channel.send(response.format(message))
                for d in range(0,t):
                    await choice.add_reaction(digitemojis[d+1])                
                try:
                    digitrespond = await client.wait_for('reaction_add',check=digitResponse,timeout=10)
                except:
                    response = "No response received. Registration cancelled."
                    await message.channel.send(response.format(message))
                    return
                teamid = teamids[emojidigits[digitrespond[0].emoji]-1]
                teamname = teamnames[emojidigits[digitrespond[0].emoji]-1]
            cursor = sqlConn.cursor()
            try:
                cursor.execute('EXEC corgi.RegisterTeam ?, ?;',eventid,teamid)
            except pyodbc.Error as ex:
                if ex.args[0] == '42000':
                    response = "A player in your team is already registered for the event on another Team. A player cannot be registered multiple times for the same event."
                if ex.args[0] == '23000':
                    response = "You are already registered for this event."
                await message.channel.send(response.format(message))
                return
            sqlConn.commit()
            cursor.close()
            response = "Team " + teamname + " has been registered for the event " + eventname + "."
            team = discord.utils.get(message.guild.roles, id=teamid)
            await message.channel.send(response.format(message))
            embed = discord.Embed(title="Team Registered for Event", color=team.colour) 
            embed.add_field(name="Registered By", value=message.author.display_name, inline=False)
            embed.add_field(name="Registered By ID", value=message.author.id, inline=False)
            embed.add_field(name="Team Name", value=team.name, inline=False)
            embed.add_field(name="Team ID", value=team.id, inline=False)
            embed.add_field(name="Event Name", value=eventname, inline=False)
            embed.add_field(name="Event ID", value=eventid, inline=False)
            now = datetime.utcnow()
            embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
            logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
            await logchannel.send(embed=embed)
            if channels == 1 and discord.utils.get(message.guild.categories, name=team.name) is None:
                response = "Event allows for creation of Team Channels. Creating channels."
                await message.channel.send(response.format(message))
                teamcategory = await message.guild.create_category(teamname)
                #await newcategory.edit(position=6)
                botrole = discord.utils.get(message.guild.roles, name="Bot")
                captainroleid = getcaptainrole(message.guild)
                captainrole = discord.utils.get(message.guild.roles, id=captainroleid)
                talkrights = {message.guild.default_role: discord.PermissionOverwrite(read_messages=False),botrole: discord.PermissionOverwrite(read_messages=True)}
                newtalk = await message.guild.create_text_channel(name="Team Chat",category=teamcategory,overwrites=talkrights)
                await newtalk.set_permissions(team, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True)
                await newtalk.set_permissions(captainrole, manage_messages=True)
                #await newtalk.set_permissions(CommitteeRole, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True)
                #await newtalk.set_permissions(HeadJudgeRole, read_messages=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, use_external_emojis=True)
                chatrights = {message.guild.default_role: discord.PermissionOverwrite(view_channel=False)}
                newchat = await message.guild.create_voice_channel(name="Team Talk",category=teamcategory,overwrites=chatrights)
                await newchat.set_permissions(team,view_channel=True,connect=True,speak=True)        
                response = "New Channels created."
                await message.channel.send(response.format(message))        
                embed = discord.Embed(title="Team channels created", color=team.colour) 
                embed.add_field(name="Team Name", value=team.name, inline=False)
                embed.add_field(name="Team ID", value=team.id, inline=False)
                now = datetime.utcnow()
                embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
                await logchannel.send(embed=embed)

async def deregisterteam(client,message):
    def booleanResponse(r,u):
        return r.message.id == choice.id and u.id == message.author.id and r.emoji in ("✅","❎")
    if iscaptain(message.guild,message.author):
        if message.content[16:] == "":
            response = "No event id was supplied."
            await message.channel.send(response.format(message))
            return
        elif not(message.content[16:].isdecimal()):
            response = "Invalid event ID."
            await message.channel.send(response.format(message))
            return
        else:
            eventid = int(message.content[16:])
            events = getevent(message.guild,eventid)
            if events is None:
                response = "Invalid event ID; event does not exist."
                await message.channel.send(response.format(message))
                return
            for event in events:
                eventname = event[1]
                isteam = event[4]
                channels = event[5]
            events.close()
            response = "Are you sure you want to deregister your team for the event " + eventname + "?"
            choice = await message.channel.send(response.format(message))
            await choice.add_reaction(greenTick)
            await choice.add_reaction(greenCross)
            try:
                booleanrespond = await client.wait_for('reaction_add',check=booleanResponse,timeout=10)
            except:
                response = "No response received. DeRegistration cancelled."
                await message.channel.send(response.format(message))
                return                
            if booleanrespond[0].emoji == greenCross:
                response = "DeRegistration cancelled."
                await message.channel.send(response.format(message))
                return
            else:
                cursor = sqlConn.cursor()
                cursor.execute('EXEC corgi.DeregisterTeam ?, ?;',eventid,message.author.id)
                for row in cursor:
                    teamid = row[0]
                sqlConn.commit()
                cursor.close()
                if teamid is None:
                    response = "You did not have any teams registered for the event " + eventname + "."
                    await message.channel.send(response.format(message))
                else:
                    team = discord.utils.get(message.guild.roles, id=teamid)
                    response = "Team " + team.name + " has been registered for the event " + eventname + "."
                    await message.channel.send(response.format(message))
                    embed = discord.Embed(title="Team Deregistered for Event", color=team.colour) 
                    embed.add_field(name="Deregistered By", value=message.author.display_name, inline=False)
                    embed.add_field(name="Deregistered By ID", value=message.author.id, inline=False)
                    embed.add_field(name="Team Name", value=team.name, inline=False)
                    embed.add_field(name="Team ID", value=team.id, inline=False)
                    embed.add_field(name="Event Name", value=eventname, inline=False)
                    embed.add_field(name="Event ID", value=eventid, inline=False)
                    now = datetime.utcnow()
                    embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                    logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
                    await logchannel.send(embed=embed)    
    return

async def addplayer(client,message):
    def booleanResponse(r,u):
        return r.message.id == choice.id and u.id == message.author.id and r.emoji in ("✅","❎")
    def digitResponse(r,u):
        return r.message.id == choice.id and u.id == message.author.id and emojidigits[r.emoji] <= t
    if iscaptain(message.guild,message.author):
        if len(message.mentions) == 0:
            response = "You must mention the user you want to add to your Team."
            await message.channel.send(response.format(message))
            return
        
        teams = getteams(message.author)
        #Now because Python can't count we have to do dumb shit...
        t = 0
        teamids = []
        teamnames = []
        response = "What team do you want to add the player " + message.mentions[0].display_name + " to?"
        for team in teams:
            if discord.utils.get(message.guild.roles, id=team[0]):
                t = t + 1
                teamids.append(team[0])
                teamnames.append(team[1])
                response = response + "\n" + digitemojis[t] + ": " + team[1]                    
        teams.close()
        if t == 0:
            response = "You haven't created a team to add a player to. Use the `$CreateTeam` command."
            await message.channel.send(response.format(message))
            return
        elif t == 1:
            response = "Add player " + message.mentions[0].display_name + " to the team " + teamnames[0] + "?"
            choice = await message.channel.send(response.format(message))
            await choice.add_reaction(greenTick)
            await choice.add_reaction(greenCross)
            try:
                booleanrespond = await client.wait_for('reaction_add',check=booleanResponse,timeout=10)
            except:
                response = "No response received. Player not added."
                await message.channel.send(response.format(message))
                return                
            if booleanrespond[0].emoji == greenCross:
                response = "Player not added."
                await message.channel.send(response.format(message))
                return
            else:
                teamid = teamids[0]
                teamname = teamnames[0]
        else:
            choice = await message.channel.send(response.format(message))
            for d in range(0,t):
                await choice.add_reaction(digitemojis[d+1])                
            try:
                digitrespond = await client.wait_for('reaction_add',check=digitResponse,timeout=10)
            except:
                response = "No response received. Player not added."
                await message.channel.send(response.format(message))
                return
            teamid = teamids[emojidigits[digitrespond[0].emoji]-1]
            teamname = teamnames[emojidigits[digitrespond[0].emoji]-1]
        cursor = sqlConn.cursor()
        try:
            cursor.execute('EXEC corgi.AddPlayer ?, ?;',teamid,message.mentions[0].id)
        except pyodbc.Error as ex:
            if ex.args[0] == '23000':
                response = "Player already registered for this team."
            await message.channel.send(response.format(message))
            return
        sqlConn.commit()
        cursor.close()
        response = "Player " + message.mentions[0].display_name + " has been added to the team " + teamname + "."
        team = discord.utils.get(message.guild.roles, id=teamid)
        await message.mentions[0].add_roles(team)
        await message.channel.send(response.format(message))
        embed = discord.Embed(title="Player added to Team", color=team.colour) 
        embed.add_field(name="Added By", value=message.author.display_name, inline=False)
        embed.add_field(name="Added By ID", value=message.author.id, inline=False)
        embed.add_field(name="Team Name", value=team.name, inline=False)
        embed.add_field(name="Team ID", value=team.id, inline=False)
        embed.add_field(name="Player Name", value=message.mentions[0].display_name, inline=False)
        embed.add_field(name="Player ID", value=message.mentions[0].id, inline=False)
        now = datetime.utcnow()
        embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
        logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
        await logchannel.send(embed=embed)    
    return

async def removeplayer(client,message):
    def booleanResponse(r,u):
        return r.message.id == choice.id and u.id == message.author.id and r.emoji in ("✅","❎")
    def digitResponse(r,u):
        return r.message.id == choice.id and u.id == message.author.id and emojidigits[r.emoji] <= t
    if iscaptain(message.guild,message.author):
        if len(message.mentions) == 0:
            response = "You must mention the user you want to remove from your Team."
            await message.channel.send(response.format(message))
            return
        teams = getteams(message.author)
        #Now because Python can't count we have to do dumb shit...
        t = 0
        teamids = []
        teamnames = []
        response = "What team do you want to remove the player " + message.mentions[0].display_name + " to?"
        for team in teams:
            if discord.utils.get(message.guild.roles, id=team[0]):
                t = t + 1
                teamids.append(team[0])
                teamnames.append(team[1])
                response = response + "\n" + digitemojis[t] + ": " + team[1]                    
        teams.close()
        if t == 0:
            response = "You haven't created a team to remove a player from. Use the `$CreateTeam` command."
            await message.channel.send(response.format(message))
            return
        elif t == 1:
            response = "Remove player " + message.mentions[0].display_name + " from the team " + teamnames[0] + "?"
            choice = await message.channel.send(response.format(message))
            await choice.add_reaction(greenTick)
            await choice.add_reaction(greenCross)
            try:
                booleanrespond = await client.wait_for('reaction_add',check=booleanResponse,timeout=10)
            except:
                response = "No response received. Player not removed."
                await message.channel.send(response.format(message))
                return                
            if booleanrespond[0].emoji == greenCross:
                response = "Player not removed."
                await message.channel.send(response.format(message))
                return
            else:
                teamid = teamids[0]
                teamname = teamnames[0]
        else:
            choice = await message.channel.send(response.format(message))
            for d in range(0,t):
                await choice.add_reaction(digitemojis[d+1])                
            try:
                digitrespond = await client.wait_for('reaction_add',check=digitResponse,timeout=10)
            except:
                response = "No response received. Player not removed."
                await message.channel.send(response.format(message))
                return
            teamid = teamids[emojidigits[digitrespond[0].emoji]-1]
            teamname = teamnames[emojidigits[digitrespond[0].emoji]-1]
        cursor = sqlConn.cursor()
        try:
            cursor.execute('EXEC corgi.RemovePlayer ?, ?;',teamid,message.mentions[0].id)
        except:
            response = "Failed to remove Player."
            await message.channel.send(response.format(message))
            return
        for row in cursor:
            playerid = row[0]            
        sqlConn.commit()
        cursor.close()
        if playerid is None:
            response = "Player " + message.mentions[0].display_name + " was not part of the team " + teamname + "."
            await message.channel.send(response.format(message))
            return
        response = "Player " + message.mentions[0].display_name + " has been removed from the team " + teamname + "."
        team = discord.utils.get(message.guild.roles, id=teamid)
        await message.mentions[0].remove_roles(team)
        await message.channel.send(response.format(message))
        embed = discord.Embed(title="Player removed from Team", color=team.colour) 
        embed.add_field(name="Removed By", value=message.author.display_name, inline=False)
        embed.add_field(name="Removed By ID", value=message.author.id, inline=False)
        embed.add_field(name="Team Name", value=team.name, inline=False)
        embed.add_field(name="Team ID", value=team.id, inline=False)
        embed.add_field(name="Player Name", value=message.mentions[0].display_name, inline=False)
        embed.add_field(name="Player ID", value=message.mentions[0].id, inline=False)
        now = datetime.utcnow()
        embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
        logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
        await logchannel.send(embed=embed)    
    return

async def changecolour(client,message):
    def booleanResponse(r,u):
        return r.message.id == choice.id and u.id == message.author.id and r.emoji in ("✅","❎")
    def digitResponse(r,u):
        return r.message.id == choice.id and u.id == message.author.id and emojidigits[r.emoji] <= t
    if iscaptain(message.guild,message.author):
        teamcolour = message.content[12:].lower()
        if not re.match("[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]",teamcolour) and colours.count(teamcolour) == 0 and not teamcolour == "random":
            await message.channel.send("Invalid hex or predefined colour.")
            return
        teams = getteams(message.author)
        #Now because Python can't count we have to do dumb shit...
        t = 0
        teamids = []
        teamnames = []
        response = "What team do you want to change the colour of?"
        for team in teams:
            if discord.utils.get(message.guild.roles, id=team[0]):
                t = t + 1
                teamids.append(team[0])
                teamnames.append(team[1])
                response = response + "\n" + digitemojis[t] + ": " + team[1]                    
        teams.close()
        if t == 0:
            response = "You haven't created a team to change. Use the `$CreateTeam` command."
            await message.channel.send(response.format(message))
            return
        elif t == 1:
            response = "Change colour of the team " + teamnames[0] + "?"
            choice = await message.channel.send(response.format(message))
            await choice.add_reaction(greenTick)
            await choice.add_reaction(greenCross)
            try:
                booleanrespond = await client.wait_for('reaction_add',check=booleanResponse,timeout=10)
            except:
                response = "No response received. Colour not changed."
                await message.channel.send(response.format(message))
                return                
            if booleanrespond[0].emoji == greenCross:
                response = "Colour not changed."
                await message.channel.send(response.format(message))
                return
            else:
                teamid = teamids[0]
        else:
            choice = await message.channel.send(response.format(message))
            for d in range(0,t):
                await choice.add_reaction(digitemojis[d+1])                
            try:
                digitrespond = await client.wait_for('reaction_add',check=digitResponse,timeout=10)
            except:
                response = "No response received. Colour not changed."
                await message.channel.send(response.format(message))
                return
            teamid = teamids[emojidigits[digitrespond[0].emoji]-1]
        team = discord.utils.get(message.guild.roles, id=teamid)
        if colours.count(teamcolour) == 1:
            colour = colourings[teamcolour]
            await team.edit(colour=discord.Colour(colour.value))
            embed = discord.Embed(title="Team Colour Changed", color=colour.value)
        elif teamcolour == "random":
            colour = int("0x"+str(randomcolour()),16)
            await team.edit(colour=discord.Colour(colour))
            embed = discord.Embed(title="Team Colour Changed", color=discord.Colour(colour)) 
        else:
            colour = int("0x"+teamcolour,16)
            await team.edit(colour=discord.Colour(colour))
            embed = discord.Embed(title="Team Colour Changed", color=discord.Colour(colour)) 
        response = "Team colour changed."
        await message.channel.send(response.format(message))
        embed.add_field(name="Changed By", value=message.author.display_name, inline=False)
        embed.add_field(name="Changed By ID", value=message.author.id, inline=False)
        embed.add_field(name="Team Name", value=team.name, inline=False)
        embed.add_field(name="Team ID", value=team.id, inline=False)
        now = datetime.utcnow()
        embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
        logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
        await logchannel.send(embed=embed)
    return

async def renameteam(client,message):
    def booleanResponse(r,u):
        return r.message.id == choice.id and u.id == message.author.id and r.emoji in ("✅","❎")
    def digitResponse(r,u):
        return r.message.id == choice.id and u.id == message.author.id and emojidigits[r.emoji] <= t
    if iscaptain(message.guild,message.author):
        newname = message.content[12:]
        if newname == "":
            response = "You need to supply a new name."
            await message.channel.send(response.format(message))
            return
        team = discord.utils.get(message.guild.roles, name=newname)
        category = discord.utils.get(message.guild.categories, name=newname)
        if not(team is None and category is None):
            response = "A team, role or category with that name already exists on the server. Please choose a different name."
            await message.channel.send(response.format(message))
            return
        teams = getteams(message.author)
        #Now because Python can't count we have to do dumb shit...
        t = 0
        teamids = []
        teamnames = []
        response = "What team do you want to rename?"
        for team in teams:
            if discord.utils.get(message.guild.roles, id=team[0]):
                t = t + 1
                teamids.append(team[0])
                teamnames.append(team[1])
                response = response + "\n" + digitemojis[t] + ": " + team[1]                    
        teams.close()
        if t == 0:
            response = "You haven't created a team to rename. Use the `$CreateTeam` command."
            await message.channel.send(response.format(message))
            return
        elif t == 1:
            response = "Change name of the team " + teamnames[0] + "?"
            choice = await message.channel.send(response.format(message))
            await choice.add_reaction(greenTick)
            await choice.add_reaction(greenCross)
            try:
                booleanrespond = await client.wait_for('reaction_add',check=booleanResponse,timeout=10)
            except:
                response = "No response received. Name not changed."
                await message.channel.send(response.format(message))
                return                
            if booleanrespond[0].emoji == greenCross:
                response = "Name not changed."
                await message.channel.send(response.format(message))
                return
            else:
                teamid = teamids[0]
                teamname = teamnames[0]
        else:
            choice = await message.channel.send(response.format(message))
            for d in range(0,t):
                await choice.add_reaction(digitemojis[d+1])                
            try:
                digitrespond = await client.wait_for('reaction_add',check=digitResponse,timeout=10)
            except:
                response = "No response received. Name not changed."
                await message.channel.send(response.format(message))
                return
            teamid = teamids[emojidigits[digitrespond[0].emoji]-1]
            teamname = teamnames[emojidigits[digitrespond[0].emoji]-1]
        cursor = sqlConn.cursor()
        try:
            cursor.execute('EXEC corgi.RenameTeam ?, ?;',teamid,newname)
        except:
            response = "Failed to rename Team."
            await message.channel.send(response.format(message))
            return      
        sqlConn.commit()
        cursor.close()
        team = discord.utils.get(message.guild.roles, id=teamid)
        category = discord.utils.get(message.guild.categories, name=team.id)
        await category.edit(name=newname)
        await team.edit(name=newname)
        response = "Team name changed."
        await message.channel.send(response.format(message))
        embed = discord.Embed(title="Team Name Changed", color=team.colour) 
        embed.add_field(name="Changed By", value=message.author.display_name, inline=False)
        embed.add_field(name="Changed By ID", value=message.author.id, inline=False)
        embed.add_field(name="New Name", value=newname, inline=False)
        embed.add_field(name="Old Name", value=teamname, inline=False)
        embed.add_field(name="Team ID", value=team.id, inline=False)
        now = datetime.utcnow()
        embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
        logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
        await logchannel.send(embed=embed)
    return

async def deleteteam(client,message):
    def booleanResponse(r,u):
        return r.message.id == choice.id and u.id == message.author.id and r.emoji in ("✅","❎")
    def digitResponse(r,u):
        return r.message.id == choice.id and u.id == message.author.id and emojidigits[r.emoji] <= t
    if iscaptain(message.guild,message.author):
        teams = getteams(message.author)
        #Now because Python can't count we have to do dumb shit...
        t = 0
        teamids = []
        teamnames = []
        response = "What team do you want to delete?"
        for team in teams:
            if discord.utils.get(message.guild.roles, id=team[0]):
                t = t + 1
                teamids.append(team[0])
                teamnames.append(team[1])
                response = response + "\n" + digitemojis[t] + ": " + team[1]                    
        teams.close()
        if t == 0:
            response = "You haven't created a team to delete. Use the `$CreateTeam` command."
            await message.channel.send(response.format(message))
            return
        elif t == 1:
            response = "Are you sure you want to delete the team " + teamnames[0] + "? This action **cannot** be undone."
            choice = await message.channel.send(response.format(message))
            await choice.add_reaction(greenTick)
            await choice.add_reaction(greenCross)
            try:
                booleanrespond = await client.wait_for('reaction_add',check=booleanResponse,timeout=10)
            except:
                response = "No response received. Team not deleted."
                await message.channel.send(response.format(message))
                return                
            if booleanrespond[0].emoji == greenCross:
                response = "Team not deleted."
                await message.channel.send(response.format(message))
                return
            else:
                teamid = teamids[0]
                teamname = teamnames[0]
        else:
            choice = await message.channel.send(response.format(message))
            for d in range(0,t):
                await choice.add_reaction(digitemojis[d+1])                
            try:
                digitrespond = await client.wait_for('reaction_add',check=digitResponse,timeout=10)
            except:
                response = "No response received. Team not deleted."
                await message.channel.send(response.format(message))
                return
            teamid = teamids[emojidigits[digitrespond[0].emoji]-1]
            teamname = teamnames[emojidigits[digitrespond[0].emoji]-1]
            response = "Are you sure you want to delete the team " + teamname + "? This action **cannot** be undone."
            choice = await message.channel.send(response.format(message))
            await choice.add_reaction(greenTick)
            await choice.add_reaction(greenCross)
            try:
                booleanrespond = await client.wait_for('reaction_add',check=booleanResponse,timeout=10)
            except:
                response = "No response received. Team not deleted."
                await message.channel.send(response.format(message))
                return                
            if booleanrespond[0].emoji == greenCross:
                response = "Team not deleted."
                await message.channel.send(response.format(message))
                return
        team = discord.utils.get(message.guild.roles, id=teamid)
        cursor = sqlConn.cursor()
        try:
            cursor.execute('EXEC corgi.DeleteTeam ?;',teamid)
        except:
            response = "Failed to delete Team."
            await message.channel.send(response.format(message))
            return      
        sqlConn.commit()
        cursor.close()
        response = "Team has been deleted."
        team = discord.utils.get(message.guild.roles, id=teamid)
        category = discord.utils.get(message.guild.categories, name=team.name)
        teamcolour = team.colour
        if not(category is None):
            for channel in category.channels:
                await channel.delete()
            await category.delete()
        await team.delete()
        await message.channel.send(response.format(message))
        embed = discord.Embed(title="Team Deleted", color=teamcolour) 
        embed.add_field(name="Deleted By", value=message.author.display_name, inline=False)
        embed.add_field(name="Deleted By ID", value=message.author.id, inline=False)
        embed.add_field(name="Team Name", value=teamname, inline=False)
        embed.add_field(name="Team ID", value=team.id, inline=False)
        now = datetime.utcnow()
        embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
        logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
        await logchannel.send(embed=embed)
    return

async def removeteam(role):
    category = discord.utils.get(role.guild.categories, name=role.name)
    if not(category is None):
        for channel in category.channels:
            await channel.delete()
        await category.delete()
    cursor = sqlConn.cursor()
    cursor.execute('EXEC corgi.DeleteTeam ?;',role.id)
    sqlConn.commit()
    cursor.close()

async def reassigncaptain(member):
    teamcaptain = discord.utils.get(member.guild.roles, id=getcaptain(member.guild))
    cursor = sqlConn.cursor()
    cursor.execute('EXEC corgi.ReassignCaptain ?;',member.id)
    for row in cursor:
        newcaptain = discord.utils.get(member.guild.members, id=row[1])
        team = discord.utils.get(member.guild.roles, id=row[0])
        await newcaptain.add_roles(teamcaptain)
        embed = discord.Embed(title="Team Captain Reassigned", color=team.colour) 
        embed.add_field(name="Team Name", value=team.name, inline=False)
        embed.add_field(name="Team ID", value=team.id, inline=False)
        embed.add_field(name="New Captain", value=newcaptain.display_name, inline=False)
        embed.add_field(name="New Captain ID", value=newcaptain.id, inline=False)
        now = datetime.utcnow()
        embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
        logchannel = discord.utils.get(member.guild.channels, name="corgi-logs")
        await logchannel.send(embed=embed)
    sqlConn.commit()
    cursor.close()
    

async def clearcaptain(member):
    outercursor = sqlConn2.cursor()
    outercursor.execute('EXEC corgi.ClearCaptain ?;',member.id)
    for row in outercursor:
        team = discord.utils.get(member.guild.roles, id=row[0])
        await removeteam(team)
        embed = discord.Embed(title="Team Deleted Automatically", color=team.colour) 
        embed.add_field(name="Team Name", value=team.name, inline=False)
        embed.add_field(name="Team ID", value=team.id, inline=False)
        now = datetime.utcnow()
        embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
        logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
        await logchannel.send(embed=embed)
        await team.delete()
    sqlConn2.commit()
    outercursor.close()

