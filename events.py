import discord, discord.utils, random, os, re, json, sys, time, secrets, pyodbc
from datetime import datetime, timedelta
from dotenv import load_dotenv
from access import isowner, isadmin, isheadjudge, isjudge, iscaptain

SQLServer = os.getenv('SQL_SERVER')
SQLDatabase = os.getenv('SQL_DATABASE')
SQLLogin = os.getenv('SQL_LOGIN')
SQLPassword = os.getenv('SQL_PASSWORD')

SQLConnString = 'Driver={ODBC Driver 17 for SQL Server};Server=' + SQLServer+ ';Database=' + SQLDatabase + ';UID='+ SQLLogin +';PWD=' + SQLPassword

sqlConn = pyodbc.connect(SQLConnString)

greenTick = "✅"
greenCross = "❎"
digitemojis = {1:"1️⃣",2:"2️⃣",3:"3️⃣",4:"4️⃣",5:"5️⃣",6:"6️⃣",7:"7️⃣",8:"8️⃣",9:"9️⃣",10:"🔟"}
emojidigits = {"1️⃣":1,"2️⃣":2,"3️⃣":3,"4️⃣":4,"5️⃣":5,"6️⃣":6,"7️⃣":7,"8️⃣":8,"9️⃣":9,"🔟":10}

def validatedate(datestr):
    try:
        dateobj = datetime.strptime(datestr, '%Y-%m-%d')
        return True
    except:
        return False

def getevent (guild,eventid):
    cursor = sqlConn.cursor()
    cursor.execute('EXEC corgi.GetEvent ?, ?;',guild.id,eventid)
    return cursor

def geteventdetail (guild,eventid):
    cursor = sqlConn.cursor()
    cursor.execute('EXEC corgi.GetEventDetail ?, ?;',guild.id,eventid)
    return cursor

def getdetail (guild,detailid):
    cursor = sqlConn.cursor()
    cursor.execute('EXEC corgi.GetDetail ?, ?;',guild.id,detailid)
    return cursor

async def addevent(client,message):
    def isdate(m):
        return m.author.id == message.author.id and m.channel.id == message.channel.id and re.match("[2][0-1][0-9][0-9]-[0-1][0-9]-[0-3][0-9]",m.content) and validatedate(m.content)
    def booleanResponse(r,u):
        return r.message.id == respond.id and u.id == message.author.id and r.emoji in ("✅","❎")
    if isowner(message.guild,message.author) or isadmin(message.guild,message.author) or isheadjudge(message.guild,message.author):
        if message.content[10:] == "":
            response = "Event requires a name to be created."
            await message.channel.send(response.format(message))
            return
        else:
            eventname = message.content[10:]
        response = "What is the start date of the event? (Format required is `yyyy-MM-dd`)"
        await message.channel.send(response.format(message))
        try:
            inputdate = await client.wait_for('message',check=isdate,timeout=30)
        except:
            response = "No response received. Event creation cancelled."
            await message.channel.send(response.format(message))
        startdate = datetime.strptime(inputdate.content, '%Y-%m-%d')
        response = "What is the end date of the event? (Format required is `yyyy-MM-dd`)"
        await message.channel.send(response.format(message))
        try:
            inputdate = await client.wait_for('message',check=isdate,timeout=30)
        except:
            response = "No response received. Event creation cancelled."
            await message.channel.send(response.format(message))
        enddate = datetime.strptime(inputdate.content, '%Y-%m-%d')
        if enddate < startdate:
            response = "The Event cannot end before it has started. Event creation cancelled"
            await message.channel.send(response.format(message))
            return
        response = "Is this a Team Event?"
        respond = await message.channel.send(response.format(message))
        await respond.add_reaction(greenTick)
        await respond.add_reaction(greenCross)
        #Get that reaction
        reply = None
        try:
            reply = await client.wait_for('reaction_add',check=booleanResponse,timeout=10)
        except:
            response = "No response received. Assumed solos event."
            await message.channel.send(response.format(message))
        if reply is None or reply[0].emoji == greenCross:
            teams = 0
            teamchannels = 0
        else:
            teams = 1
        if teams == 1:
            response = "Would you like teams that register to have Team Channels created, if they do not already have one?"
            respond = await message.channel.send(response.format(message))
            await respond.add_reaction(greenTick)
            await respond.add_reaction(greenCross)
            #Get that reaction
            reply = None
            try:
                reply = await client.wait_for('reaction_add',check=booleanResponse,timeout=10)
            except:
                response = "No response received. Assumed channels are not required."
                await message.channel.send(response.format(message))
            if reply is None or reply[0].emoji == greenCross:
                teamchannels = 0
            else:
                teamchannels = 1
        cursor = sqlConn.cursor()
        cursor.execute('EXEC corgi.AddEvent ?, ?, ?, ?, ?, ?, ?;',message.guild.id,eventname,startdate,enddate,teams,teamchannels,message.author.id)
        for row in cursor:
            eventid = row[0]
        cursor.commit()
        cursor.close()
        response = "Event Created."
        await message.channel.send(response.format(message))
        #Log details
        embed = discord.Embed(title="Create Event", color=discord.Colour.orange())
        embed.add_field(name="Created By", value=message.author.display_name, inline=False)
        embed.add_field(name="Created By ID", value=message.author.id, inline=False)
        embed.add_field(name="Event Name", value=eventname, inline=False)
        embed.add_field(name="Event ID", value=eventid, inline=False)
        now = datetime.utcnow()
        embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
        logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
        await logchannel.send(embed=embed)
    return

