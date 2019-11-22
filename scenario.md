# Proposal
```python3
from pyJoules import *

# Usage 1 (basic)
with EnergyContext:
	foo()
	bar()

# Usage 2 (basic)
@measureit
def foo():
	pass

# Usage 3 (configurable)
with EnergyContext(ConsolePrinter, tag="bar", NvidiaDevice.GPU(1), RaplDevice.ALL) as ctx:
	foo()
	ctx.record(tag="foo")
	bar()

# Usage 4 (configurable)
@measureit(ConsolePrinter, NvidiaDevice.GPU(1), RaplDevice.ALL)
def foo():
	pass

# Usage 5 (advanced)
meter = EnergyMeter(CudaDevice.GPU, RaplDevice.CORE)
meter.start()
foo()
meter.record(tag="foo")
bar()
meter.stop(tag="bar")
samples = meter.compute()
ConsolePrinter.process(samples)

sample = samples.get_sample("bar")
print sample.energy(CudaDevice.GPU)
```
