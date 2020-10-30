import discord, discord.utils, random, os, re, json, sys, time, secrets, pyodbc
from datetime import datetime, timedelta
from dotenv import load_dotenv
from access import isowner, isadmin, isheadjudge, isjudge, iscaptain

load_dotenv()
debugon = os.getenv('DEBUG')
SQLServer = os.getenv('SQL_SERVER')
SQLDatabase = os.getenv('SQL_DATABASE')
SQLLogin = os.getenv('SQL_LOGIN')
SQLPassword = os.getenv('SQL_PASSWORD')

SQLConnString = 'Driver={ODBC Driver 17 for SQL Server};Server=' + SQLServer + ';Database=' + SQLDatabase + ';UID='+ SQLLogin +';PWD=' + SQLPassword

sqlConn = pyodbc.connect(SQLConnString)

def addfetchscore(message,score):
    cursor = sqlConn.cursor()
    cursor.execute('EXEC corgi.AddFetchScore ?, ?, ?;',message.guild.id,message.author.id,score)
    for scores in cursor:
        score=scores[0]
    sqlConn.commit()
    cursor.close()
    return score

async def playfetch(client,message):
    stick = client.get_emoji(735827082151723029)
    lurk = client.get_emoji(736190606254145548)
    directions = ["⬅️","⬆️","➡️","⬇️","↗️","↘️","↙️","↖️","↩","↪","⤴️","⤵️"]
    def isStick(r,u):
        return r.message.id == stickmessage.id and u.id == message.author.id and r.emoji == stick
    def isThrow(r,u):
        return r.message.id == throw.id and u.id == message.author.id and r.emoji in directions
    stickmessage = message
    play = True
    success = 0
    while play == True:
        if stick:
            if success == 1:
                throws = "throw"
            else:
                throws = "throws"
            await stickmessage.add_reaction(stick)
            try:
                reply = await client.wait_for('reaction_add',check=isStick,timeout=10)
            except:
                if success == 0:
                    await stickmessage.remove_reaction(stick,client.user)
                    await stickmessage.add_reaction(lurk)
                else:
                    await throw.delete()
                    hiscore = addfetchscore(message,success)
                    response = "*Looks bored and walks off.* (" + str(success) + " successful " + throws + ". Your hiscore is " + str(hiscore) + ".)"
                    stickmessage = await message.channel.send(response.format(message))
                return
            if success < 5:
                options = 3
            elif success < 10:
                options = 7
            else:
                options = 11
            direction = random.randint(0,options)            
            if not(debugon is None):
                print('Random Direction is:' + str(direction))
                print('Random Direction is:' + str(directions[direction]))
            response = "Where will you throw the stick?"
            throw = await message.channel.send(response.format(message))
            for r in range(0,options+1):
                await throw.add_reaction(directions[r])
            #await throw.add_reaction("⬅️")
            #await throw.add_reaction("⬆️")
            #await throw.add_reaction("➡️")
            #await throw.add_reaction("⬇️")
            try:
                reply = await client.wait_for('reaction_add',check=isThrow,timeout=10)
                if message != stickmessage:
                    await stickmessage.delete()
            except:
                if message != stickmessage:
                    await stickmessage.delete()
                await throw.delete()
                hiscore = addfetchscore(message,success)
                response = "*Looks bored and walks off.* (" + str(success) + " successful " + throws + ". Your hiscore is " + str(hiscore) + ".)"
                stickmessage = await message.channel.send(response.format(message))
                return               
            if directions[direction] == reply[0].emoji:
                success = success + 1
                response = "*Runs after the stick, and returns it.* (" + str(success) + " successful " + throws + ".)"
                stickmessage = await message.channel.send(response.format(message))
                await throw.delete()
            else:
                hiscore = addfetchscore(message,success)
                response = "*Looks at you puzzled.* (" + str(success) + " successful " + throws + ". Your high score is " + str(hiscore) + ".)"
                await message.channel.send(response.format(message))
                await throw.delete()
                play = False

async def fetchhiscores(message):
    cursor = sqlConn.cursor()
    #await message.guild.chunk(cache=True)
    cursor.execute('EXEC corgi.GetFetchLeaderboard ?, ?;',message.guild.id,message.author.id)
    UserDID = None
    Fetches = None
    Rank = None
    Row = None
    HiScores = "```none\nRank|User                            |Fetches\n----|--------------------------------|-------"
    for scores in cursor:
        UserDID=scores[0]
        Fetches=scores[1]
        Rank=scores[2]
        #User = discord.utils.get(message.guild.members, id=UserDID)
        User = message.guild.get_member(UserDID)
        if User is None:
            Username = "Left User (" + str(UserDID) + ")"
        else:
            Username = User.display_name
        Row = "\n" + ("    " + str(Rank))[-4:] + "|" + (Username + "                                ")[:32] + "|" + str(Fetches)
        if Rank > 10:
            HiScores = HiScores + "\n----|--------------------------------|-------"
        HiScores = HiScores + Row
    HiScores = HiScores + "\n```"
    HiScores = HiScores.format(HiScores)
    sqlConn.commit()
    cursor.close()
    embed = discord.Embed(color=discord.Colour.orange()) #description=message.mentions[0].display_name
    embed.add_field(name="Fetch High Scores", value=HiScores, inline=False)
    await message.channel.send(embed=embed)