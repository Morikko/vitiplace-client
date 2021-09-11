import bs4
from typing import NamedTuple

from vitiplace_client.model import Wine

# An id given by Vitiplace for a wine specific per year
WineReferenceId = str

UNKNOWN = "unknown"


def extract_wine_list_from_board_page(text_page: str) -> list[tuple[str, str]]:
    WINE_LINK_CSS_REF = "#table_stock .wine_name a"

    page = bs4.BeautifulSoup(text_page, "html.parser")
    wine_tags = page.select(WINE_LINK_CSS_REF)
    return [(wine.text, wine.attrs["href"]) for wine in wine_tags]


def get_wine_information_from_page(page_url: str) -> Wine:
    # TODO
    ...


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


def get_wine_id_from_box_id(id: int) -> str:
    # TODO:
    ...
