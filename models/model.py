from sqlalchemy import create_engine, Column, Integer, String, BigInteger, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///databases/g_scraper.db")

Base = declarative_base()
session = sessionmaker(bind=engine)
session = session()


class GpUrlBase(Base):
    __tablename__ = "gp_url_base"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String)
    register_date = Column(BigInteger)
    last_view_date = Column(BigInteger)
    last_scan_date = Column(BigInteger)


class GpScreenShoot(Base):
    __tablename__ = "gp_screen_shoot"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_app = Column(Integer, ForeignKey("gp_url_base.id"))
    local_url = Column(String)
    position = Column(Integer)
    date_added = Column(BigInteger)
    date_evaluated = Column(BigInteger)


class GpScreenEvaluated(Base):
    __tablename__ = "gp_screen_evaluated"
    id = Column(Integer, primary_key=True, autoincrement=True)

    screen_id = Column(Integer, ForeignKey("gp_screen_shoot.id"))

    # Tiene texto en la screen shoot
    have_text = Column(Boolean, default=False)
    # Hay una imagen real de lo que vamos a ver dentro de la app
    have_app_screen_shoot = Column(Boolean, default=False)
    # Tiene un fondo independiente de las imagenes y el texto
    have_bg = Column(Boolean, default=False)
    # El diseño es bueno/bonito
    have_good_art = Column(Boolean, default=False)
    # La imagen tiene 3 niveles de profundidad o más (text, app screenshoot o game play, fondo)
    have_deep = Column(Boolean, default=False)
    # El texto inicia con un verbo de acción.
    text_start_with_action_verb = Column(Boolean, default=False)
    # La screen tiene texto excesivo
    excesive_text = Column(Boolean, default=False)
    # Sobrecargada de cosas
    content_overload = Column(Boolean, default=False)
    # Es un juego
    is_a_game = Column(Boolean, default=False)
    # Indicamos si es una app pensada para niños mediante sus gráficos
    is_for_kids = Column(Boolean, default=False)

    date_registered = Column(BigInteger)


class GpLogoApp(Base):
    __tablename__ = "gp_logo_app"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_app = Column(Integer, ForeignKey("gp_url_base.id"))
    local_url = Column(String)
    date_added = Column(BigInteger)
    date_evaluated = Column(BigInteger)


def init():
    Base.metadata.create_all(engine)


def getSession():
    return session
