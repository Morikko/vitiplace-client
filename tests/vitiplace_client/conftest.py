import json
from pathlib import Path
import pytest

FIXTURES_PATH = Path(__file__).parent / "__fixtures__"


def load_html_page(page_name: str) -> str:
    with open(FIXTURES_PATH / page_name) as fp:
        return fp.read()


def load_json(page_name: str) -> str:
    with open(FIXTURES_PATH / page_name) as fp:
        return json.load(fp)


@pytest.fixture
def board_page() -> str:
    return load_html_page("board_page.html")


@pytest.fixture
def visual_page() -> str:
    return load_html_page("visual_page.html")


@pytest.fixture
def wine_page() -> str:
    return load_html_page("wine_page.html")


@pytest.fixture
def wine_information_api() -> str:
    return load_json("wine_information.json")
