# rx_algorithm

A fast (experimental) RX algorithm implementation in Python 3.9+ with overhead reduction based on entropy estimation via compression.

## Example usage

```python
from rx_algorithm import rx
from rx.utils import plot

X = rx(array)
plot(X, 'out.png')
```