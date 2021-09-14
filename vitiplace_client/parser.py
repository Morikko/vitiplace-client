import bs4
from typing import NamedTuple, Optional

from vitiplace_client.model import (
    Wine,
    WineMillesime,
    WineInfoApi,
    API_NO_YEAR_PLACEHOLDER,
)

# An id given by Vitiplace for a wine specific per year
WineReferenceId = str

UNKNOWN = "unknown"


def extract_urls_from_list_page(text_page: str) -> list[str]:
    WINE_LINK_CSS_REF = "#table_stock .wine_name a"

    page = bs4.BeautifulSoup(text_page, "html.parser")
    wine_tags = page.select(WINE_LINK_CSS_REF)
    return [wine.attrs["href"] for wine in wine_tags]


def get_id_from_url(url: str) -> int:
    return int(url[url.rindex("-") + 1 : url.rindex(".php")])


def get_wine_with_purchase_history_from_wine_page(text_page: str) -> Wine:
    page = bs4.BeautifulSoup(text_page, "html.parser")

    url = page.select_one('link[rel="canonical"]').attrs["href"]
    id = get_id_from_url(url)

    # TODO:
    purchase_history = []

    return Wine(
        id=id,
        url=url,
        name=page.select_one("#nomvin").text,
        region=page.select_one("#region").text,
        appellation=page.select_one("#app").text,
        type=page.select_one("#robe").text,
        millesimes={},
        purchase_history=purchase_history,
    )


class WineIdLocation(NamedTuple):
    wine_id: str
    location: str


def extract_wine_locations_from_visual_page(visual_page: str) -> list[WineIdLocation]:
    BOX_CSS_REF = "div.bottle-box"
    WINE_IN_BOX_CSS_REF = "td div div"
    UNKNOWN_LOCATION_CSS_REF = "div#unPlacedList ul#list_wine li"

    page = bs4.BeautifulSoup(visual_page, "html.parser")

    location_boxes = page.select(BOX_CSS_REF)

    wine_location_list: list[WineIdLocation] = [
        WineIdLocation(wine_id=wine.attrs["id"], location=box.h4.text)
        for box in location_boxes
        for wine in box.select(WINE_IN_BOX_CSS_REF)
    ]

    unknown_located_wines = page.select(UNKNOWN_LOCATION_CSS_REF)
    for wine in unknown_located_wines:
        quantity = int(wine.select(".qty.qty-look")[0].text)
        for i in range(quantity):
            wine_location_list.append(
                WineIdLocation(wine_id=wine.attrs["id"], location=UNKNOWN)
            )

    return wine_location_list


def get_wine_ref(
    wine_information: WineInfoApi,
) -> tuple[str, int]:
    """
    Return the url and millesime
    """
    details = wine_information["vin"]

    return (
        details["url"],
        details["mil"],
    )


def get_year_from_string(year: str) -> Optional[int]:
    return int(year) if year != API_NO_YEAR_PLACEHOLDER else None


def get_wine_millesime(wine_information: WineInfoApi) -> WineMillesime:
    details = wine_information["vin"]

    millesime = get_year_from_string(details["mil"])
    if not millesime:
        raise ValueError("Should not be None")

    return WineMillesime(
        millesime=millesime,
        ready_year=get_year_from_string(details["from"]),
        best_year=get_year_from_string(details["apg"]),
        limit_year=get_year_from_string(details["limit"]),
        locations={},
        quantity=0,
    )
