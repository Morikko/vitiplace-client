import pytest
from pathlib import Path

from vitiplace_client import parser

FIXTURES_PATH = Path(__file__).parent / "__fixtures__"


def load_html_page(page_name: str) -> str:
    with open(FIXTURES_PATH / page_name) as fp:
        return fp.read()


class TestParser:
    @pytest.fixture
    def board_page(self) -> str:
        return load_html_page("board_page.html")

    @pytest.fixture
    def visual_page(self) -> str:
        return load_html_page("visual_page.html")

    def test_extract_wine_list_from_board_page(self, board_page: str):
        actual_wine_list = parser.extract_wine_list_from_board_page(board_page)

        assert len(actual_wine_list) == 2

        expected_wine_list = [
            (
                "Domaine des Gandines - Terroir de Clessé",
                "https://vin.vitiplace.com/vire-clesse/domaine-des-gandines-terroir-de-clesse-247690.php",
            ),
            (
                "Domaine des Gandines - Terroir de Clessé",
                "https://vin.vitiplace.com/vire-clesse/domaine-des-gandines-terroir-de-clesse-224039.php",
            ),
        ]
        assert expected_wine_list == actual_wine_list

    def test_extract_wine_locations_from_visual_page(self, visual_page: str):
        actual_wine_boxes = parser.extract_wine_locations_from_visual_page(visual_page)

        expected_wine_boxes = [
            parser.WineIdLocation(wine_id="300139", location="Carton 1"),
            parser.WineIdLocation(wine_id="395529", location="Carton 1"),
            parser.WineIdLocation(wine_id="188030", location="Carton 1"),
            parser.WineIdLocation(wine_id="395528", location="Carton 1"),
            parser.WineIdLocation(wine_id="168435", location="Carton 1"),
            parser.WineIdLocation(wine_id="442417", location=parser.UNKNOWN),
            parser.WineIdLocation(wine_id="442418", location=parser.UNKNOWN),
            parser.WineIdLocation(wine_id="442418", location=parser.UNKNOWN),
        ]

        assert actual_wine_boxes == expected_wine_boxes
