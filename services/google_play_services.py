from datetime import datetime, timedelta
from config.google_play_config import GooglePlayConfig


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
