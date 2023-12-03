from datetime import datetime

import requests


class HttpServices:

    def uploadFile(self, url, pathOfFile: str):
        result = requests.post(url, {"api_key": "Lvf8M6qM0xCkJBbGpc5xS0C4CPFQ5WLqkL2Xn1b9Hk9feHoO36L2L98jkA1wGkk3"},
                               files={"items": open(pathOfFile, "rb")})

        result = result.json()
        with open("log.txt", "a", encoding="UTF8") as f:
            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            f.write(date + " | " + str(result) + "\n")
            f.close()


instance: HttpServices = HttpServices()
