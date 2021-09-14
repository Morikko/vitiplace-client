from vitiplace_client import parser, model


class TestParser:
    def test_extract_urls_from_list_page(self, board_page: str):
        actual_wine_list = parser.extract_urls_from_list_page(board_page)

        assert len(actual_wine_list) == 2

        expected_wine_list = [
            "https://vin.vitiplace.com/vire-clesse/domaine-des-gandines-terroir-de-clesse-247690.php",
            "https://vin.vitiplace.com/vire-clesse/domaine-des-gandines-terroir-de-clesse-224039.php",
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

    def test_get_wine_with_purchase_history_from_wine_page(self, wine_page):
        actual_wine = parser.get_wine_with_purchase_history_from_wine_page(wine_page)
        expected_wine = model.Wine(
            id=247690,
            url="https://vin.vitiplace.com/vire-clesse/domaine-des-gandines-terroir-de-clesse-247690.php",
            name="Pietramore - Cerasuolo d’Abruzzo",
            region="Abruzzes",
            appellation="Controguerra",
            type="Rosé",
            millesimes={},
            purchase_history=[],
        )

        assert actual_wine == expected_wine

    def test_get_id_from_url(self):
        actual_id = parser.get_id_from_url(
            "https://vin.vitiplace.com/vire-clesse/domaine-des-gandines-terroir-de-clesse-224039.php"
        )

        assert actual_id == 224039

    def test_get_year_from_string(self):
        assert 2020 == parser.get_year_from_string("2020")
        assert None == parser.get_year_from_string(model.API_NO_YEAR_PLACEHOLDER)

    def test_get_wine_ref(self, wine_information_api):
        assert parser.get_wine_ref(wine_information_api) == (
            "https://vin.vitiplace.com/controguerra/pietramore-cerasuolo-d-abruzzo-247696.php",
            "2018",
        )

    def test_get_wine_millesime(self, wine_information_api):
        actual_wine_millesime = parser.get_wine_millesime(wine_information_api)

        expected_wine_millesime = model.WineMillesime(
            millesime=2018,
            ready_year=2020,
            best_year=None,
            limit_year=2022,
            locations={},
            quantity=0,
        )

        assert actual_wine_millesime == expected_wine_millesime
