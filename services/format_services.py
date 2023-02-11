from datetime import datetime


class FormatServices:
    _mothDict = {"ene": "jan", "feb": "feb", "mar": "mar", "abr": "apr", "may": "may", "jun": "jun", "jul": "jul",
                 "ago": "aug", "sept": "sep", "oct": "oct", "nov": "nov", "dic": "dec"}

    @staticmethod
    def parseReviewCountToNumber(reviewCountStr: str):
        split = reviewCountStr.strip().split("\n")[0].split(" ")

        if split[1].strip() == "M":
            return round(float(split[0].strip().replace(",", ".")) * 1000000)
        elif split[1].strip() == "mil":
            return round(float(split[0].strip().replace(",", ".")) * 1000)
        else:
            return int(split[0].strip())

    @staticmethod
    def parseReviewScore(reviewScoreStr: str):
        split = reviewScoreStr.strip().split("\n")[0]
        return float(split.replace(",", "."))

    @staticmethod
    def parseDownloadsCount(downloadsCountStr: str):
        split = downloadsCountStr.split(" ")[0].strip().replace("+", "").replace(".", "")
        return int(split)

    @staticmethod
    def parseDateToMillis(dateInStr: str):
        dateInStr = dateInStr.lower()

        for i in FormatServices._mothDict:
            dateInStr = dateInStr.replace(i, FormatServices._mothDict[i])

        return round(datetime.strptime(dateInStr, "%d %b %Y").timestamp() * 1000)
