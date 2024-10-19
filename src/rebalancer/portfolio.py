from datetime import datetime

from pydantic import BaseModel


class Instrument(BaseModel):
    instrument: str
    price: float
    units: int
    unincreasable: bool = False


class AssetClass(BaseModel):
    asset_class: str
    target: float
    instruments: list[Instrument]

    @property
    def total(self) -> float:
        return sum(map(lambda x: x.price * x.units, self.instruments))

    def get_ratio(self, denominator: float) -> float:
        return (sum(map(lambda x: x.price * x.units, self.instruments)) /
                denominator)


class Portfolio(BaseModel):
    time: datetime
    portfolio: list[AssetClass]

    @property
    def total(self) -> float:
        return sum(map(lambda x: x.total, self.portfolio))

    @property
    def total_target(self) -> float:
        return sum(map(lambda x: x.target, self.portfolio))
