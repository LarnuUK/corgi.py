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

def validatedate(datestr):
    try:
        dateobj = datetime.strptime(datestr, '%Y-%m-%d')
        return True
    except:
        return False

async def addevent(client,message):
    def isdate(m):
        return m.author.id == message.author.id and m.channel.id == message.channel.id and re.match("[2][0-1][0-9][0-9]-[0-1][0-9]-[0-3][0-9]",m.content) and validatedate(m.content)
    def channelsResponse(r,u):
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
            response = "No response received. Event creation cancelled"
            await message.channel.send(response.format(message))
        startdate = datetime.strptime(inputdate.content, '%Y-%m-%d')
        response = "What is the end date of the event? (Format required is `yyyy-MM-dd`)"
        await message.channel.send(response.format(message))
        try:
            inputdate = await client.wait_for('message',check=isdate,timeout=30)
        except:
            response = "No response received. Event creation cancelled"
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
            reply = await client.wait_for('reaction_add',check=channelsResponse,timeout=10)
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
                reply = await client.wait_for('reaction_add',check=channelsResponse,timeout=10)
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
        embed.add_field(name="Created ID", value=message.author.id, inline=False)
        embed.add_field(name="Event Name", value=eventname, inline=False)
        embed.add_field(name="Event ID", value=eventid, inline=False)
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
            
