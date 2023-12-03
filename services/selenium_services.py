import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from services.format_services import FormatServices
import requests
import wget
import zipfile
import os

import pathlib
import time

from glob import glob


class SeleniumServices:

    def __init__(self, useEdge=False, lang="es"):

        driverPath = self.downloadWebDriverAuto()

        if useEdge is True:
            options = webdriver.EdgeOptions()
        else:
            options = webdriver.ChromeOptions()

        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--incognito")
        options.add_argument("--headless=new")
        # options.add_argument("--lang=" + lang)

        if useEdge is True:
            driver = webdriver.Edge(driverPath, options=options)
        else:
            driver = webdriver.Edge(driverPath, options=options)

        driver.set_window_position(2400, 0)
        driver.maximize_window()
        self.driver = driver

    def getDriver(self):
        return self.driver

    def scrollPageToFinish(self, driver: webdriver, element):

        lastHeight = 0

        trys = 0

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            try:
                WebDriverWait(driver, timeout=1).until(ec.element_to_be_clickable(
                    (By.XPATH, "/html/body/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/div/div/span"))).click()
                time.sleep(5)
            except:
                pass

            if int(element.size["height"]) != lastHeight:
                lastHeight = int(element.size["height"])
                trys = 0
            else:
                trys += 1

            if trys > 5:
                break

            time.sleep(1)

        return True

    def getCategoricalAppData(self, urlBase: str, getCategories=False, onlyLoad=False):

        """
        :param urlBase: La cadena que contiene la URL a analizar
        :return: None en caso de que falle o la cedena esté mal, un diccionario en caso de que todo haya ido correctamnete.
        """
        if urlBase is None or urlBase == "" or "details?id" not in urlBase:
            return None

        self.driver.get(urlBase)

        if onlyLoad is True:
            return None

        # Todo, revisar a ver de donde podemos sacar el título de la app
        title = self.driver.find_elements(By.TAG_NAME, "h1")
        if len(title) > 0:
            title = title[0].text
        else:
            print("No se ha podido extraer el título: " + urlBase)
            return None

        isApp = True

        # Es el contenido de la sección de "Información de la app"
        h2 = [
            "/html/body/c-wiz[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[2]/div/section/header/div/div[1]/h2",
            "/html/body/c-wiz[3]/div/div/div[1]/div[2]/div/div[1]/c-wiz[2]/div/section/header/div/div[1]/h2",
            "/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[2]/div/section/header/div/div[1]/h2",
            "/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/div[1]/c-wiz[2]/div/section/header/div/div[1]/h2",
        ]

        for i in h2:
            try:
                temp = self.driver.find_element(By.XPATH, i)
                isApp = "aplicación" in str(temp.text).strip().lower()
                break

            except Exception as e:
                pass

        categories = []

        try:
            if getCategories is True:

                # Es el contenedor del listado de categorías
                catXpaths = [
                    "/html/body/c-wiz[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[2]/div/section/div/div[3]",
                    "/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/div[1]/c-wiz[2]/div/section/div/div[3]",
                    "/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[2]/div/section/div/div[3]"
                ]

                for i in catXpaths:
                    try:
                        categoriesContainer = self.driver.find_element(By.XPATH, i)
                        if categoriesContainer is not None:
                            categories = [item.get_attribute("href") for item in
                                          categoriesContainer.find_elements(By.TAG_NAME, "a")]

                    except Exception as e:
                        pass

            infoButtons = [
                "/html/body/c-wiz[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[2]/div/section/header/div/div[2]/button",
                "/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/div[1]/c-wiz[2]/div/section/header/div/div[2]/button",
                "/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[2]/div/section/header/div/div[2]/button"
            ]

            for i in infoButtons:
                try:
                    WebDriverWait(self.driver, 1).until(ec.element_to_be_clickable((By.XPATH, i))).click()
                    break
                except:
                    continue

            time.sleep(200 / 1000)

            closeButtons = [
                "/html/body/div[4]/div[2]/div/div/div/div/div[1]/button",
                "/html/body/div[4]/div[2]/div/div/div/div/button"
            ]

            closeButton = None
            for i in closeButtons:
                try:
                    closeButton = WebDriverWait(self.driver, 1).until(
                        ec.element_to_be_clickable((By.XPATH, i)))
                    break
                except:
                    continue

            if closeButton is None:
                return None

            dataContainers = [
                "/html/body/div[4]/div[2]/div/div/div/div[1]/div[2]",
                "/html/body/div[4]/div[2]/div/div/div/div[2]/div[3]",
                "/html/body/div[4]/div[2]/div/div/div/div/div[2]/div[3]",
                "/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[3]",

            ]

            data = None
            for i in dataContainers:
                try:
                    data = self.driver.find_element(By.XPATH, i)
                    break
                except:
                    continue

            if data is None:
                return None

            divs = data.find_elements(By.TAG_NAME, "div")

            downloads = ""

            for i in range(len(divs)):
                if "descargas" in divs[i].text.lower() and len(divs[i].find_elements(By.TAG_NAME, "div")) <= 0:
                    downloads = divs[i + 1].text
                    break

            downloads = FormatServices.parseDownloadsCount(downloads)

            release = ""

            try:
                for i in range(len(divs)):
                    if "fecha de publicación" in divs[i].text.lower() and len(
                            divs[i].find_elements(By.TAG_NAME, "div")) <= 0:
                        release = divs[i + 1].text
                        break
                release = FormatServices.parseDateToMillis(release)
            except:
                print("No se ha podido capturar la fecha")

            closeButton.click()

            reviewCount = self.driver.find_element(By.XPATH,
                                                   "/html/body/c-wiz[2]/div/div/div[2]/div[1]/div/div/c-wiz/div[2]/div[2]/div/div/div[1]/div[2]").text.strip()

            if ("descargas" not in reviewCount.lower()):
                try:
                    reviewCount = FormatServices.parseReviewCountToNumber(reviewCount)
                except:
                    reviewCount = 0
            else:
                reviewCount = 0

            try:
                reviewScore = self.driver.find_element(By.XPATH,
                                                       "/html/body/c-wiz[2]/div/div/div[2]/div[1]/div/div/c-wiz/div[2]/div[2]/div/div/div[1]/div[1]/div/div").text.strip()
            except:
                reviewScore = ""

            if reviewScore != "":
                reviewScore = FormatServices.parseReviewScore(reviewScore)
            else:
                reviewScore = 0.0

            isThatPay = False

            try:
                temp = self.driver.find_element(By.XPATH,
                                                "/html/body/c-wiz[2]/div/div/div[2]/div[1]/div/div/div/div[1]/div/c-wiz/div/div/div/div/button")

                if temp is not None and "comprar" in temp.text.lower():
                    isThatPay = True
            except:
                pass

            # some can be None, check always
            return {"downloads": downloads, "release": release, "review_count": reviewCount,
                    "review_score": reviewScore, "is_that_pay": isThatPay, "is_app": isApp, "categories": categories,
                    "app_title": title}

        except Exception as e:
            return None

    def getAppScreensLinks(self, urlApp: str, forceLoad=True):

        if forceLoad:
            self.driver.get(urlApp)

        time.sleep(1)

        try:
            container = self.driver.find_element(By.XPATH,
                                                 "/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[1]/div/div/div[1]")
        except Exception as e:
            try:
                container = self.driver.find_element(By.XPATH,
                                                     "/html/body/c-wiz[5]/div/div/c-wiz/c-wiz[2]/c-wiz/section/div/div/div[1]/div[2]/c-wiz/div/div/div[1]")
            except Exception as j:
                container = None

        imgs = container.find_elements(By.TAG_NAME, "img")
        links = [i.get_attribute("src") for i in imgs]

        return links if links is not None else None

    logos = [
        "/html/body/c-wiz[2]/div/div/div[2]/div[1]/div/div/c-wiz/div[1]/img[1]",
        "/html/body/c-wiz[2]/div/div/div[2]/div[1]/div/div/c-wiz/div[2]/div[2]/div/img",
        "/html/body/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[2]/div/img",
        "/html/body/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[1]/img[1]",
    ]

    def getLogoUrl(self):

        logo = None
        index = 0

        for i in self.logos:
            try:
                logo = self.driver.find_element(By.XPATH, i)
                if ".jpg" in logo.get_attribute("src") or ".png" in logo.get_attribute("src"):
                    continue
                break
            except:
                if index == 0:
                    index += 1
                else:
                    print("Logo no encontrado: " + i)

        if logo is None:
            return None

        logo = logo.get_attribute("src")
        return logo

    def _getLinks(self, driver):

        return [i.get_attribute("href") for i in driver.find_elements(By.TAG_NAME, "a")]

    def closeWindow(self):
        self.driver.close()

    def getAppPageUrls(self, urlBase: str):
        self.driver.set_page_load_timeout(10)
        self.driver.set_script_timeout(10)
        self.driver.implicitly_wait(2)
        try:
            self.driver.get(urlBase)
        except Exception as e:
            print(e)
            return None
        links = self._getLinks(self.driver)
        self.driver.stop_client()
        return links

    def getHomeUrls(self, urlBase: str):

        if urlBase is None or urlBase == "":
            raise Exception("La url enviada no es válida")

        self.driver.get(urlBase)

        self.scrollPageToFinish(self.driver,
                                self.driver.find_element(By.XPATH, "/html/body/c-wiz[2]/div/div/div[1]/c-wiz"))

        sendLinks = self._getLinks(self.driver)

        return sendLinks

    def downloadWebDriverAuto(self):

        """
        chromedriver_autoinstaller.install()
        return
        """

        # get the latest chrome driver version number
        url = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'
        response = requests.get(url)
        version_number = response.json()
        version_number = version_number['channels']["Stable"]["downloads"]["chromedriver"]
        path = ""
        for i in version_number:
            if i["platform"] == "win64":
                path = i["url"]

        if path == "":
            return

        # build the donwload url

        # download the zip file using the url built above
        latest_driver_zip = wget.download(path, 'chromedriver.zip')

        try:
            # extract the zip file
            with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
                zip_ref.extractall("assets")  # you can specify the destination folder path here
            os.remove(latest_driver_zip)
        except:
            pass

        item = glob("assets/**/*", recursive=True)
        for i in item:
            if "chromedriver.exe" in i:
                return i

        return ""


instance: SeleniumServices = SeleniumServices()
