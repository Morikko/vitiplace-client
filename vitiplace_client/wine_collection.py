import json
from vitiplace_client import parser, website_view, model


class WineCollection:
    def __init__(self, wines: list[model.Wine] = None):
        self.wines = wines

    def backup(self, path: str):
        with open(path, "w") as fp:
            json.dump(self.wines, fp)

    @classmethod
    def from_file(cls, path: str) -> "WineCollection":
        """
        No check is done on the loaded data.

        Please verify the data comes from `cls.backup()` or respects
        the data models in `vitiplace_client.model`.
        """
        with open(path) as fp:
            return cls(wines=json.load(fp))

    @classmethod
    def from_vitiplace(
        cls,
        email: str = None,
        password: str = None,
    ) -> "WineCollection":
        vitiplace_wine_collection = VitiplaceWineCollection(
            email=email, password=password
        )
        return vitiplace_wine_collection.fetch_wine_collection()


class VitiplaceWineCollection:
    """
    An helper class to create a wine collection from an account
    on `vitiplace.com`.

    The pages fetched on the website are cached and could be reused
    on repeated execution.
    """

    def __init__(
        self,
        # Set Credentials or use env vars
        email: str = None,
        password: str = None,
        # Avoid to recompute some steps
        wines_by_url=None,
        cache_wine_details: dict[int, model.WineInfoApi] = None,
    ):
        self.vitiplace_view = website_view.VitiplaceView(email=email, password=password)
        self.wines_by_url = wines_by_url if wines_by_url else {}
        self.cache_wine_details = cache_wine_details if cache_wine_details else {}

    def fetch_wines_by_url(self) -> None:
        board_urls = parser.extract_urls_from_list_page(
            self.vitiplace_view.get_board_page()
        )
        history_urls = parser.extract_urls_from_list_page(
            self.vitiplace_view.get_history_page()
        )
        wine_urls = set(board_urls) | set(history_urls)

        # Get wine identity and the purchase history
        # Do not get millesimes as it is done by JS
        for wine_url in wine_urls:
            if wine_url in self.wines_by_url:
                continue
            print(wine_url)
            wine = parser.get_wine_with_purchase_history_from_wine_page(
                self.vitiplace_view.get_page(wine_url)
            )

            self.wines_by_url[wine_url] = wine

    def fetch_wine_locations(self):
        # Get millesimes with stock
        wine_locations = parser.extract_wine_locations_from_visual_page(
            self.vitiplace_view.get_visual_page()
        )
        for w in wine_locations:
            print(w)
            wine_details = (
                self.vitiplace_view.get_wine_information(w.wine_id)
                if w.wine_id not in self.cache_wine_details
                else self.cache_wine_details[w.wine_id]
            )

            self.cache_wine_details[w.wine_id] = wine_details

            (url, mil) = parser.get_wine_ref(wine_details)

            wine = self.wines_by_url[url]

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

    def get_wine_collection(self) -> WineCollection:
        return WineCollection(
            wines=sorted(list(self.wines_by_url.values()), key=lambda d: d["id"])
        )

    def fetch_wine_collection(self):
        self.fetch_wines_by_url()
        self.fetch_wine_locations()
        return self.get_wine_collection()
