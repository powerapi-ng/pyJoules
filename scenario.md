
# Exemple 1
```python
from pyJoules import *

rapl = RaplDevice(RaplDevice.package(0), RaplDevice.package(1), RaplDevice.dram(1))
gpu = NvidiaDevice(NvidiaDevice.gpu(0)
file = FileRecorder('result.csv')

energy_trace = EnergyTrace(devices, default_tag='tag')

energy_trace.start(tag='start')
foo()
energy_trace.record(tag='middle')	
bar()
energy_trace.stop()

file.handle(energy_trace)

energy_trace2 = EnergyTrace(devices)
energy_trace2.start(tag='start2')
foo()
energy_trace2.record(tag='middle2')	
bar()
energy_trace2.stop()

file.handle(energy_trace2)

file.save_data()	
```

# Exemple 2
```python
from pyJoules import *

devices = pyJoules.discoverDevices()
pandas_recorder = PandasRecorder()

with EnergyTrace(devices, default_tag='tag') as trace:
	foo()
	trace.record(tag='middle')	
	bar()
	trace.stop()
	pandas_recorder.handle(trace)
```

# Proposal
```python
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
with EnergyContext(ConsolePrinter(), tag="bar", NvidiaDevice.GPU(1), RaplDevice.ALL()) as trace:
	foo()
	trace.record(tag="foo")
	bar()

# Usage 4 (configurable)
@measureit(ConsolePrinter(), NvidiaDevice.GPU(1), RaplDevice.ALL())
def foo():
	pass

# Usage 4 (advanced)
meter = EnergyMeter(NvidiaDevice.GPU(1), RaplDevice.ALL())

meter.start()
foo()
meter.record(tag="foo")
bar()
meter.stop(tag="bar")
ConsolePrinter.process(trace)

sample = meter.get_sample("bar)
print sample.energy(NvidiaDevice.GPU)
```
