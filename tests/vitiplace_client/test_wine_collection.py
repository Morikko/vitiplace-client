from unittest import mock

from vitiplace_client import wine_collection


class TestWineCollection:
    @mock.patch("vitiplace_client.website_view.VitiplaceView")
    def test_from_vitiplace(
        self,
        MockVitiplaceView,
        board_page,
        custom_wine_page,
        visual_page,
        wine_information_api,
    ):
        first_url = "https://vin.vitiplace.com/vire-clesse/domaine-des-gandines-terroir-de-clesse-247690.php"  # noqa: E501
        second_url = "https://vin.vitiplace.com/vire-clesse/domaine-des-gandines-terroir-de-clesse-224039.php"  # noqa: E501
        instance = MockVitiplaceView.return_value
        instance.get_board_page.return_value = board_page
        instance.get_history_page.return_value = board_page

        def get_wine_page(url):
            if url == second_url:
                return custom_wine_page.replace(
                    first_url,
                    second_url,
                )
            else:
                return custom_wine_page

        instance.get_page.side_effect = get_wine_page
        instance.get_visual_page.return_value = visual_page
        instance.get_wine_information.return_value = wine_information_api

        actual_wine_collection = wine_collection.WineCollection.from_vitiplace()

        assert actual_wine_collection.wines == [
            {
                "id": 224039,
                "url": "https://vin.vitiplace.com/vire-clesse/domaine-des-gandines-terroir-de-clesse-224039.php",  # noqa: E501
                "name": "Pietramore - Cerasuolo d’Abruzzo",
                "region": "Abruzzes",
                "appellation": "Controguerra",
                "type": "Rosé",
                "millesimes": {},
                "purchase_history": [
                    {
                        "comment": None,
                        "date": "12/10/2020",
                        "millesime": 2018,
                        "quantity": 6,
                        "unitary_price": 0.0,
                        "volume": 0.75,
                    }
                ],
            },
            {
                "id": 247690,
                "url": "https://vin.vitiplace.com/vire-clesse/domaine-des-gandines-terroir-de-clesse-247690.php",  # noqa: E501
                "name": "Pietramore - Cerasuolo d’Abruzzo",
                "region": "Abruzzes",
                "appellation": "Controguerra",
                "type": "Rosé",
                "millesimes": {
                    "2018": {
                        "millesime": 2018,
                        "ready_year": 2020,
                        "best_year": None,
                        "limit_year": 2022,
                        "locations": {"Carton 1": 5, "unknown": 3},
                        "quantity": 8,
                    }
                },
                "purchase_history": [
                    {
                        "comment": None,
                        "date": "12/10/2020",
                        "millesime": 2018,
                        "quantity": 6,
                        "unitary_price": 0.0,
                        "volume": 0.75,
                    }
                ],
            },
        ]
