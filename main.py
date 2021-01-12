import requests
from icalendar import Calendar
from datetime import *
from pytz import timezone
import locale
from operator import itemgetter
import discord
from discord.ext import commands


def get_desc(description):
    a = description.strip("\n").split("\n")
    res = "\n".join(a[:-1])
    return res


def get_res_str(res):
    result = ""
    longueur = len(res)
    c = 0
    if longueur == 0:
        result = "Aucun cours aujourd'hui"
    else:
        for cours in res:
            c += 1
            for i in cours:
                result += i + "\n"
            if c != longueur:
                result += "\n"
    return result


def print_cal(cal):
    for component in cal.walk():
        if component.name == "VEVENT":
            print(component.get('summary'))
            print(get_desc(component.get('description')))
            print(component.get('location'))
            print(component.decoded('dtstart').time(), "-", component.decoded('dtend').time())
            print("-------------------------")


def print_cal_today(d):
    res = []
    for component in cal.walk():
        if component.name == "VEVENT":
            summary = component.get('summary')
            dtstart = component.decoded('dtstart')
            dtend = component.decoded('dtend')
            description = get_desc(component.get('description'))
            location = component.get('location')
            dtstart = dtstart.astimezone(timezone("Europe/Paris"))
            dtend = dtend.astimezone(timezone("Europe/Paris"))
            if d.date() == dtstart.date():
                time = dtstart.time().isoformat('minutes') + " - " + dtend.time().isoformat('minutes')
                res.append([summary, time, description, location])
    res = sorted(res, key=itemgetter(1))
    result = "**"
    result += d.strftime("%A %d %B %Y")
    result += "**"
    result += "```"
    result += "\n\n"
    result += get_res_str(res)
    result += "```"
    return result


bot = commands.Bot(command_prefix='!', help_command=None)


@bot.event
async def on_ready():
    locale.setlocale(locale.LC_TIME, '')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("!help"))
    print("Ready!")


@bot.command()
async def linkICal(ctx, link):
    global url
    global calendar
    global cal
    url = link
    try:
        calendar = requests.get(url).text
        cal = Calendar.from_ical(calendar)
    except:
        await ctx.send("URL invalide")
    else:
        await ctx.send("Linked !")


@bot.command()
async def today(ctx):
    try:
        await ctx.send(print_cal_today(datetime.today()))
    except NameError:
        await ctx.send(
            "Aucun lien iCal n'a été définit.\nPour en définir un faites : ``!linkICal {lien iCal}``\nPour plus "
            "d'informations faites : ``!help``")


@bot.command()
async def helpICal(ctx):
    text = "**Obtenir lien iCal :**\n\n"
    text += "Pour obtenir votre lien iCal rendez vous sur l'ENT > Planning 20-21.\n"
    text += "Sélectionnez votre(s) groupe(s) d'enseignement(s) dans l'onglet Préférences.\n"
    text += "Rendez vous dans l'onglet iCal et sélectionnez le lien présent.\n"
    text += "Attention ce lien iCal n'est valable que pour la sélection actuelle de vos groupes d'enseignement. Si " \
            "vous modifiez votre sélection de groupes d'enseignement il faut ré-exécuter la commande ``!linkICal {" \
            "lien iCal}`` avec le nouveau lien iCal"
    await ctx.send(text)


@bot.command()
async def help(ctx):
    text = "**Commandes EDT :**\n\n"
    text += ":small_blue_diamond:``!linkICal {lien iCal}`` : permet de lier le bot avec votre EDT personnel. Pour " \
            "savoir comment obtenir ce lien faites : ``!helpICal``.\n"
    text += ":small_blue_diamond:``!today`` : permet d'obtenir votre emploi du temps du jour.\n"
    text += ":small_blue_diamond:``!help`` : avoir un aperçu des commandes.\n"
    await ctx.send(text)


token = "Nzk4NTc2MTc5OTI5Mjg0NjQ5.X_3CBg.yMEAV1hqJ7XqY3Hgep2poWyXe98"
bot.run(token)
