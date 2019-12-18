# MIT License
# Copyright (c) 2019, INRIA
# Copyright (c) 2019, University of Lille
# All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List, Optional

from . import EnergyDomain
from ..exception import PyJoulesException

class NotConfiguredDeviceException(PyJoulesException):
    """
    Exception raised when a user call the get_energy method if a device that was not configured before
    """


class EnergyDevice:
    """
    Interface to get energy consumption information about a specific device
    """

    @staticmethod
    def available_domains() -> List[str]:
        """
        Returns names of the domain that could be monitored on the Device
        :return: a list of domain names
        :raise NoSuchEnergyDeviceError: if the device is not available on this machine
        """
        raise NotImplementedError()

    def configure(self, domains: List[EnergyDomain] = None):
        """
        configure the device to return only the energy consumption of the given energy domain when calling the
        :py:meth:`pyJoules.energy_device.EnergyDevice.get_energy` method
        :param domains: domains to be monitored by the device, if None, all the available domain will be monitored
        :raise NoSuchDomainError: if one given domain could not be monitored on this machine
        """
        raise NotImplementedError()

    def get_energy(self) -> List[float]:
        """
        Get the energy consumption of the device since the last device reset
        :return: a list of each domain power consumption. Value order is the same than the domain order passed as
                 argument to the :py:meth:`pyJoules.energy_device.EnergyDevice.configure` method.
        """
        raise NotImplementedError()


class EnergyDeviceFactory:

    @staticmethod
    def create(domains: List[EnergyDomain]) -> List[EnergyDevice]:
        """
        return a list of devices that configured to monitor the given energy domains
        :param domains: list of energy domains to monitor
        :return: a list of energy devices configured to monitor the given energy domains
        """
        raise NotImplementedError()
