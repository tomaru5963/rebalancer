from datetime import datetime
from importlib import resources
import json

import jsonschema

from .portfolio import Portfolio
from .problem import Problem


def validate_portfolio(portfolio: Portfolio):
    with (resources.files('rebalancer') / 'schema.json').open() as f:
        schema = json.load(f)

    def is_aware_datetime(checker, instance):
        return (isinstance(instance, datetime) and
                instance.tzinfo is not None and
                instance.tzinfo.utcoffset(instance) is not None)

    validator = jsonschema.validators.validator_for(schema)
    type_checker = validator.TYPE_CHECKER.redefine('datetime-aware',
                                                   is_aware_datetime)
    validator = jsonschema.validators.extend(validator,
                                             type_checker=type_checker)
    validator(schema).validate(portfolio, schema)


def report(portfolio: Portfolio, solution: Problem) -> str:
    ledger = [
        f'Time: {portfolio.time}',
        f'Total target ratio: {portfolio.total_target:.2%}',
        f'Remainder: US$ {solution.remainder:.2f}',
    ]

    for cur_asset, new_asset in zip(portfolio.portfolio, solution.portfolio):
        target_delta = cur_asset.get_ratio(portfolio.total) - cur_asset.target
        solution_target_delta = (new_asset.get_ratio(solution.total) -
                                 cur_asset.target)
        ledger.append(
            f'Asset class: {cur_asset.asset_class} ({cur_asset.target:.2%}, '
            f'{target_delta:.2%} -> {solution_target_delta:.2%})'
        )
        for cur_instrument, new_instrument in zip(cur_asset.instruments,
                                                  new_asset.instruments):
            ledger.append(
                '  '
                f'Instrument: {cur_instrument.instrument}, '
                f'Price: US$ {cur_instrument.price}, '
                f'Units: {cur_instrument.units} -> {int(new_instrument.units)}'
            )
    return '\n'.join(ledger)