async def eventdetails(message,eventid):
    details = geteventdetail(message.guild,eventid)
    r = 1
    embed = None
    for row in details:
        eventid = row[0]
        eventname = row[1]
        startdate = row[2]
        enddate = row[3]
        teamevent = row[4]
        teamchannels = row[5]
        detailid = row[6]
        detailname = row[7]
        detail = row[8]
        if r == 1:
            embed = discord.Embed(title=eventname, color=discord.Colour.orange())
            embed.add_field(name="Start Date", value=row[2], inline=True)
            embed.add_field(name="End Date", value=row[3], inline=True)
            if row[4] == 1:
                TeamEvent = "Yes"
                if row[5] == 1:
                    TeamChannels = "Yes"
                else:
                    TeamChannels = "No"
            else: 
                TeamEvent = "No"
            embed.add_field(name="Team Event", value=TeamEvent, inline=True)
            if TeamEvent == "Yes":
                embed.add_field(name="Team Channels", value=TeamChannels, inline=True)
            embed.add_field(name="Event ID", value=row[0], inline=True)
        if not(detailid is None):
            embed.add_field(name="\u200b",value="\u200b",inline=False)
            embed.add_field(name=detailname,value=detail,inline=True)
            embed.add_field(name="Detail ID",value=detailid,inline=True)
        r = r + 1
    details.close()
    if embed is None:
        response = "Invalid event ID; event does not exist."
        await message.channel.send(response.format(message))
    else:
        await message.channel.send(embed=embed)
    return


async def adddetail(client,message):
    def isuser(m):
        return m.author.id == message.author.id and m.channel.id == message.channel.id
    if isowner(message.guild,message.author) or isadmin(message.guild,message.author) or isheadjudge(message.guild,message.author):
        if message.content[16:] == "":
            response = "Requires Event ID to add a detail."
            await message.channel.send(response.format(message))
            return
        elif not(message.content[16:].isdecimal()):
            response = "Invalid event ID."
            await message.channel.send(response.format(message))
            return
        else:
            eventid = int(message.content[16:])
            event = getevent(message.guild,eventid)
            if event is None:
                response = "Invalid event ID; event does not exist."
                await message.channel.send(response.format(message))
                return
            event.close()
            response = "What is the name of the detail you want to add?"
            await message.channel.send(response.format(message))
            try:
                detailname = await client.wait_for('message',check=isuser,timeout=30)
            except:
                response = "No response received. Detail amendedment cancelled."
                await message.channel.send(response.format(message))
                return
            response = "What is the detail you want to add?"
            await message.channel.send(response.format(message))
            try:
                detail = await client.wait_for('message',check=isuser,timeout=120)
            except:
                response = "No response received. Detail amendedment cancelled."
                await message.channel.send(response.format(message))
                return
            cursor = sqlConn.cursor()
            cursor.execute('EXEC corgi.AddDetail ?, ?, ?;',eventid,detailname.content,detail.content)
            for row in cursor:
                detailid = row[0]
            cursor.commit()
            cursor.close()
            response = "Detail has been added to the event."
            await message.channel.send(response.format(message))

            #Log details
            embed = discord.Embed(title="Add Event Detail", color=discord.Colour.orange())
            embed.add_field(name="Added By", value=message.author.display_name, inline=False)
            embed.add_field(name="Added By ID", value=message.author.id, inline=False)
            embed.add_field(name="Detail Name", value=detailname.content, inline=False)
            embed.add_field(name="Detail ID", value=detailid, inline=False)
            now = datetime.utcnow()
            embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
            logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
            await logchannel.send(embed=embed)
            await eventdetails(message,eventid)
    return

