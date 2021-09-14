import json
from vitiplace_client import parser, website_view, model


class WineCollection:
    def __init__(self, wines: list[model.Wine] = None):
        self.wines = wines

    def backup(self, path: str):
        with open(path) as fp:
            json.dump(self.wines, fp)

    @classmethod
    def from_vitiplace(cls, email: str = None, password: str = None):
        vitiplace_view = website_view.VitiplaceView(email=email, password=password)

        board_urls = parser.extract_urls_from_list_page(vitiplace_view.get_board_page())
        history_urls = parser.extract_urls_from_list_page(
            vitiplace_view.get_history_page()
        )
        wine_urls = set(board_urls) | set(history_urls)
        print(wine_urls)

        # Get wine identity and the purchase history
        # Do not get millesimes as it is done by JS
        wines_by_url = {}
        for wine_url in wine_urls:
            if wine_url in wines_by_url:
                continue
            wine = parser.get_wine_with_purchase_history_from_wine_page(
                vitiplace_view.get_page(wine_url)
            )

            wines_by_url[wine_url] = wine

        # Get millesimes with stock
        cache_wine_details: dict[int, model.WineInfoApi] = {}
        wine_locations = parser.extract_wine_locations_from_visual_page(
            vitiplace_view.get_visual_page()
        )
        for w in wine_locations:
            wine_details = (
                vitiplace_view.get_wine_information(w.wine_id)
                if w.wine_id not in cache_wine_details
                else cache_wine_details[w.wine_id]
            )

            (url, mil) = parser.get_wine_ref(wine_details)

            wine = wines_by_url[url]

            if mil not in wine["millesimes"]:
                wine_millesime = parser.get_wine_millesime(wine_details)
                wine_millesime["quantity"] = 1
                wine_millesime["locations"][w.location] = 1
                wine["millesimes"][mil] = wine_millesime
            else:
                wine_millesime = wine["millesimes"][mil]
                wine_millesime["quantity"] += 1
                if w.location in wine_millesime["locations"]:
                    wine_millesime["locations"][w.location] += 1
                else:
                    wine_millesime["locations"][w.location] = 1

        return cls(wines=sorted(list(wines_by_url.values()), key=lambda d: d["id"]))
