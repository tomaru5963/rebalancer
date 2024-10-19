import argparse
from pathlib import Path

import yaml

from .portfolio import Portfolio
from .solver import Solver
from .utils import report, validate_portfolio


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('portfolio')
    parser.add_argument('--list', action='store_true',
                        help='list the portfoliios')
    parser.add_argument('--index', default=0, type=int,
                        help='specify portfolio index to rebalance')
    args = parser.parse_args()

    with Path(args.portfolio).open() as f:
        portfolios = list(yaml.safe_load_all(f))
    for portfolio in portfolios:
        validate_portfolio(portfolio)

    portfolios.sort(key=lambda x: x['time'], reverse=True)
    assert len(portfolios) > 0

    if args.list:
        for index, portfolio in enumerate(portfolios):
            print(f'{index}: {portfolio["time"]}')
        exit()

    portfolio = Portfolio.model_validate(portfolios[args.index])
    solver = Solver(portfolio)
    solution = solver.solve()
    if solution is None:
        print('No solution was found')
        exit()

    print(report(portfolio, solution))
