# gaussbinomdistributions

gaussbinomdistributions is a Python library for calculating **gaussian** and **binomial** distributions.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install distributions.

```bash
pip install gaussbinomdistributions
```

## Usage

```python
from gaussbinomdistributions import Gaussian

g1 = Gaussian(mean=10, stdev=0.2)
g2 = Gaussian(mean=6, stdev=0.4)

g3 = g1 + g2

print(f"mean {g3.mean}, standard deviation {g3.stdev}")

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
