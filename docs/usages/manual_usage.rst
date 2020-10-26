Manual usage
************

Use a EnergyMeter to measure energy consumption without decorator or context manager
------------------------------------------------------------------------------------

If you want need more flexibility and measure energy consumption of piece of
code that can't be bound inside a decorated function of a context manager, you
can use an instance of :raw-role:`<a
href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter">` ``EnergyMeter``
:raw-role:`</a>`.

Instance of :raw-role:`<a
href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter">` ``EnergyMeter``
:raw-role:`</a>` is the underlayer tool used by context manager and
decorator to measure energy consumption.

Create the EnergyMeter
^^^^^^^^^^^^^^^^^^^^^^

Before using an energy meter, you have to create it with devices that it have to monitor. For this, use an :raw-role:`<a
href="../API/main_api.html#pyJoules.device.device_factory.DeviceFactory">` ``DeviceFactory`` :raw-role:`</a>` to create and configure the monitored devices

The following piece of code show how to create an :raw-role:`<a
href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter">` ``EnergyMeter``
:raw-role:`</a>` that monitor CPU, DRAM and GPU energy consumption.

.. code-block:: python

   domains = [RaplPackageDomain(0), RaplDramDomain(0), NvidiaGPUDomain(0)]
   devices = DeviceFactory.create_devices(domains)
   meter = EnergyMeter(devices)

Tips : call the :raw-role:`<a href="../API/main_api.html#pyJoules.device.device_factory.DeviceFactory.create_devices">` ``DeviceFactory.create_devices`` :raw-role:`</a>` without parameter to get the list of all monitorable devices.

Use the EnergyMeter
^^^^^^^^^^^^^^^^^^^
   
When you have your :raw-role:`<a
href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter">` ``EnergyMeter``
:raw-role:`</a>` you can use it to measure energy consumption of piece of code.

An :raw-role:`<a
href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter">` ``EnergyMeter``
:raw-role:`</a>` have three main method :

- :raw-role:`<a href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter.start">` ``start`` :raw-role:`</a>`: to start the energy consumption monitoring
- :raw-role:`<a href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter.record">` ``record`` :raw-role:`</a>`: to tag a hotspot in monitored piece of code
- :raw-role:`<a href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter.stop">` ``stop`` :raw-role:`</a>`: to stop the energy consumption monitoring

The following piece of code show how to use an :raw-role:`<a
href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter">` ``EnergyMeter``
:raw-role:`</a>` to monitor piece of code: 

.. code-block:: python

   meter.start(tag='foo')
   foo()
   meter.record(tag='bar')
   bar()
   meter.stop()

Get the EnergyTrace
^^^^^^^^^^^^^^^^^^^

When you finished to measure the energy consumed during execution of your piece of code, you can retrieve its energy trace using the :raw-role:`<a href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter.get_trace">` ``EnergyMeter.get_trace`` :raw-role:`</a>` method

This will return an iterator on some :raw-role:`<a href="../API/main_api.html#pyJoules.energy_trace.EnergySample">` ``EnergySample`` :raw-role:`</a>`. Each energy sample contains energy consumption information measured between each call to :raw-role:`<a href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter.start">` ``start`` :raw-role:`</a>`, :raw-role:`<a href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter.record">` ``record`` :raw-role:`</a>` and :raw-role:`<a href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter.stop">` ``stop`` :raw-role:`</a>` method.

For example, the trace of the previous example contains two :raw-role:`<a href="../API/main_api.html#pyJoules.energy_trace.EnergySample">` ``EnergySample`` :raw-role:`</a>`. One that contains the energy measured between :raw-role:`<a href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter.start">` ``start`` :raw-role:`</a>` and :raw-role:`<a href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter.record">` ``record`` :raw-role:`</a>` methods (during ``foo`` method execution) and the second that contains energy measured between :raw-role:`<a href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter.record">` ``record`` :raw-role:`</a>` and :raw-role:`<a href="../API/main_api.html#pyJoules.energy_meter.EnergyMeter.stop">` ``stop`` :raw-role:`</a>` method (during ``bar`` method execution) .

Energy sample contains :

- a tag
- a timestamp (the beginning of the measure)
- the duration of the measure
- the energy consumed during the measure

Full Example
^^^^^^^^^^^^

.. code-block:: python

   from pyJoules.device import DeviceFactory
   from pyJoules.device.rapl_device import RaplPackageDomain, RaplDramDomain
   from pyJoules.device.nvidia_device import NvidiaGPUDomain
   from pyJoules.energy_meter import EnergyMeter
   
   domains = [RaplPackageDomain(0), RaplDramDomain(0), NvidiaGPUDomain(0)]
   devices = DeviceFactory.create_devices(domains)
   meter = EnergyMeter(devices)
   
   meter.start(tag='foo')
   foo()
   meter.record(tag='bar')
   bar()
   meter.stop()

   trace = meter.get_trace()

 
