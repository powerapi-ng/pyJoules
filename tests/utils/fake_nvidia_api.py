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

import random
import pytest
from pynvml import NVMLError
from pyJoules.energy_device.nvidia_device import NvidiaGPUDomain, NvidiaGPUDevice
from .fake_api import FakeAPI
from mock import patch, Mock

class FakeNvidiaAPI(FakeAPI):

    def __init__(self, number_of_device):
        self.number_of_device = number_of_device

        self.domains_current_energy = None

    def reset_values(self):
        self.domains_current_energy = {}
        for device_id in range(self.number_of_device):
            self.domains_current_energy[str(NvidiaGPUDomain(device_id))] = random.random()

    def get_energy_value(self, device_id):
        return self.domains_current_energy[str(NvidiaGPUDomain(device_id))]

    def get_device_type(self):
        return NvidiaGPUDevice

@pytest.fixture
def no_gpu_api():
    patcher = patch('pynvml.nvmlInit', side_effect=NVMLError(0))
    yield patcher.start()
    patcher.stop()


class MockedHandle(Mock):

    def __init__(self, device_id):
        Mock.__init__(self)
        self.device_id = device_id


@pytest.fixture
def one_gpu_api():
    fake_api = FakeNvidiaAPI(1)
    fake_api.reset_values()

    patcher_init = patch('pynvml.nvmlInit')
    patcher_device_count = patch('pynvml.nvmlDeviceGetCount', return_value=1)
    patcher_get_handle = patch('pynvml.nvmlDeviceGetHandleByIndex', side_effect=MockedHandle)
    patcher_get_energy = patch('pynvml.nvmlDeviceGetTotalEnergyConsumption',
                               side_effect=lambda mocked_handle: fake_api.get_energy_value(mocked_handle.device_id))

    patcher_init.start()
    patcher_device_count.start()
    patcher_get_handle.start()
    patcher_get_energy.start()
    yield fake_api
    patcher_init.stop()
    patcher_device_count.stop()
    patcher_get_handle.stop()
    patcher_get_energy.stop()


@pytest.fixture
def two_gpu_api():
    fake_api = FakeNvidiaAPI(2)
    fake_api.reset_values()

    patcher_init = patch('pynvml.nvmlInit')
    patcher_device_count = patch('pynvml.nvmlDeviceGetCount', return_value=2)
    patcher_get_handle = patch('pynvml.nvmlDeviceGetHandleByIndex', side_effect=MockedHandle)
    patcher_get_energy = patch('pynvml.nvmlDeviceGetTotalEnergyConsumption',
                               side_effect=lambda mocked_handle: fake_api.get_energy_value(mocked_handle.device_id))

    patcher_init.start()
    patcher_device_count.start()
    patcher_get_handle.start()
    patcher_get_energy.start()
    yield fake_api
    patcher_init.stop()
    patcher_device_count.stop()
    patcher_get_handle.stop()
    patcher_get_energy.stop()
