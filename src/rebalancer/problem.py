from enum import Enum
from math import ceil, floor

from pydantic import BaseModel

from .portfolio import Portfolio


class Instrument(BaseModel):
    price: float
    units: float
    lower: int
    upper: int


class AssetClass(BaseModel):
    target_total: float
    remainder: float
    instruments: list[Instrument]

    def get_ratio(self, denominator: float) -> float:
        return (sum(map(lambda x: x.price * x.units, self.instruments)) /
                denominator)


class Status(Enum):
    unfeasible = 'unfeasible'
    candidate = 'candidate'
    optimal = 'optimal'
    unknwon = 'unknown'


class Problem(BaseModel):
    status: Status
    total: float
    remainder: float
    objective_value: float
    portfolio: list[AssetClass]

    @staticmethod
    def from_portfolio(portfolio: Portfolio) -> 'Problem':
        total = portfolio.total
        assets: list[AssetClass] = []
        for asset in portfolio.portfolio:
            instruments: list[Instrument] = []
            for instrument in asset.instruments:
                upper = floor(total / instrument.price)
                if instrument.unincreasable:
                    upper = instrument.units
                instruments.append(Instrument(price=instrument.price, units=-1,
                                              upper=upper, lower=0))
            asset_total = total * asset.target
            assets.append(AssetClass(target_total=asset_total,
                                     remainder=asset_total,
                                     instruments=instruments))
        return Problem(status=Status.unknwon,
                       total=total, remainder=total,
                       objective_value=float('inf'),
                       portfolio=assets)

    def get_objective_value(self) -> float:
        objective_value = 0
        for asset in self.portfolio:
            asset_total = 0
            for instrument in asset.instruments:
                asset_total += instrument.price * instrument.units
            objective_value += (asset.target_total - asset_total) ** 2
        return objective_value

    def fit(self) -> Status:
        assert self.status is Status.unknwon

        self.remainder = self.total
        for asset in self.portfolio:
            asset.remainder = asset.target_total
            for instrument in filter(lambda x: x.units >= 0,
                                     asset.instruments):
                assert instrument.lower <= instrument.units <= instrument.upper
                self.remainder -= instrument.price * instrument.units
                asset.remainder -= instrument.price * instrument.units
            if self.remainder < 0:
                self.status = Status.unfeasible
                return self.status

        for asset in self.portfolio:
            for instrument in filter(lambda x: x.units < 0, asset.instruments):
                if asset.remainder > 0 and self.remainder > 0:
                    instrument.units = (min(asset.remainder, self.remainder) /
                                        instrument.price)
                else:
                    instrument.units = 0
                instrument.units = min(instrument.units, instrument.upper)
                instrument.units = max(instrument.units, instrument.lower)
                self.remainder -= instrument.price * instrument.units
                asset.remainder -= instrument.price * instrument.units
            if self.remainder < 0:
                self.status = Status.unfeasible
                return self.status

        is_all_integer = True
        for asset in self.portfolio:
            for instrument in asset.instruments:
                is_all_integer = is_all_integer and float(instrument.units).is_integer()
                if not is_all_integer:
                    break
        if is_all_integer:
            self.status = Status.candidate
        else:
            self.status = Status.optimal
        self.objective_value = self.get_objective_value()
        return self.status

    def flatten_instruments(self) -> list[Instrument]:
        instruments: list[Instrument] = []
        for asset in self.portfolio:
            instruments += asset.instruments
        return instruments

    def branch(self) -> tuple['Problem', 'Problem']:
        instruments = self.flatten_instruments()
        found = False
        index = -1
        for i, instrument in enumerate(instruments):
            if not found and not float(instrument.units).is_integer():
                found = True
                index = i
            else:
                instrument.units = -1
        upper = floor(instruments[index].units)
        lower = ceil(instruments[index].units)
        assert lower >= 0, f'{index}, {upper}, {lower}, {instruments[index]}'
        self.status = Status.unknwon
        left = self.model_copy(deep=True)
        right = self.model_copy(deep=True)

        instruments = left.flatten_instruments()
        instruments[index].upper = upper
        instruments[index].units = upper

        instruments = right.flatten_instruments()
        instruments[index].lower = lower
        instruments[index].units = lower
        return left, right
