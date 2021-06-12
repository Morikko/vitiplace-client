import requests
import datetime
import os

from typing import TypedDict, Optional

VITIPLACE_CLIENT_EMAIL_VAR_NAME = "VITIPLACE_CLIENT_EMAIL"
VITIPLACE_CLIENT_PASSWORD_VAR_NAME = "VITIPLACE_CLIENT_PASSWORD"

BASE_URL = "https://www.vitiplace.com"
BASE_ACCOUNT_URL = "https://abonne.vitiplace.com"
BASE_WINE_URL = "https://vin.vitiplace.com"

BOARD_URL = f"{BASE_ACCOUNT_URL}/tableau_de_bord.php"
VISUAL_URL = f"{BASE_ACCOUNT_URL}/visual-gest.php"
LOGIN_URL = f"{BASE_URL}/progs/identification.php"
WINE_INFO_URL = f"{BASE_URL}/progs/cellar-center.php"

API_NO_YEAR_PLACEHOLDER = "-"


# "from" is a restricted python keyword
WineInfoApiRestricted = TypedDict("WineInfoApiRestricted", {"from": int})


class WineInfoApi(TypedDict, WineInfoApiRestricted):
    idv: int
    nom: str
    url: str
    app: str
    idtype: str
    libtype: str
    tag: str
    mil: int
    apg: str
    limit: str


class WineInfoResponseApi(TypedDict):
    vin: WineInfoApi


class VitiplaceView:
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        self.session = requests.Session()
        self.email = (
            email if email is not None else os.environ[VITIPLACE_CLIENT_EMAIL_VAR_NAME]
        )
        self.password = (
            password
            if password is not None
            else os.environ[VITIPLACE_CLIENT_PASSWORD_VAR_NAME]
        )
        self.is_login = False

    def ensure_login(self):
        if not self.is_login:
            self.login()

    def login(self):
        resp = self.session.post(
            LOGIN_URL,
            data={
                "mail": self.email,
                "mdp": self.password,
                "altmdp": "",
            },
        )

        resp.raise_for_status()
        self.is_login = True

    def get_board_page(self, with_history: bool = False) -> str:
        self.ensure_login()
        resp = self.session.get(
            BOARD_URL + ("?h=1" if with_history else ""),
        )
        resp.raise_for_status()
        return resp.text

    def get_visual_page(self) -> str:
        self.ensure_login()
        resp = self.session.get(VISUAL_URL)
        resp.raise_for_status()
        return resp.text

    def get_wine_information(self, id: int) -> WineInfoResponseApi:
        """
        Example:
            {
                "vin": {
                    "idv": "247696",
                    "nom": "Pietramore - Cerasuolo dAbruzzo",
                    "url": "https://vin.vitiplace.com/controguerra/pietramore-cerasuolo-d-abruzzo-247696.php",
                    "app": "Controguerra",
                    "idtype": "3",
                    "libtype": "Rosé",
                    "type": "3",
                    "tag": "/images/etiquettes/thumbs/default_mini_sticker.png",
                    "mil": "2018",
                    "from": "2020",
                    "apg": "-",
                    "limit": "2022",
                }
            }
        """
        self.ensure_login()
        resp = self.session.post(
            WINE_INFO_URL,
            data={
                "act": "getIwine",
                "ids": id,
            },
        )

        resp.raise_for_status()
        return resp.json()

    def get_page(self, url: str) -> str:
        self.ensure_login()

        resp = self.session.get(url)

        resp.raise_for_status()
        return resp.text
