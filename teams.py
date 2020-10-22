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

def getcaptainrole (guild):
    cursor = sqlConn.cursor()
    cursor.execute('EXEC corgi.GetServerCaptain ?;',guild.id)
    for row in cursor:
        return row[0]
    cursor.close()
    return None
    

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
    else:
        return