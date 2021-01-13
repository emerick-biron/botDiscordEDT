import requests
from icalendar import Calendar
from datetime import *
from pytz import timezone
from operator import itemgetter
import json


def get_token():
    file = open("token.txt", 'r')
    token = file.read()
    file.close()
    return token


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


def print_cal_today(ctx, d):
    res = []
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
        calendar = requests.get(data[str(ctx.message.author)]).text
        cal = Calendar.from_ical(calendar)
    except KeyError:
        return ("Aucun lien iCal n'a été définit.\nPour en définir un faites : ``?linkICal {lien iCal}``\nPour plus "
                "d'informations faites : ``?help``")
    else:
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