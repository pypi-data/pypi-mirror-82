# ConchPattern

A Python simulator of control chart patterns

Checkout the documentation here

## Usage

Here we are demonstrating a process that experiences a large shift in the quality measurement halfway into the process:

```python
from conch_pattern import ControlledProcess, ShiftProcess
import numpy
import matplotlib.pyplot as plt

# We sample `n` points from this process using `generate(n)`, which is returned as a numpy array
sample = numpy.append(
    ControlledProcess().generate(50),
    ShiftProcess(magnitude=3).generate(50)
)

# We often want to plot the results
plt.plot(sample)
plt.show()
```

This will print something like:

![](readme.png)
