#!/usr/bin/env python3
import discord, discord.utils, random, os, re, json, sys, time, secrets

async def german(client,message):
    #define checks
    def winnerResponse(r,u):
        return r.message.id == winner.id and u.id == message.author.id and r.emoji in ("✅","❎")
    def tableResponse(r,u):
        return r.message.id == table.id and u.id == winningPlayer.id and r.emoji in ("1️⃣","3️⃣")
    def winnerDm(m):
        return m.author.id == winningPlayer.id and m.channel.type == discord.ChannelType.private
    def loserDm(m):
        return m.author.id == losingPlayer.id and m.channel.type == discord.ChannelType.private

    #What emojis we got?
    greenTick = "✅"
    greenCross = "❎"
    oneDigit = "1️⃣"
    threeDigit = "3️⃣"

    #Who won the roll?
    response = "Did you win the dice roll, " + message.author.display_name + "?"
    winner = await message.channel.send(response.format(message))
    await winner.add_reaction(greenTick)
    await winner.add_reaction(greenCross)
    #Get that reaction
    try:
        reply = await client.wait_for('reaction_add',check=winnerResponse,timeout=10)
    except:
        response = "No response received. Pairing cancelled. If you have not yet rolled off, each use the `$roll` command."
        await message.channel.send(response.format(message))
        return
    
    #Set winner/loser based on reaction
    if reply[0].emoji == greenCross:
        response = "You lost the dice roll, " + message.mentions[0].display_name +" gets to choose the first table."
        winningPlayer = message.mentions[0]
        losingPlayer = message.author
    else:
        response = "You won the dice roll, you get to choose the first table."
        winningPlayer = message.author
        losingPlayer = message.mentions[0]
    await message.channel.send(response.format(message))

    #What table do you want, winner?
    response = winningPlayer.display_name + " what table would you like to place your first player card on?"
    table = await message.channel.send(response.format(message))
    await table.add_reaction(oneDigit)
    await table.add_reaction(threeDigit)
    #Get that reaction
    try:
        reply = await client.wait_for('reaction_add',check=tableResponse,timeout=180)
    except:
        response = "No response received. Pairing cancelled."
        await message.channel.send(response.format(message))
        return
    #Set table order for selection
    if reply[0].emoji == oneDigit:
        firstTable = oneDigit
        secondTable = threeDigit
    else:
        firstTable = threeDigit
        secondTable = oneDigit
    
    #Get Winning Player First Card
    response = winningPlayer.display_name + " has chosen to place their first card on table " + firstTable + ". Please reply to the DM to confirm the player, and casters, that will you will be placing on this table."
    await message.channel.send(response.format(message))
    dm = "Please respond with the Player Name, and their casters, that you would like to play on table " + firstTable + ". For example: Thom: Lucant and Aurora2"
    await winningPlayer.send(dm.format(message))
    try:
        winnerFirstPlayer = await client.wait_for('message',check=winnerDm,timeout=600)
    except:
        response = "No response received to DM. Pairing cancelled."
        await message.channel.send(response.format(message))
        return
    response = winningPlayer.display_name + " has chosen their first card. " + losingPlayer.display_name + " please reply to the DM to confirm the player, and casters, that will you will be placing on table " + secondTable + "."
    await message.channel.send(response.format(message))
    #Get Losing Player First Card
    dm = "Please respond with the Player Name, and their casters, that you would like to play on table " + secondTable + ". For example: Thom, Lucant and Aurora2"
    await losingPlayer.send(dm.format(message))
    try:
        loserFirstPlayer = await client.wait_for('message',check=loserDm,timeout=600)
    except:
        response = "No response received to DM. Pairing cancelled."
        await message.channel.send(response.format(message))
        return
    response = winningPlayer.display_name + " has chosen to play the following card on table " + firstTable + ": " + winnerFirstPlayer.content + "\n" + losingPlayer.display_name + " has chosen to play the following card on table " + secondTable + ": " + loserFirstPlayer.content
    await message.channel.send(response.format(message))
    response = winningPlayer.display_name + " please respond to the DM to confirm what card will be played on table " + firstTable + "."
    await message.channel.send(response.format(message))

    #Get Winning Player Second Card
    dm = "Please respond with your Opponent's Player Name, and their casters, that you would like to play against on table " + firstTable + ". This will be against your card: " + winnerFirstPlayer.content + ". For example: Ryan, Harbinger and Feora4"
    await winningPlayer.send(dm.format(message))
    try:
        winnerSecondPlayer = await client.wait_for('message',check=winnerDm,timeout=600)
    except:
        response = "No response received to DM. Pairing cancelled."
        await message.channel.send(response.format(message))
        return
    response = winningPlayer.display_name + " has chosen their second card. " + losingPlayer.display_name + " please reply to the DM to confirm the player, and casters, that will you will be placing on table " + secondTable + "."
    await message.channel.send(response.format(message))

    #Get Losing Player Second Card
    dm = "Please respond with your Opponent's Player Name, and their casters, that you would like to play against on table " + secondTable + ". This will be against your card: " + loserFirstPlayer.content + ".  For example: Ryan, Harbinger and Feora4"
    await losingPlayer.send(dm.format(message))
    try:
        loserSecondPlayer = await client.wait_for('message',check=loserDm,timeout=600)
    except:
        response = "No response received to DM. Pairing cancelled."
        await message.channel.send(response.format(message))
        return
    #We did it!!!
    opponents = "All player cards have been chosen!\n"
    #Tell people who they are playing
    if firstTable == oneDigit:
        opponents = opponents + "1️⃣: " + winnerFirstPlayer.content + " **VS** " + winnerSecondPlayer.content + "\n2️⃣: Players that were not selected.\n3️⃣: " + loserSecondPlayer.content + " **VS** " + loserFirstPlayer.content
    else:
        opponents = opponents + "1️⃣: " + winnerSecondPlayer.content + " **VS** " + winnerFirstPlayer.content + "\n2️⃣: Players that were not selected.\n3️⃣: " + loserFirstPlayer.content + " **VS** " + loserSecondPlayer.content
    await message.channel.send(opponents.format(message))
    return