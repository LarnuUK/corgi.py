import discord, discord.utils, random, os, re, json, sys, time, secrets, pyodbc
from decimal import Decimal

def validDecimal(m):
    try:
        s = Decimal(m)
        return True
    except:
        return False

async def loscheck(client,message):
    def isSize(r,u):
        return r.message.id == size.id and u.id == message.author.id and r.emoji in ("🇸","🇲","🇱","🇭")
    def isSameChannel(m):
        return m.channel.id == reply.channel.id and m.author.id == message.author.id
        
    response = "Is the model you are drawing LOS ***from*** a 🇸mall, 🇲edium, 🇱arge, or 🇭uge base model?"
    size = await message.channel.send(response.format(message))
    await size.add_reaction("🇸")
    await size.add_reaction("🇲")
    await size.add_reaction("🇱")
    await size.add_reaction("🇭")
    try:
        m1size = await client.wait_for('reaction_add',check=isSize,timeout=10)
    except:
        response = "No response received. Cancelled LOS checking."
        await message.channel.send(response.format(message))
        return
    if m1size[0].emoji == "🇸":
        m1 = "s"
    elif m1size[0].emoji == "🇲":
        m1 = "m"
    elif m1size[0].emoji == "🇱":
        m1 = "l"
    elif m1size[0].emoji == "🇭":
        m1 = "h"
    response = "Is the model you are drawing LOS ***to*** a 🇸mall, 🇲edium, 🇱arge, or 🇭uge base model?"
    size = await message.channel.send(response.format(message))
    await size.add_reaction("🇸")
    await size.add_reaction("🇲")
    await size.add_reaction("🇱")
    await size.add_reaction("🇭")
    try:
        m2size = await client.wait_for('reaction_add',check=isSize,timeout=10)
    except:
        response = "No response received. Cancelled LOS checking."
        await message.channel.send(response.format(message))
        return
    if m2size[0].emoji == "🇸":
        m2 = "s"
    elif m2size[0].emoji == "🇲":
        m2 = "m"
    elif m2size[0].emoji == "🇱":
        m2 = "l"
    elif m2size[0].emoji == "🇭":
        m2 = "h"
    validreply = False
    response = "How tall is the intervening building in inches?"
    reply = await message.channel.send(response.format(message))
    while validreply == False:
        try:
            buildingy = await client.wait_for('message',check=isSameChannel,timeout=10)
        except:
            response = "No response received. Cancelled LOS checking."
            await message.channel.send(response.format(message))
            return
        if validDecimal(buildingy.content):
            validreply = True
        else:
            response = "Height must be a numerical value, for example: 7.2. How tall is the intervening building in inches?"
            reply = await message.channel.send(response.format(message))
    response = "How wide is the intervening building in inches where LOS is being drawn?"
    reply = await message.channel.send(response.format(message))
    validreply = False
    while validreply == False:
        try:
            buildingx = await client.wait_for('message',check=isSameChannel,timeout=10)
        except:
            response = "No response received. Cancelled LOS checking."
            await message.channel.send(response.format(message))
            return
        if validDecimal(buildingx.content):
            validreply = True
        else:
            response = "Width must be a numerical value, for example: 7.2. How wide is the intervening building in inches?"
            reply = await message.channel.send(response.format(message))
    response = "How far is the intervening building from where LOS is being drawn in inches?"
    reply = await message.channel.send(response.format(message))
    validreply = False
    while validreply == False:
        try:
            buildingdist = await client.wait_for('message',check=isSameChannel,timeout=10)
        except:
            response = "No response received. Cancelled LOS checking."
            await message.channel.send(response.format(message))
            return
        if validDecimal(buildingdist.content):
            validreply = True
        else:
            response = "Distance must be a numerical value, for example: 7.2. How far is the intervening building from where LOS is being drawn in inches?"
            reply = await message.channel.send(response.format(message))
    response = "How far are the models from each other in inches?"
    reply = await message.channel.send(response.format(message))
    validreply = False
    while validreply == False:
        try:
            modeldist = await client.wait_for('message',check=isSameChannel,timeout=10)
        except:
            response = "No response received. Cancelled LOS checking."
            await message.channel.send(response.format(message))
            return
        if validDecimal(modeldist.content):
            validreply = True
        else:
            response = "Distance must be a numerical value, for example: 7.2. How far is the are the models from each other in inches?"
            reply = await message.channel.send(response.format(message))
    response = "https://fishcord.larnu.uk/corgi/loschecker/loschecker.php?m1="+m1+"&m2="+m2+"&buildingx="+buildingx.content+"&buildingy="+buildingy.content+"&builddist="+buildingdist.content+"&modeldist="+modeldist.content
    reply = await message.channel.send(response.format(message))