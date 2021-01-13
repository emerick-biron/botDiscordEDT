# -*- coding: utf-8 -*-
import locale
import discord
from discord.ext import commands
from functions import *

bot = commands.Bot(command_prefix='?', help_command=None)


@bot.event
async def on_ready():
    locale.setlocale(locale.LC_TIME, '')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("?help"))
    print("Ready!")


@bot.command()
async def linkICal(ctx, link):
    url = link
    try:
        calendar = requests.get(url).text
    except:
        await ctx.send("URL invalide")
    else:
        key = str(ctx.message.author)
        with open("data.json", "r") as f:
            data = json.load(f)
            data[key] = url
        with open("data.json", "w") as f:
            json.dump(data, f)
        await ctx.send("Linked !")


@bot.command()
async def today(ctx):
    try:
        await ctx.send(print_cal_today(ctx, datetime.today()))
    except NameError:
        await ctx.send(
            "Aucun lien iCal n'a été définit.\nPour en définir un faites : ``?linkICal {lien iCal}``\nPour plus "
            "d'informations faites : ``?help``")


@bot.command()
async def helpICal(ctx):
    text = "**Obtenir lien iCal :**\n\n"
    text += "Pour obtenir votre lien iCal rendez vous sur l'ENT > Planning 20-21.\n"
    text += "Sélectionnez votre(s) groupe(s) d'enseignement(s) dans l'onglet Préférences.\n"
    text += "Rendez vous dans l'onglet iCal et sélectionnez le lien présent.\n"
    text += "Attention ce lien iCal n'est valable que pour la sélection actuelle de vos groupes d'enseignement. Si " \
            "vous modifiez votre sélection de groupes d'enseignement il faut ré-exécuter la commande ``?linkICal {" \
            "lien iCal}`` avec le nouveau lien iCal"
    await ctx.send(text)


@bot.command()
async def help(ctx):
    text = "**Commandes EDT :**\n\n"
    text += ":small_blue_diamond:``?linkICal {lien iCal}`` : permet de lier le bot avec votre EDT personnel. Pour " \
            "savoir comment obtenir ce lien faites : ``?helpICal``.\n"
    text += ":small_blue_diamond:``?today`` : permet d'obtenir votre emploi du temps du jour.\n"
    text += ":small_blue_diamond:``?help`` : avoir un aperçu des commandes.\n"
    await ctx.send(text)


bot.run(get_token())
