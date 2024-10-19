Portfolio rebalancer - rebalance your portfolio
===============================================

This rebalances your portfolio by Integer Programming (IP) using Branch and
Bound (BB). But to be honest, I am not sure if I have implemented it correctly.

## Build and Installation

To build and install:

```sh
poetry build
cd the_environment_where_you_install_this
pip install the_place_of_dist/rebalancer-x.y.z-py3-none-any.whl
```

## Samples

sample.yaml:

```yaml:sample.yaml
time: 2023-09-30T10:20:30+09:00
portfolio:
  - asset_class: us_market_stocks
    target: 0.50
    instruments:
      - instrument: vti
        price: 283.20
        units: 33
  - asset_class: depeloped_markets_stocks
    target: 0.35
    instruments:
      - instrument: vea
        price: 52.98
        units: 102
  - asset_class: emerging_markets_stocks
    target: 0.15
    instruments:
      - instrument: vwo
        price: 48.25
        units: 49
```

`rebalancer sample.yaml` will show:

```
Time: 2023-09-30 10:20:30+09:00
Total target ratio: 100.00%
Remainder: US$ 73.82
Asset class: us_market_stocks (50.00%, 4.61% -> -0.36%)
  Instrument: vti, Price: US$ 283.2, Units: 33 -> 30
Asset class: depeloped_markets_stocks (35.00%, -3.42% -> -0.02%)
  Instrument: vea, Price: US$ 52.98, Units: 102 -> 113
Asset class: emerging_markets_stocks (15.00%, -1.19% -> -0.06%)
  Instrument: vwo, Price: US$ 48.25, Units: 49 -> 53a
```

Here 30 units for vti, 113 units for vea and 53 units for vwo are better for
good fitting to the target ratio of each asset class. 
