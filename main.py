import requests
from icalendar import Calendar, Event
from datetime import *
from pytz import timezone
import locale
from operator import itemgetter
import discord


def getDesc(description):
    a = description.strip("\n").split("\n")
    res = "\n".join(a[:-1])
    return res


def getResStr(res):
    result = ""
    l = len(res)
    c = 0
    if l == 0:
        result = "Aucun cours ajourd'hui"
    else:
        for cours in res:
            c += 1
            for i in cours:
                result += i + "\n"
            if c != l:
                result += "\n"
    return result


def printCal(cal):
    for component in cal.walk():
        if component.name == "VEVENT":
            print(component.get('summary'))
            print(getDesc(component.get('description')))
            print(component.get('location'))
            print(component.decoded('dtstart').time(), "-", component.decoded('dtend').time())
            print("-------------------------")


def printCalToday(d):
    res = []
    for component in cal.walk():
        if component.name == "VEVENT":
            summary = component.get('summary')
            dtstart = component.decoded('dtstart')
            dtend = component.decoded('dtend')
            dtstamp = component.decoded('dtstamp')
            description = getDesc(component.get('description'))
            location = component.get('location')
            dtstart = dtstart.astimezone(timezone("Europe/Paris"))
            dtend = dtend.astimezone(timezone("Europe/Paris"))
            dtstamp = dtstamp.astimezone(timezone("Europe/Paris"))
            if d.date() == dtstart.date():
                time = dtstart.time().isoformat('minutes') + " - " + dtend.time().isoformat('minutes')
                res.append([summary, time, description, location])
    res = sorted(res, key=itemgetter(1))
    print(d.strftime("%A %w %B %Y"), "\n\n")
    print(getResStr(res))


bot = discord.Client()
token = "Nzk4NTc2MTc5OTI5Mjg0NjQ5.X_3CBg.yMEAV1hqJ7XqY3Hgep2poWyXe98"
bot.run(token)

url = "https://proseconsult.umontpellier.fr/jsp/custom/modules/plannings/direct_cal.jsp?data=58c99062bab31d256bee14356aca3f2423c0f022cb9660eba051b2653be722c431b66c493702208e664667048bc04373dc5c094f7d1a811b903031bde802c7f59b21846d3c6254443d7b6e956d3145c6e0d5bac87b70fdd185b8b86771d71211f59e59934f30faea6068e5857005c27f166c54e36382c1aa3eb0ff5cb8980cdb,1"
calendar = requests.get(url).text
cal = Calendar.from_ical(calendar)
today = datetime.today()
d = datetime(2020, 12, 1)
locale.setlocale(locale.LC_TIME, '')

printCalToday(today)
