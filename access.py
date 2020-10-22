import discord, discord.utils, random, os, re, json, sys, time, secrets, pyodbc
from datetime import datetime, timedelta
from dotenv import load_dotenv

SQLServer = os.getenv('SQL_SERVER')
SQLDatabase = os.getenv('SQL_DATABASE')
SQLLogin = os.getenv('SQL_LOGIN')
SQLPassword = os.getenv('SQL_PASSWORD')

SQLConnString = 'Driver={ODBC Driver 17 for SQL Server};Server=' + SQLServer+ ';Database=' + SQLDatabase + ';UID='+ SQLLogin +';PWD=' + SQLPassword

sqlConn = pyodbc.connect(SQLConnString)

digitemojis = {1:"1️⃣",2:"2️⃣",3:"3️⃣",4:"4️⃣",5:"5️⃣",6:"6️⃣",7:"7️⃣",8:"8️⃣",9:"9️⃣",10:"🔟"}
emojidigits = {"1️⃣":1,"2️⃣":2,"3️⃣":3,"4️⃣":4,"5️⃣":5,"6️⃣":6,"7️⃣":7,"8️⃣":8,"9️⃣":9,"🔟":10}

def isowner(guild,user):
    if guild.owner == user:
        return True
    else:
        return False

def isadmin(guild,user):
    userRoles = user.roles
    roleParam = ""
    for role in userRoles:
        roleParam = "," + str(role.id)
    cursor = sqlConn.cursor()
    roleParam = roleParam[2:]
    cursor.execute('EXEC corgi.GetUserAccess ?, ?;',guild.id,roleParam)
    for row in cursor:
        if row[1] == "Server Administrator":
            cursor.close()
            return True
    cursor.close()
    return False

def isheadjudge(guild,user):
    userRoles = user.roles
    roleParam = ""
    for role in userRoles:
        roleParam = "," + str(role.id)
    cursor = sqlConn.cursor()
    roleParam = roleParam[2:]
    cursor.execute('EXEC corgi.GetUserAccess ?, ?;',guild.id,roleParam)
    for row in cursor:
        if row[1] == "Server Administrator":
            cursor.close()
            return True
    cursor.close()
    return False
    
def isjudge(guild,user):
    userRoles = user.roles
    roleParam = ""
    for role in userRoles:
        roleParam = "," + str(role.id)
    cursor = sqlConn.cursor()
    roleParam = roleParam[2:]
    cursor.execute('EXEC corgi.GetUserAccess ?, ?;',guild.id,roleParam)
    for row in cursor:
        if row[1] == "Judge" or row[1] == "Head Judge":
            cursor.close()
            return True
    cursor.close()
    return False

def iscaptain(guild,user):
    userRoles = user.roles
    roleParam = ""
    for role in userRoles:
        roleParam = "," + str(role.id)
    cursor = sqlConn.cursor()
    roleParam = roleParam[2:]
    cursor.execute('EXEC corgi.GetUserAccess ?, ?;',guild.id,roleParam)
    for row in cursor:
        if row[1] == "Team Captain":
            cursor.close()
            return True
    cursor.close()
    return False