async def editevent(client,message):
    def editResponse(r,u):
        return r.message.id == respond.id and u.id == message.author.id and emojidigits[r.emoji] <= reactions
    def isuser(m):
        return m.author.id == message.author.id and m.channel.id == message.channel.id
    def isdate(m):
        return m.author.id == message.author.id and m.channel.id == message.channel.id and re.match("[2][0-1][0-9][0-9]-[0-1][0-9]-[0-3][0-9]",m.content) and validatedate(m.content)
    def booleanResponse(r,u):
        return r.message.id == respond.id and u.id == message.author.id and r.emoji in ("✅","❎")
    if isowner(message.guild,message.author) or isadmin(message.guild,message.author) or isheadjudge(message.guild,message.author):
        if message.content[11:] == "":
            response = "Requires Event ID to edit."
            await message.channel.send(response.format(message))
            return
        elif not(message.content[11:].isdecimal()):
            response = "Invalid event ID."
            await message.channel.send(response.format(message))
            return
        else:
            eventid = message.content[11:]
            event = getevent(message.guild,eventid)
            if event is None:
                response = "Invalid event ID; event does not exist."
                await message.channel.send(response.format(message))
                return
            for row in event:
                eventname = row[1]
                startdate = row[2]
                enddate = row[3]
                teamevent = row[4]
                channels = row[5]
            event.close()
            response = "What would you like to amend?\n" + digitemojis[1] + ": Event Name\n" + digitemojis[2] + ": Start Date\n" + digitemojis[2] + ": End Date\n" + digitemojis[4] + ": Event Type"
            reactions = 4
            if teamevent == 1:
                response = response + "\n" + digitemojis[5] + ": Team Channels"
                reactions = 5
            respond = await message.channel.send(response.format(message))
            await respond.add_reaction(digitemojis[1])
            await respond.add_reaction(digitemojis[2])
            await respond.add_reaction(digitemojis[3])
            await respond.add_reaction(digitemojis[4])
            if reactions == 5:
                await respond.add_reaction(digitemojis[5])
            try:
                reply = await client.wait_for('reaction_add',check=editResponse,timeout=10)
            except:
                response = "No response received. Editting cancelled."
                await message.channel.send(response.format(message))
                return
            replyoption = emojidigits[reply[0].emoji]
            if replyoption == 1:
                response = "What is the new name of the event?"
                await message.channel.send(response.format(message))
                try:
                    reply = await client.wait_for('message',check=isuser,timeout=30)
                except:
                    response = "No response received. Editting cancelled."
                    await message.channel.send(response.format(message))
                    return
                eventname = reply.content
            elif replyoption == 2:
                response = "What is the new start date of the event? (Format required is `yyyy-MM-dd`)"
                await message.channel.send(response.format(message))
                try:
                    reply = await client.wait_for('message',check=isdate,timeout=30)
                except:
                    response = "No response received. Editting cancelled."
                    await message.channel.send(response.format(message))
                    return
                startdate = datetime.strptime(reply.content, '%Y-%m-%d').date()
                if startdate > enddate:
                    response = "Start date cannot be after end date of Event. Editting cancelled."
                    await message.channel.send(response.format(message))
                    return
            elif replyoption == 3:
                response = "What is the new end date of the event? (Format required is `yyyy-MM-dd`)"
                await message.channel.send(response.format(message))
                try:
                    reply = await client.wait_for('message',check=isdate,timeout=30)
                except:
                    response = "No response received. Editting cancelled."
                    await message.channel.send(response.format(message))
                    return
                enddate = datetime.strptime(reply.content, '%Y-%m-%d').date()
                if startdate > enddate:
                    response = "End date cannot be before start date of Event. Editting cancelled."
                    await message.channel.send(response.format(message))
                    return
            elif replyoption == 4:
                response = "Make event a Team Event?"
                respond = await message.channel.send(response.format(message))
                await respond.add_reaction(greenTick)
                await respond.add_reaction(greenCross)
                #Get that reaction
                reply = None
                try:
                    reply = await client.wait_for('reaction_add',check=booleanResponse,timeout=10)
                except:
                    response = "No response received. Assumed solos event."
                    await message.channel.send(response.format(message))
                if reply is None or reply[0].emoji == greenCross:
                    teamevent = 0
                    channels = 0
                else:
                    teamevent = 1
                if teamevent == 1:
                    response = "Would you like teams that register to have Team Channels created, if they do not already have one?"
                    respond = await message.channel.send(response.format(message))
                    await respond.add_reaction(greenTick)
                    await respond.add_reaction(greenCross)
                    #Get that reaction
                    reply = None
                    try:
                        reply = await client.wait_for('reaction_add',check=booleanResponse,timeout=10)
                    except:
                        response = "No response received. Assumed channels are not required."
                        await message.channel.send(response.format(message))
                    if reply is None or reply[0].emoji == greenCross:
                        channels = 0
                    else:
                        channels = 1
            elif replyoption == 5:
                response = "Would you like teams that register to have Team Channels created, if they do not already have one?"
                respond = await message.channel.send(response.format(message))
                await respond.add_reaction(greenTick)
                await respond.add_reaction(greenCross)
                #Get that reaction
                reply = None
                try:
                    reply = await client.wait_for('reaction_add',check=booleanResponse,timeout=10)
                except:
                    response = "No response received. Assumed channels are not required."
                    await message.channel.send(response.format(message))
                if reply is None or reply[0].emoji == greenCross:
                    channels = 0
                else:
                    channels = 1
            cursor = sqlConn.cursor()
            cursor.execute('EXEC corgi.EditEvent ?, ?, ?, ?, ?, ?, ?;',message.guild.id,eventid,eventname,startdate,enddate,teamevent,channels)
            cursor.commit()
            cursor.close()
            response = "Event Amended."
            await message.channel.send(response.format(message))
            #Log details
            embed = discord.Embed(title="Event Amended", color=discord.Colour.orange())
            embed.add_field(name="Amended By", value=message.author.display_name, inline=False)
            embed.add_field(name="Amended By ID", value=message.author.id, inline=False)
            embed.add_field(name="Event Name", value=eventname, inline=False)
            embed.add_field(name="Event ID", value=eventid, inline=False)
            now = datetime.utcnow()
            embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
            logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
            await logchannel.send(embed=embed)
    return

