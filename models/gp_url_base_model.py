import datetime

from models.model import GpUrlBase, getSession
from sqlalchemy import asc


class GpUrlBaseModel:

    @staticmethod
    def insertAppLinks(links: list):

        sendGpUrl = []

        for i in links:
            temp = None
            try:
                temp = getSession().query(GpUrlBase).where(GpUrlBase.url == i).one()
            except:
                pass

            if temp is None:
                temp = GpUrlBase()
                temp.url = i
                temp.register_date = round(datetime.datetime.now().timestamp() * 1000)
                temp.last_view_date = 0
                temp.last_scan_date = 0
                getSession().add(temp)
                sendGpUrl.append(temp)

        #Todo, revisar si esto se puede meter dentro del cloque del if.
        getSession().commit()

        return sendGpUrl

    @staticmethod
    def getNextUrlToSearch():
        try:
            temp = getSession().query(GpUrlBase).order_by(asc(GpUrlBase.last_view_date)).limit(1).one()
            print("Vamos por el: " + str(temp.id))
            temp.last_view_date = round(datetime.datetime.now().timestamp() * 1000)
            getSession().add(temp)
            getSession().commit()
            return temp.url
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def getNextUrlToScan():
        try:
            temp = getSession().query(GpUrlBase).order_by(asc(GpUrlBase.last_scan_date)).limit(1).one()
            print("Vamos por el: " + str(temp.id))
            temp.last_scan_date = round(datetime.datetime.now().timestamp() * 1000)
            getSession().add(temp)
            getSession().commit()
            return temp.url
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def getGpUrlBase(id):
        try:
            temp = getSession().query(GpUrlBase).get(id)
            return temp
        except:
            return None

    @staticmethod
    def delete(appUrl: str):
        try:
            getSession().query(GpUrlBase).where(GpUrlBase.url == appUrl).delete()
            getSession().commit()
            return True
        except Exception as e:
            return None
