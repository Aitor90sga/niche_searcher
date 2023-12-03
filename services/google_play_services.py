from datetime import datetime, timedelta

import requests

from config.google_play_config import GooglePlayConfig
from os.path import exists
from os import makedirs
from services.selenium_services import instance as seleniumServices


class GooglePlayServices:

    @staticmethod
    def clearLinksForAppsOnly(inLinks: list):

        outLinks = []

        for item in inLinks:
            if "details?id=" in item:
                outLinks.append(item.split("&")[0])

        return outLinks

    @staticmethod
    def isAGoodApp(downloads: int, releaseDateInMillis: int, reviewCount: int, reviewScore: float,
                   isThatPay: bool):

        timeSinceRelease = round(datetime.now().timestamp() * 1000) - releaseDateInMillis
        delta = timedelta(milliseconds=timeSinceRelease)

        meanDownloadsPerDay = downloads / delta.days
        meanReviewsPerDay = reviewCount / delta.days
        reviewScoreNormalized = (reviewScore * 100 / GooglePlayConfig.MAX_RATE_VALUE) / 100

        reviewPoints = meanReviewsPerDay * reviewScoreNormalized

        if isThatPay is False:
            reviewPoints = reviewPoints / GooglePlayConfig.REVIEW_SCORE_THRESHOLD
            downloadsPoints = meanDownloadsPerDay / GooglePlayConfig.DOWNLOAD_THRESHOLD
        else:
            reviewPoints = reviewPoints / (GooglePlayConfig.REVIEW_SCORE_THRESHOLD / 4)
            downloadsPoints = meanDownloadsPerDay / (GooglePlayConfig.DOWNLOAD_THRESHOLD / 4)

        return downloadsPoints * reviewPoints > 1

    @staticmethod
    def _downloadFile(fileUrl: str, name: str):
        response = requests.get(fileUrl)

        if response.status_code != 200:
            raise Exception("La descarga ha fallado, la solicitud ha devuelto un error: " + str(response.status_code))

        if exists("assets/temp") is False:
            makedirs("assets/temp")

        baseRoute = "assets/temp/" + name

        if exists(baseRoute):
            return baseRoute

        f = open(baseRoute, mode="wb")
        f.write(response.content)
        f.close()

        response.close()

        return baseRoute

    @staticmethod
    def downloadLogo(fileUrl: str):

        temp = fileUrl.split("=")[0].split("/")
        temp = temp[len(temp) - 1]
        temp = temp.split("=")[0]

        name = temp + ".png"

        try:
            url = GooglePlayServices._downloadFile(fileUrl.split("=")[0] + "=w512", name)
        except:
            url = None

        return url

    @staticmethod
    def getLogoFromAppUrl(urlOfApp: str):
        seleniumServices.getCategoricalAppData(urlOfApp, onlyLoad=True)
        logoUrl = seleniumServices.getLogoUrl()
        return logoUrl