async def deleteevent(client,message):
    def booleanResponse(r,u):
        return r.message.id == respond.id and u.id == message.author.id and r.emoji in ("✅","❎")
    if isowner(message.guild,message.author) or isadmin(message.guild,message.author) or isheadjudge(message.guild,message.author):
        if message.content[13:] == "":
            response = "Requires Event ID to delete."
            await message.channel.send(response.format(message))
            return
        elif not(message.content[13:].isdecimal()):
            response = "Invalid event ID."
            await message.channel.send(response.format(message))
            return
        else:
            eventid = message.content[13:]
            event = getevent(message.guild,eventid)
            if event is None:
                response = "Invalid event ID; event does not exist."
                await message.channel.send(response.format(message))
                return
            for row in event:
                eventname = row[1]
            event.close()
            response = "Are you sure you want to delete the event " + eventname + "?"
            respond = await message.channel.send(response.format(message))
            await respond.add_reaction(greenTick)
            await respond.add_reaction(greenCross)
            #Get that reaction
            reply = None
            try:
                reply = await client.wait_for('reaction_add',check=booleanResponse,timeout=10)
            except:
                response = "No response received. Deletion cancelled."
                await message.channel.send(response.format(message))
                return
            if reply is None or reply[0].emoji == greenCross:
                response = "Deletion cancelled."
                await message.channel.send(response.format(message))
                return
            else:
                cursor = sqlConn.cursor()
                cursor.execute('EXEC corgi.DeleteEvent ?, ?;', message.guild.id, eventid)
                cursor.commit()
                cursor.close()
                response = "Event Deleted."
                await message.channel.send(response.format(message))
                #Log details
                embed = discord.Embed(title="Event Deleted", color=discord.Colour.orange())
                embed.add_field(name="Deleted By", value=message.author.display_name, inline=False)
                embed.add_field(name="Deleted By ID", value=message.author.id, inline=False)
                embed.add_field(name="Event Name", value=eventname, inline=False)
                embed.add_field(name="Event ID", value=eventid, inline=False)
                now = datetime.utcnow()
                embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
                await logchannel.send(embed=embed)
    return

