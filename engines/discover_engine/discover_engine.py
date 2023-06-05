from services.selenium_services import SeleniumServices
from services.google_play_services import GooglePlayServices
from models.gp_url_base_model import GpUrlBaseModel


class DiscoverEngine:
    locale = "es_ES"

    categories = [
        "TOOLS",
        "LIFESTYLE",
        "SPORTS",
        "HEALTH_AND_FITNESS",
        "SHOPPING",
        "SOCIAL",
        "COMMUNICATION",
        "PRODUCTIVITY",
        "VIDEO_PLAYERS",
        "FINANCE",
        "ENTERTAINMENT",
        "MUSIC_AND_AUDIO",
        "TRAVEL_AND_LOCAL",
        "ANDROID_WEAR",
        "WATCH_FACE",
        "ART_AND_DESIGN",
        "AUTO_AND_VEHICLES",
        "BEAUTY",
        "LIBRARIES_AND_DEMO",
        "HOUSE_AND_HOME",
        "DATING",
        "FOOD_AND_DRINK",
        "COMICS",
        "EDUCATION",
        "BUSINESS",
        "EVENTS",
        "PHOTOGRAPHY",
        "GAME",
        "BOOKS_AND_REFERENCE",
        "MAPS_AND_NAVIGATION",
        "MEDICAL",
        "MUSIC_AND_AUDIO",
        "FAMILY",
        "NEWS_AND_MAGAZINES",
        "PERSONALIZATION",
        "HEALTH_AND_FITNESS",
        "PARENTING",
        "WEATHER",
    ]

    def __init__(self, locale: str):
        self.locale = locale
        self.langs = [
            "&hl=en&gl=US",
            "&hl=es&gl=ES",
            "&hl=es&gl=US",
            "&hl=es&gl=419",
            "&hl=af",
            "&hl=de&gl=DE",
            "&hl=am",
            "&hl=hy&gl=AM",
            "&hl=bn&gl=BD",
            "&hl=be",
            "&hl=my&gl=MY",
            "&hl=bg",
            "&hl=kn&gl=IN",
            "&hl=ca",
            "&hl=cs&gl=CZ",
            "&hl=zh&gl=HK",
            "&hl=zh&gl=CN",
            "&hl=zh&gl=TW",
            "&hl=si&gl=LK",
            "&hl=ko&gl=KR",
            "&hl=hr",
            "&hl=da&gl=DK",
            "&hl=sk",
            "&hl=sl",
            "&hl=sl",
            "&hl=et",
            "&hl=eu&gl=ES",
            "&hl=fi&gl=FL",
            "&hl=fr&gl=CA",
            "&hl=fr&gl=FR",
            "&hl=gl&gl=ES",
            "&hl=ka&gl=GE",
            "&hl=el&gl=GR",
            "&hl=iw&gl=IL",
            "&hl=hi&gl=IN",
            "&hl=hu&gl=HU",
            "&hl=en&gl=IN",
            "&hl=en&gl=SG",
            "&hl=en&gl=ZA",
            "&hl=en&gl=AU",
            "&hl=en&gl=CA",
            "&hl=en&gl=GB",
            "&hl=is&gl=IS",
            "&hl=it&gl=IT",
            "&hl=ja&gl=JP",
            "&hl=km&gl=KH",
            "&hl=kk",
            "&hl=ky&gl=KG",
            "&hl=lo&gl=LA",
            "&hl=lv",
            "&hl=lt",
            "&hl=mk&gl=MK",
            "&hl=ms",
            "&hl=ms&gl=MY",
            "&hl=ml&gl=IN",
            "&hl=mn&gl=MN",
            "&hl=nl&gl=NL",
            "&hl=ne&gl=NP",
            "&hl=no&gl=NO",
            "&hl=fa&gl=IR",
            "&hl=fa&gl=AF",
            "&hl=fa&gl=AE",
            "&hl=fa",
            "&hl=pl&gl=PL",
            "&hl=pt&gl=BR",
            "&hl=pt&gl=PT",
            "&hl=pa",
            "&hl=ro",
            "&hl=sr",
            "&hl=sw",
            "&hl=sv&gl=SE",
            "&hl=th",
            "&hl=ta&gl=IN",
            "&hl=te&gl=IN",
            "&hl=tr&gl=TR",
            "&hl=vi",
            "&hl=zu",
            "&hl=ar",
        ]

        self.lang = self.langs[0]

        self.init()

    def init(self):

        selServices = SeleniumServices(useEdge=False)

        """
        links = selServices.getHomeUrls("https://play.google.com/store/apps?hl=es&gl=ES")
        links = GooglePlayServices.clearLinksForAppsOnly(links)
        updatedLinks = GpUrlBaseModel.insertAppLinks(links)
        """

        index = 1

        while True:
            try:

                if index % 100 != 0:

                    newLink = GpUrlBaseModel.getNextUrlToSearch()
                    if newLink is None:
                        break

                    links = selServices.getAppPageUrls(newLink + self.lang)

                    if links is None:
                        continue

                    if len(links) == 1 and "https://play.google.com/store" in links[0]:
                        links = selServices.getAppPageUrls(newLink)
                        if len(links) == 1 and "https://play.google.com/store" in links[0]:
                            print("Deleting link: " + newLink)
                            GpUrlBaseModel.delete(newLink)
                            continue

                    links = GooglePlayServices.clearLinksForAppsOnly(links)
                    GpUrlBaseModel.insertAppLinks(links)

                else:

                    for cat in self.categories:
                        links = selServices.getAppPageUrls(
                            "https://play.google.com/store/apps/category/" + cat + "?" + self.lang)
                        links = GooglePlayServices.clearLinksForAppsOnly(links)
                        GpUrlBaseModel.insertAppLinks(links)

                    if self.lang == self.langs[len(self.langs) - 1]:
                        self.lang = self.langs[0]
                    else:
                        for i in range(len(self.langs)):
                            if self.langs[i] == self.lang and i < len(self.langs) - 2:
                                self.lang = self.langs[i + 1]
                                break

            except Exception as e:
                # selServices.getDriver().close()
                break

            index += 1

        print("Ha terminado de buscar urls")
        print("Iniciamos de nuevo en 1 minutos")
        selServices.closeWindow()
        # time.sleep(1)
        self.init()
