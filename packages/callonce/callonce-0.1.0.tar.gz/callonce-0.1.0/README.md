# callonce

## Usage

```python
from callonce import callonce


@callonce
def _return_true() -> bool:
    return True


def _call_return_true():
    return _return_true()


def _call_return_true_3times():
    return _return_true(times=3)


def test_call_once():
    assert _call_return_true() == True
    assert _call_return_true() == None


def test_call_3times():
    assert _call_return_true_3times() == True
    assert _call_return_true_3times() == True
    assert _call_return_true_3times() == True
    assert _call_return_true_3times() == None
```

We offer a `printonce` function for easy debug in deep learning model, e.g., PyTorch. You don't have to remove the `printonce` when training the model in loop because the shape will be printed only once.

```python
from callonce import printonce
from torch import nn

class Net(nn.Module):

    def __init__(self):
        self.linear = nn.Linear(4, 8)

    def forward(self, x):
        printonce('x:', x.shape)
        y = self.linear(x)
        printonce('y:', y.shape)
        return y
```
