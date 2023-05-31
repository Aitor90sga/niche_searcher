from datetime import datetime, timedelta

class AppConfig:
    downloadRequired = 99999
    dataToEvaluate = int((datetime.now() - timedelta(days=365)).timestamp() * 1000)
