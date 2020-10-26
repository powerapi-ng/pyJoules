Nvidia GPU
**********
**pyJoules** uses the nvidia "*Nvidia Management Library*" technology to measure energy consumption of nvidia devices. The energy measurement API is only available on nvidia GPU with `Volta architecture`__ (2018)

__ https://en.wikipedia.org/wiki/Volta_(microarchitecture)

Usage
=====
To configure your function decorator, context manager or energy meter to measure the energy consumption of a GPU, pass as :code:`domain` attribute a list of instance of :code:`pyJoules.device.rapl_device.NvidiaGPUDomain`.

For example, if you want to configure a context manager to measure the energy consumed by the gpu of id :code:`0` follow this example :

.. code-block:: python

   from pyJoules.device.nvidia_device import NvidiaGPUDomain
   with EnergyContext(domains=[NvidiaGPUDomain(0)):
       foo()