async def addaccess(client,message):
    #Check permissions
    if isowner(message.guild,message.author) or isadmin(message.guild,message.author):
        #Open a connection
        cursor = sqlConn.cursor()
        #Get details of the role
        roleid = None
        if len(message.role_mentions) == 1:
            rolename = message.role_mentions[0].name
            roleid = message.role_mentions[0].id
        else:
            rolename = message.content[15:]
            serverroles = message.guild.roles
            for role in serverroles:
                if role.name.lower() == rolename.lower():
                    roleid = role.id
                    rolename = role.name
                    break
        #There is no role
        if roleid is None:
            response = "Role not found, access level has not been changed."
            await message.channel.send(response.format(message))
        else:
            #Get role levels
            cursor.execute('EXEC corgi.GetAccessLevels;')
            r = 1
            response = "What access level would you like to the the role?"
            levels = []
            accesses = []
            for row in cursor:
                response = response + "\n" + digitemojis[r] + ": " + row[1]
                levels.append(row[0])
                accesses.append(row[1])
                r = r + 1
            rows = r - 1
            #prompt user and add reactions
            access = await message.channel.send(response.format(message))
            r = 1
            while r <= rows:
                await access.add_reaction(digitemojis[r])
                r = r + 1
            def accessResponse(r,u):
                return r.message.id == access.id and u.id == message.author.id and emojidigits[r.emoji] <= rows
            try:
                reply = await client.wait_for('reaction_add',check=accessResponse,timeout=10)
            except:
                #Got bored waiting
                response = "No response received. Access amendment cancelled."
                await message.channel.send(response.format(message))
                return
            #Add the access
            try:
                cursor.execute('EXEC corgi.AddRoleAccess ?, ?, ?;',message.guild.id,roleid,levels[emojidigits[reply[0].emoji]-1])
                sqlConn.commit()
                response = "Access level of " + accesses[emojidigits[reply[0].emoji]-1] + " given to role " + rolename + "."
                #Log details
                embed = discord.Embed(title="Give Role Access", color=discord.Colour.orange()) #description=message.mentions[0].display_name
                embed.add_field(name="Added By", value=message.author.display_name, inline=False)
                embed.add_field(name="Added By ID", value=message.author.id, inline=False)
                embed.add_field(name="Role Affected", value=rolename, inline=False)
                embed.add_field(name="Role ID", value=roleid, inline=False)
                embed.add_field(name="Access Granted", value=accesses[emojidigits[reply[0].emoji]-1], inline=False)
                now = datetime.utcnow()
                embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
                logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
                await logchannel.send(embed=embed)
            except pyodbc.Error as ex:
                if ex.args[0] == "23000":
                    response = "There is already a role with Team Captain Access on this Server."
                else:
                    response = "Failed to give access level of " + accesses[emojidigits[reply[0].emoji]-1] + " to role " + rolename + "."
            cursor.close()
            await message.channel.send(response.format(message))
    return

async def removeaccess(message):
    #Check permissions
    if isowner(message.guild,message.author) or isadmin(message.guild,message.author):
        #Get details of the role
        delrole = None
        if len(message.role_mentions) == 1:
            delrole = message.role_mentions[0]
        else:
            rolename = message.content[18:]
            serverRoles = message.guild.roles
            for role in serverRoles:
                if role.name.lower() == rolename.lower():
                    delrole = role
                    break
        ##There is no role
        if delrole is None:
            response = "Role not found, access level has not been changed."
            await message.channel.send(response.format(message))
        else:
            response = "Permissions related to the role " + delrole.name + " have been removed."
            await message.channel.send(response.format(message))
            await removeaccesslevel(message.guild,delrole)
            #Log details
            embed = discord.Embed(title="Remove Role Access", color=discord.Colour.orange()) #description=message.mentions[0].display_name
            embed.add_field(name="Removed By", value=message.author.display_name, inline=False)
            embed.add_field(name="Removed By ID", value=message.author.id, inline=False)
            embed.add_field(name="Role Affected", value=delrole.name, inline=False)
            embed.add_field(name="Role ID", value=delrole.id, inline=False)
            now = datetime.utcnow()
            embed.set_footer(text="Logged: " + now.strftime("%Y-%m-%d %H:%M:%S") + " UTC")
            logchannel = discord.utils.get(message.guild.channels, name="corgi-logs")
            await logchannel.send(embed=embed)
    return

async def removeaccesslevel(guild,role):
    cursor = sqlConn.cursor()
    cursor.execute('EXEC corgi.RemoveRoleAccess ?, ?;',guild.id,role.id)
    sqlConn.commit()
    cursor.close()


async def checkaccess(message):
    if isowner(message.guild,message.author) or isadmin(message.guild,message.author):
        #Get details of the role
        checkrole = None
        if len(message.role_mentions) == 1:
            checkrole = message.role_mentions[0]
        else:
            rolename = message.content[17:]
            serverRoles = message.guild.roles
            for role in serverRoles:
                if role.name.lower() == rolename.lower():
                    checkrole = role
                    break
        ##There is no role
        if checkrole is None:
            response = "Role not found."
            await message.channel.send(response.format(message))
        else:
            cursor = sqlConn.cursor()
            cursor.execute('EXEC corgi.GetRoleAccess ?, ?;',message.guild.id,checkrole.id)
            response = None
            for row in cursor:
                response = "The role " + checkrole.name + " currently has the access level " + row[1] + "."
            cursor.close()
            if response is None:
                response = "The role " + checkrole.name + " currently has no access level."
            await message.channel.send(response.format(message))
    return