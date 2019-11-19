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

from typing import List


class EnergyDevice:
    """
    Interface to get energy consumption information about a specific device
    """

    def available_domains(self) -> List[str]:
        """
        Returns names of the domain that could be monitored on the Device
        :return: a list of domain names
        """
        raise NotImplementedError()

    def get_energy(self, domains: List[str] = []) -> List[float]:
        """
        Get the energy consumption of the device since the last device reset
        :param domains: a list of domains to be monitored, by default (or if you pass an empty list as domains
                        parameter) all available domains are monitored
        :return: a list of each domain power consumption. Value order is the same than the domain order passed as
                 argument. By default this order is the same than the domain list returned by
                 :py:meth:`pyJoules.energy_device.EnergyDevice.available_domains` method.
        :raise NoSuchDomainError: if the domain could not be monitored on this machine
        """
        raise NotImplementedError()
