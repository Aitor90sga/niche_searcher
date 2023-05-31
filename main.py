from engines.discover_engine.discover_engine import DiscoverEngine
from engines.evaluate_engine.evaluate_engine import EvaluateEngine
import threading

if __name__ == '__main__':

    def startDiscoverEngine():
        """
        Esta es la funcionalidad base que nos permite descubrir nuevas aplicaciones que se hayan subido a Google play.
        :return:
        """
        DiscoverEngine("es_ES")


    def startEvaluateEngine():
        EvaluateEngine()


    while True:
        print("1) Actualizar URLS")
        print("2) Evaluar nichos")
        result = input("Ingrese una opción:")

        if result == "2":
            threading.Thread(target=startEvaluateEngine()).start()

        else:
            threading.Thread(target=startDiscoverEngine).start()