async def deletedetail(client,message):
    def booleanResponse(r,u):
        return r.message.id == respond.id and u.id == message.author.id and r.emoji in ("✅","❎")
    if isowner(message.guild,message.author) or isadmin(message.guild,message.author) or isheadjudge(message.guild,message.author):
        if message.content[14:] == "":
            response = "Requires Detail ID to edit."
            await message.channel.send(response.format(message))
            return
        elif not(message.content[14:].isdecimal()):
            response = "Invalid detail ID."
            await message.channel.send(response.format(message))
            return
        else:
            detailid = message.content[14:]
            detail = getdetail(message.guild,detailid)
            if detail is None:
                response = "Invalid detail ID; detail does not exist."
                await message.channel.send(response.format(message))
                return
            for row in detail:
                eventname = row[1]
                detailname = row[7]
            detail.close()
            response = "Are you sure you want to delete the detail " + detailname + " for the event " + eventname + "?"
            respond = await message.channel.send(response.format(message))
            await respond.add_reaction(greenTick)
            await respond.add_reaction(greenCross)
            #Get that reaction
            reply = None
            try:
                reply = await client.wait_for('reaction_add',check=booleanResponse,timeout=10)
            except:
                response = "No response received. Deletion cancelled."
                await message.channel.send(response.format(message))
                return
            if reply is None or reply[0].emoji == greenCross:
                response = "Deletion cancelled."
                await message.channel.send(response.format(message))
                return
            else:
                cursor = sqlConn.cursor()
                cursor.execute('EXEC corgi.DeleteDetail ?, ?;', message.guild.id, detailid)
                cursor.commit()
                cursor.close()
                response = "Detail Deleted."
                await message.channel.send(response.format(message))
                #Log details
                embed = discord.Embed(title="Delete Event Detail", color=discord.Colour.orange())
                embed.add_field(name="Deleted By", value=message.author.display_name, inline=False)
                embed.add_field(name="Deleted By ID", value=message.author.id, inline=False)
                embed.add_field(name="Detail Name", value=detailname, inline=False)
                embed.add_field(name="Detail ID", value=detailid, inline=False)
                now = datetime.utcnow()
                embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
                await logchannel.send(embed=embed)
    return


async def events(message):
    embed = discord.Embed(title="Current Events", color=discord.Colour.orange())
    cursor = sqlConn.cursor()
    cursor.execute('EXEC corgi.GetEvents ?;',message.guild.id)
    e = 1
    for row in cursor:
        if e > 1:
            embed.add_field(name="\n\u200b",value="\n\u200b",inline=False)
        embed.add_field(name="Name", value=row[1], inline=False)
        embed.add_field(name="Start Date", value=row[2], inline=True)
        embed.add_field(name="End Date", value=row[3], inline=True)
        if row[4] == 1:
            TeamEvent = "Yes"
            if row[5] == 1:
                TeamChannels = "Yes"
            else:
                TeamChannels = "No"
        else: 
            TeamEvent = "No"
        embed.add_field(name="Team Event", value=TeamEvent, inline=True)
        if TeamEvent == "Yes":
            embed.add_field(name="Team Channels", value=TeamChannels, inline=True)
        embed.add_field(name="Event ID", value=row[0], inline=True)
        e = e + 1
    cursor.close()
    await message.channel.send(embed=embed)
    return
            
