# PyJoules

[![License: MIT](https://img.shields.io/pypi/l/pyRAPL)](https://spdx.org/licenses/MIT.html)
[![Build Status](https://img.shields.io/circleci/build/github/powerapi-ng/pyJoules.svg)](https://circleci.com/gh/powerapi-ng/pyjoules)


# About
**pyJoules** is a software toolkit to measure the energy footprint of a host machine along the execution of a piece of Python code.
It monitors the energy consumed by specific device of the host machine such as :

- intel CPU socket package
- RAM (for intel server architectures)
- intel integrated GPU (for client architectures)
- nvidia GPU

## Limitation

### CPU, RAM and integrated GPU
**pyJoules** uses the Intel "_Running Average Power Limit_" (RAPL) technology that estimates power consumption of the CPU, ram and integrated GPU.
This technology is available on Intel CPU since the [Sandy Bridge generation](https://fr.wikipedia.org/wiki/Intel#Historique_des_microprocesseurs_produits)(2010).

### Nvidia GPU
**pyJoules** uses the nvidia "_Nvidia Management Library_" technology to measure energy consumption of nvidia devices. The energy measurement API is only available on nvidia GPU with [Volta architecture](https://en.wikipedia.org/wiki/Volta_(microarchitecture))(2018)
# Installation

### Measurement frequency
PyJoule use hardware measurement tools (intel RAPL, nvidia GPU tools, ...) to measure device energy consumption. Theses tools have a mesasurement frequency that depend of the device. Thus, you can't use Pyjoule to measure energy consumption during a period shorter than the device energy measurement frequency. Pyjoule will return null values if the measurement period is to short.

## Requirements

- python >= 3.7
- [nvml](https://developer.nvidia.com/nvidia-management-library-nvml) (if you want nvidia GPU support)

## Installation
You can install **pyJoules** with pip: `pip install pyJoules`

if you want to use pyJoule to also measure nvidia GPU energy consumption, you have to install it with nvidia driver support using this command : `pip install pyJoules[nvidia]`.

# Basic usage

Here are some basic usages of **pyJoules**. Please note that the reported energy consumption is not only the energy consumption of the code you are running. This includes the _global energy consumption_ of all the process running on the machine during this period, thus including the operating system and other applications.
That is why we recommend to eliminate any extra programs that may alter the energy consumption of the machine hosting experiments and to keep _only_ the code under measurement (_i.e._, no extra applications, such as graphical interface, background running task...). This will give the closest measure to the real energy consumption of the measured code.

## Decorate a function to measure its energy consumption

To measure the energy consumed by the machine during the execution of the function `foo()` run the following code:
```python
from pyJoules.energy_meter import measureit

@measureit
def foo():
	# Instructions to be evaluated.

foo()
```

This will print on the console the recorded energy consumption of all the monitorable devices during the execution of function `foo`.

### Output description
decorator basic usage will print iformation with this format : 

`begin timestamp : XXX; tag : YYY; duration : ZZZ;device_name: AAAA`

with : 
- `begin timestamp` : monitored function launching time
- `tag`: tag of the measure, if nothing is specified, this will be the function name
- `duration`: function execution duration
- `device_name`: power consumption of the device `device_name` in uJ

for cpu and ram devices, device_name match the RAPL domain described on the image below plus the CPU socket id. Rapl domain are described [here](https://github.com/powerapi-ng/pyJoules/blob/master/README.md#rapl-domain-description)

## Configure the decorator specifying the device to monitor

You can easily configure which device to monitor using the parameters of the `measureit` decorator. 
For example, the following example only monitors the CPU power consumption on the CPU socket `1` and the Nvidia GPU `0`.
By default, **pyJoules** monitors all the available devices of the CPU sockets.
```python
from pyJoules.energy_meter import measureit
from pyJoules.energy_device.rapl_device import RaplPackageDomain
from pyJoules.energy_device.nvidia_device import NvidiaGPUDomain
	
@measureit(domains=[RaplPackageDomain(1), NvidiaGPUDomain(0)])
def foo():
	# Instructions to be evaluated.
	
foo()	
```

You can append the following domain list to monitor them : 
	
- `pyJoules.energy_device.rapl_device.RaplPackageDomain` : CPU (specify the socket id in parameter)
- `pyJoules.energy_device.rapl_device.RaplDramDomain` : RAM (specify the socket id in parameter)
- `pyJoules.energy_device.rapl_device.RaplUncoreDomain` : integrated GPU (specify the socket id in parameter)
- `pyJoules.energy_device.rapl_device.RaplCoreDomain` : RAPL Core domain (specify the socket id in parameter)
- `pyJoules.energy_device.nvidia_device.NvidiaGPUDomain` : Nvidia GPU (specify the socket id in parameter)

to understand which par of the cpu each RAPL domain monitor, see this [section](https://github.com/powerapi-ng/pyJoules/blob/master/README.md#rapl-domain-description)

## Configure the output of the decorator

If you want to handle data with different output than the standard one, you can configure the decorator with an `EnergyHandler` instance from the `pyJoules.energy_handler` module.

As an example, if you want to write the recorded energy consumption in a .csv file:
```python
from pyJoules.energy_meter import measureit
from pyJoules.energy_handler.energy_recorder import CSVHandler
	
csv_handler = CSVHandler('result.csv')
	
@measureit(handler=csv_handler)
def foo():
	# Instructions to be evaluated.

for _ in range(100):
	foo()
		
csv_handler.save_data()
```

This will produce a csv file of 100 lines. Each line containing the energy
consumption recorded during one execution of the function `foo`.
Other predefined `Handler` classes exist to export data to *MongoDB* and *Panda*
dataframe.

## Use a context manager to add tagged "_breakpoint_" in your measurment

If you want to know where is the "_hot spots_" where your python code consume the
most energy you can add "_breakpoints_" during the measurement process and tag
them to know amount of energy consumed between this breakpoints.

For this, you have to use a context manager to measure the energy
consumption. It is configurable as the decorator. For example, here we use an
`EnergyContext` to measure the power consumption of CPU `1` and nvidia gpu `0`
and report it in a csv file : 

```python
from pyJoules.energy_meter import EnergyContext
from pyJoules.energy_device.rapl_device import RaplPackageDomain
from pyJoules.energy_device.nvidia_device import NvidiaGPUDomain
from pyJoules.energy_handler.energy_recorder import CSVHandler
	
csv_handler = CSVHandler('result.csv')

with EnergyContext(handler=csv_handler, domains=[RaplPackageDomain(1), NvidiaGPUDomain(0)], start_tag='foo') as ctx:
	foo()
	ctx.record(tag='bar')
	bar()

csv_handler.save_data()
```

This will record the energy consumed :

- between the beginning of the `EnergyContext` and the call of the `ctx.record` method
- between the call of the `ctx.record` method and the end of the `EnergyContext`

Each measured part will be written in the csv file. One line per part.

# RAPL domain description

RAPL domains match part of the cpu socket as described in this image : 

![](https://raw.githubusercontent.com/powerapi-ng/pyJoules/master/rapl_domains.png)

- Package : correspond to the wall cpu energy consumption
- core : correpond to the sum of all cpu core energy consumption
- uncore : correspond to the integrated GPU

# Miscellaneous

## About

**pyJoules** is an open-source project developed by the [Spirals research group](https://team.inria.fr/spirals) (University of Lille and Inria) that is part of the [PowerAPI](http://powerapi.org) initiative.

The documentation is available [here](https://pyJoules.readthedocs.io/en/latest/).

## Mailing list

You can follow the latest news and asks questions by subscribing to our <a href="mailto:sympa@inria.fr?subject=subscribe powerapi">mailing list</a>.

## Contributing

If you would like to contribute code, you can do so via GitHub by forking the repository and sending a pull request.

When submitting code, please make every effort to follow existing coding conventions and style in order to keep the code as readable as possible.
