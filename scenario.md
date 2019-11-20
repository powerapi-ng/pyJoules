
# Exemple 1

	from pyJoules import *
	
	rapl = RaplDevice(RaplDevice.package(0), RaplDevice.package(1), RaplDevice.dram(1))
	gpu = NvidiaDevice(NvidiaDevice.gpu(0)
	file = FileRecorder('result.csv')
		
	energy_trace = EnergyTrance(devices, default_tag='tag')
	
	energy_trace.start(tag='start')
	foo()
	energy_trace.record(tag='middle')	
	bar()
	energy_trace.stop()
	
	file.handle(energy_trace)
	
	energy_trace2 = EnergyTrance(devices)
	energy_trace2.start(tag='start2')
	foo()
	energy_trace2.record(tag='middle2')	
	bar()
	energy_trace2.stop()
	
	file.handle(energy_trace2)
	
	file.save_data()	
	
# Exemple 2

	from pyJoules import *
	
	devices = pyJoules.discoverDevices()
	pandas_recorder = PandasRecorder()
	
	with EnergyTrance(devices, default_tag='tag') as trace:
		foo()
		trace.record(tag='middle')	
		bar()
		trace.stop()
		pandas_recorder.handle(trace)
