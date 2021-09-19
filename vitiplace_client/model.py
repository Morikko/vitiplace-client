from typing import Optional, Dict, List
from typing_extensions import TypedDict


class WineMillesime(TypedDict):
    """
    Information about a specific millesime
    """

    millesime: int
    quantity: int  # still full
    ready_year: Optional[int]
    best_year: Optional[int]
    limit_year: Optional[int]
    locations: Dict[str, int]


class WinePurchaseHistory(TypedDict):
    date: str
    millesime: int
    volume: float
    quantity: int
    unitary_price: float
    comment: Optional[str]


class Wine(TypedDict):
    id: int
    url: str
    name: str
    # country: str
    region: str
    appellation: str
    type: str

    millesimes: Dict[int, WineMillesime]
    purchase_history: List[WinePurchaseHistory]


API_NO_YEAR_PLACEHOLDER = "-"


# "from" is a restricted python keyword
WineInfoApiRestricted = TypedDict("WineInfoApiRestricted", {"from": str})


class WineDetailsApi(TypedDict, WineInfoApiRestricted):
    idv: int
    nom: str
    url: str
    app: str
    idtype: str
    libtype: str
    tag: str
    mil: str
    apg: str
    limit: str


class WineInfoApi(TypedDict):
    vin: WineDetailsApi
