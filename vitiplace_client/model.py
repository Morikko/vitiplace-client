from typing import TypedDict, Optional


class Wine(TypedDict):
    name: str
    country: str
    region: str
    appellation: str
    type: str
    millesime: Optional[int]
    quantity: int
    volume: int
    cost_date: Optional[str]  # as date
    price: Optional[float]  # unitary
    ready_year: Optional[int]
    best_year: Optional[int]
    final_year: Optional[int]
    comment: str
    location: list[str]
