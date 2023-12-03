from engines.discover_engine.discover_engine import DiscoverEngine
from engines.evaluate_engine.evaluate_engine import EvaluateEngine
from engines.sync_engine.sync_engine import SyncEngine

import threading

if __name__ == '__main__':

    def startDiscoverEngine():
        DiscoverEngine("es_ES")


    def startEvaluateEngine():
        EvaluateEngine()


    def startSyncEngine():
        SyncEngine()
        pass


    while True:
        print("1) Actualizar URLS")
        print("2) Evaluar nichos")
        print("3) Sync with server")

        result = input("Ingrese una opción:")

        if result == "2":
            threading.Thread(target=startEvaluateEngine()).start()

        elif result == "1":
            threading.Thread(target=startDiscoverEngine).start()

        elif result == "3":
            threading.Thread(target=startSyncEngine).start()
