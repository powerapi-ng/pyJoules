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
from operator import add
from . import EnergyDomain, EnergyDevice
from .rapl_device import RaplDevice
from .nvidia_device import NvidiaGPUDevice
from ..exception import NoSuchEnergyDeviceError

from functools import reduce


class EnergyDeviceFactory:

    @staticmethod
    def _gen_all_available_domains() -> List[EnergyDevice]:
        available_api = [RaplDevice, NvidiaGPUDevice]
        available_domains = []
        for api in available_api:
            try:
                available_domains.append(api.available_domains())
            except NoSuchEnergyDeviceError:
                pass
        flaten_available_domain_list = reduce(add, available_domains, [])
        return flaten_available_domain_list

    @staticmethod
    def create_devices(domains: Optional[EnergyDomain] = None) -> List[EnergyDevice]:
        """
        Create and configure the EnergyDevice instance with the given EnergyDomains
        :param domains: a list of EnergyDomain instance that as to be monitored
        :return: a list of device configured with the given EnergyDomains
        :raise NoSuchEnergyDeviceError: if a domain depend on a device that doesn't exist on the current machine
        :raise NoSuchDomainError: if the given domain is not available on the device
        """
        if domains is None:
            domains = EnergyDeviceFactory._gen_all_available_domains()

        grouped_domains = {}
        for device_type, domain in map(lambda d: (d.get_device_type(), d), domains):
            if device_type in grouped_domains:
                grouped_domains[device_type].append(domain)
            else:
                grouped_domains[device_type] = [domain]

        devices = []

        for device_type in grouped_domains:
            device = device_type()
            device.configure(domains=grouped_domains[device_type])
            devices.append(device)
        return devices
