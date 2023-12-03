import json

from services.selenium_services import instance as seleniumServices

from services.http_services import instance as httpServices

import os


class SyncEngine:

    def __init__(self):
        self.syncWithServer()

    def syncWithServer(self):

        niches = open("niches.txt", "r", encoding="UTF8").read().split("\n")
        send = []

        index = 0

        for i in niches:
            data = seleniumServices.getCategoricalAppData(i, getCategories=True)
            if data is not None:
                data["logo_url"] = seleniumServices.getLogoUrl().split("=")[0] + "=w240"
                data["app_url"] = i
                send.append(data)
                index += 1
                print("Update: " + str(index) + "/" + str(len(niches)))
            else:
                print("Error en " + i)

        if os.path.exists("niches.json"):
            os.remove("niches.json")

        f = open("niches.json", "w", encoding="UTF8")
        f.write(json.dumps(send))
        f.close()

        httpServices.uploadFile("https://ia-pplication.com/my-files/sync-potential-niches", "niches.json")
