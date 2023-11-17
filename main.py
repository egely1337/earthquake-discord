from requests import *
from bs4 import BeautifulSoup, Tag
from bs4 import element
from time import sleep
from dataclasses import dataclass
from discordwebhook import Discord
from json import *
from discord import Color
from datetime import datetime

config = load(open("config.json"))
webhook = Discord(url=config["webhook_url"])

class Deprem:
    def __init__(self, enlem, boylam , tarih, saat, derinlik, buyukluk ,yer) -> None:
        self.tarih = tarih
        self.saat = saat
        self.buyukluk = buyukluk
        self.yer = yer
        self.derinlik = derinlik
        self.enlem = enlem
        self.boylam = boylam
    
    def __hash__(self) -> int:
        return hash(self.tarih + self.saat + self.buyukluk + self.yer + self.derinlik)


def get_earthquakes() -> list[Deprem]:
    url = "https://egely1337.com/api/v1/kandilli?limit=10"
    r = get(url=url)
    d = r.json()
    print(d["earthquakes"])
    return_list: list[Deprem] = []
    for i in d["earthquakes"]:
        yer = i["location"]
        tarih = i["date"]
        enlem = i["latitude"]
        boylam = i["longitude"]
        saat = i["time"]
        buyukluk = i["magnitude"]
        j = Deprem(enlem, boylam, tarih, saat, "null", buyukluk, yer)
        return_list.append(j)
    return return_list

def send_message(deprem:Deprem) -> None:
    timestamp = datetime.strptime(deprem.saat, "%H:%M:%S")
    embed = {
        "title" : "Yeni bir deprem oldu",
        "color" : Color.random().value,
        "fields" : [
            {"name" : "📌 Yer", "value" : "**{}**".format(deprem.yer)},
            {"name" : "📡 Şiddet", "value" : "**{} ML**".format(deprem.buyukluk)}
        ],
        "footer" : {
            "text" : "Kandilli Rasathanesi ● Today at {}".format(timestamp.strftime("%H:%M")),
            "icon_url" : "http://www.koeri.boun.edu.tr/sismo/logos/bulogo-a0.gif"
        },
        "image" : {
            "url" :  "http://static-maps.yandex.ru/1.x/?lang=en-US&ll={},{}&size=450,300&z=10&l=map".format(deprem.boylam,deprem.enlem)
        }
    }
    webhook.post(embeds=[embed])

def main():
    last_index: Deprem = Deprem(1,1,1,1,1,1,1) 
    while True:
        x = get_earthquakes()
        if x[0].__hash__() == last_index.__hash__():
            pass
        elif x[0].__hash__() != last_index.__hash__(): 
            send_message(deprem=x[0])
            last_index = x[0] 
        sleep(120)

main()
