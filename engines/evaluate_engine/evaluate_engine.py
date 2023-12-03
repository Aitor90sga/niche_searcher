from config.app_config import AppConfig
from models.gp_url_base_model import GpUrlBaseModel
from services.selenium_services import SeleniumServices


class EvaluateEngine:

    def __init__(self):
        self.init()

    def init(self):
        selServices = SeleniumServices(False)
        evaluated = 0

        while True:

            nextUrl = GpUrlBaseModel.getNextUrlToScan()

            try:
                data = selServices.getCategoricalAppData(nextUrl, True)

                if data is None:
                    continue

                if data["is_app"] is False:
                    continue

                """
                if data["release"] > AppConfig.dataToEvaluate and data["downloads"] > AppConfig.downloadRequired and \
                        data[
                            "categories"] is not None and len(
                    data["categories"]) > 0 and True in [a in data["categories"] for a in AppConfig.categoriesRequired]:
                    f = open("niches.txt", "a", encoding="UTF8")
                    f.write(nextUrl + "\r\n")
                    f.close()
                    print("Nichos actualizados")
                """

                if data["release"] > AppConfig.dataToEvaluate and data["downloads"] > AppConfig.downloadRequired:
                    f = open("niches.txt", "a", encoding="UTF8")
                    f.write(nextUrl + "\n")
                    f.close()
                    print("Nichos actualizados")

                evaluated += 1
                print("Evaluated: " + str(evaluated) + " " + nextUrl)

            except:
                continue
