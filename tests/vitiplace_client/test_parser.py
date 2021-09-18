from vitiplace_client import parser, model


class TestParser:
    def test_extract_urls_from_list_page(self, board_page: str):
        actual_wine_list = parser.extract_urls_from_list_page(board_page)

        assert len(actual_wine_list) == 2

        expected_wine_list = [
            "https://vin.vitiplace.com/vire-clesse/domaine-des-gandines-terroir-de-clesse-247690.php",  # noqa: E501
            "https://vin.vitiplace.com/vire-clesse/domaine-des-gandines-terroir-de-clesse-224039.php",  # noqa: E501
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

    def test_get_wine_with_purchase_history_from_wine_page(
        self, custom_wine_page, official_wine_page
    ):
        actual_wine = parser.get_wine_with_purchase_history_from_wine_page(
            custom_wine_page
        )
        expected_wine = model.Wine(
            id=247690,
            url="https://vin.vitiplace.com/vire-clesse/domaine-des-gandines-terroir-de-clesse-247690.php",  # noqa: E501
            name="Pietramore - Cerasuolo d’Abruzzo",
            region="Abruzzes",
            appellation="Controguerra",
            type="Rosé",
            millesimes={},
            purchase_history=[
                {
                    "comment": None,
                    "date": "12/10/2020",
                    "millesime": 2018,
                    "quantity": 6,
                    "unitary_price": 0.0,
                    "volume": 0.75,
                }
            ],
        )

        assert actual_wine == expected_wine

        actual_wine = parser.get_wine_with_purchase_history_from_wine_page(
            official_wine_page
        )
        expected_wine = model.Wine(
            id=4923,
            url="https://vin.vitiplace.com/cotes-de-bourg/bois-de-tau-4923.php",
            name="Château du Bois de Tau",
            region="Bordelais, France",
            appellation="Côtes de Bourg",
            type="Rouge",
            millesimes={},
            purchase_history=[
                {
                    "comment": None,
                    "date": "01/04/2018",
                    "millesime": 1993,
                    "quantity": 0,
                    "unitary_price": 0.0,
                    "volume": 0.75,
                }
            ],
        )

        assert actual_wine == expected_wine

    def test_get_id_from_url(self):
        actual_id = parser.get_id_from_url(
            "https://vin.vitiplace.com/vire-clesse/domaine-des-gandines-terroir-de-clesse-224039.php"  # noqa: E501
        )

        assert actual_id == 224039

    def test_get_year_from_string(self):
        assert parser.get_year_from_string("2020") == 2020
        assert parser.get_year_from_string(model.API_NO_YEAR_PLACEHOLDER) is None

    def test_get_wine_ref(self, wine_information_api):
        assert parser.get_wine_ref(wine_information_api) == (
            "https://vin.vitiplace.com/vire-clesse/domaine-des-gandines-terroir-de-clesse-247690.php",  # noqa: E501
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
