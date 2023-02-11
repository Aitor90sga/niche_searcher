from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from services.format_services import FormatServices

import pathlib
import time


class SeleniumServices:

    def __init__(self, useEdge=False, lang="es"):

        if useEdge is True:
            options = webdriver.EdgeOptions()
        else:
            options = webdriver.ChromeOptions()

        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--incognito")
        # options.add_argument("--lang=" + lang)

        if useEdge is True:
            driver = webdriver.Edge(str(pathlib.Path().resolve()) + "/assets/msedgedriver.exe", options=options)
        else:
            driver = webdriver.Edge(str(pathlib.Path().resolve()) + "/assets/chromedriver.exe", options=options)

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

    def getCategoricalAppData(self, urlBase: str, getCategories=False):

        """
        :param urlBase: La cadena que contiene la URL a analizar
        :return: None en caso de que falle o la cedena esté mal, un diccionario en caso de que todo haya ido correctamnete.
        """
        if urlBase is None or urlBase == "" or "details?id" not in urlBase:
            return None

        self.driver.get(urlBase)

        isApp = True

        try:
            temp = self.driver.find_element(By.XPATH,
                                            "/html/body/c-wiz[3]/div/div/div[1]/div[2]/div/div[1]/c-wiz[2]/div/section/header/div/div[1]/h2")

            isApp = "aplicación" in str(temp.text).strip().lower()


        except Exception as e:
            try:
                temp = self.driver.find_element(By.XPATH,
                                                "/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[2]/div/section/header/div/div[1]/h2")

                isApp = "aplicación" in str(temp.text).strip().lower()

            except Exception as j:
                print("Algo ha fallado")

        categories = []

        try:

            if getCategories is True:
                try:
                    categoriesContainer = self.driver.find_element(By.XPATH,
                                                                   "/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[2]/div/section/div/div[3]")
                    if categoriesContainer is not None:
                        categories = [item.get_attribute("href") for item in
                                      categoriesContainer.find_elements(By.TAG_NAME, "a")]

                except Exception as e:
                    pass

            WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable((By.XPATH,
                                                                            "/html/body/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[2]/div/section/header/div/div[2]/button"))).click()

            try:
                closeButton = WebDriverWait(self.driver, 3).until(
                    ec.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/div/div/div/div[1]/button")))
            except:
                closeButton = WebDriverWait(self.driver, 3).until(
                    ec.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/div/div/div/button")))

            try:
                data = self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div/div/div[2]/div[3]")
            except:
                data = self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div/div/div/div[2]/div[3]")

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
                                                   "/html/body/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[2]/div/div/div[1]/div[2]").text.strip()

            try:
                reviewCount = FormatServices.parseReviewCountToNumber(reviewCount)
            except:
                reviewCount = 0

            try:
                reviewScore = self.driver.find_element(By.XPATH,
                                                       "/html/body/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[2]/div/div/div[1]/div[1]/div/div").text.strip()
            except:
                reviewScore = ""

            isThatPay = False

            try:
                temp = self.driver.find_element(By.XPATH,
                                                "/html/body/c-wiz[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div/c-wiz/div/div/div/div/button")

                if temp is not None and "comprar" in temp.text.lower():
                    isThatPay = True
            except:
                pass

            if reviewScore != "":
                reviewScore = FormatServices.parseReviewScore(reviewScore)
            else:
                reviewScore = 0.0

            # some can be None, check always
            return {"downloads": downloads, "release": release, "review_count": reviewCount,
                    "review_score": reviewScore, "is_that_pay": isThatPay, "is_app": isApp, "categories": categories}

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

    def getLogoUrl(self):
        try:
            logo = self.driver.find_element(By.XPATH,
                                            "/html/body/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[2]/div/img")
        except:
            logo = self.driver.find_element(By.XPATH,
                                            "/html/body/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[1]/img[1]")
        logo = logo.get_attribute("src")
        return logo

    def _getLinks(self, driver):
        links = driver.find_elements(By.TAG_NAME, "a")
        sendLinks = [i.get_attribute("href") for i in links]
        return sendLinks

    def closeWindow(self):
        self.driver.close()
