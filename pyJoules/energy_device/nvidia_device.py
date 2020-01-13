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

import pynvml
from . import EnergyDevice, EnergyDomain
from ..exception import PyJoulesException, NoSuchEnergyDeviceError


class NvidiaGPUDomain(EnergyDomain):

    def __init__(self, device_id):
        EnergyDomain.__init__(self)
        self.device_id = device_id
        self._repr = 'nvidia_gpu_' + str(device_id)

    def __repr__(self):
        return self._repr

    def __eq__(self, other) -> bool:
        return isinstance(other, NvidiaGPUDomain) and self.__repr__() == other.__repr__()

    def __lt__(self, other) -> bool:
        if isinstance(other, NvidiaGPUDomain):
            return self.device_id < other.device_id
        raise ValueError()

    def __gt__(self, other) -> bool:
        if isinstance(other, NvidiaGPUDomain):
            return self.device_id > other.device_id
        raise ValueError()

    def get_device_type(self):
        return NvidiaGPUDevice


class GPUDoesNotSupportEnergyMonitoringError(PyJoulesException):
    """
    Exception raised when a NvidiaDevice is created but the GPU does not support energy monitoring
    """


class NvidiaGPUDevice(EnergyDevice):
    """
    Interface to get energy consumption of GPUs
    """

    def __init__(self):
        """
        :raise NoSuchEnergyDeviceError: if no Nvidia API is available on this machine
        :raise GPUDoesNotSupportEnergyMonitoringError: if the GPU does not support energy monitoring
        """
        EnergyDevice.__init__(self)
        self._handle = None

    def configure(self, domains: List[NvidiaGPUDomain] = None):
        EnergyDevice.configure(self, domains)
        self._handle = [pynvml.nvmlDeviceGetHandleByIndex(domain.device_id) for domain in self._configured_domains]

    def get_energy(self):
        return [pynvml.nvmlDeviceGetTotalEnergyConsumption(handle) for handle in self._handle]

    @staticmethod
    def available_domains() -> List[NvidiaGPUDomain]:
        try:
            pynvml.nvmlInit()
        except pynvml.NVMLError:
            raise NoSuchEnergyDeviceError()

        device_ids = pynvml.nvmlDeviceGetCount()
        domains = map(lambda device_id: NvidiaGPUDomain(device_id), range(device_ids))
        return list(domains)
