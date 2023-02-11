from datetime import timedelta, datetime

from models.gp_url_base_model import GpUrlBaseModel
from services.selenium_services import SeleniumServices

if __name__ == '__main__':

    selServices = SeleniumServices(False)
    now = datetime.now()
    dateRequired = int((now - timedelta(days=365)).timestamp() * 1000)
    downloadRequired = 490000

    while True:
        nextUrl = GpUrlBaseModel.getNextUrlToScan()
        try:
            data = selServices.getCategoricalAppData(nextUrl, True)
            if data is None:
                continue

            if data["is_app"] is False:
                continue

            if data["release"] > dateRequired and data["downloads"] > downloadRequired:
                f = open("niches.txt", "a", encoding="UTF8")
                f.write(nextUrl + "\r\n")
                f.close()
                print("Nichos actualizados")

        except:
            continue
