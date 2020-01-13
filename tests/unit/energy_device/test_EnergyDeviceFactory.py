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

import pytest

from pyJoules.exception import NoSuchDomainError, NoSuchEnergyDeviceError
from pyJoules.energy_device import EnergyDeviceFactory
from pyJoules.energy_device.rapl_device import RaplPackageDomain, RaplDramDomain, RaplDevice
from pyJoules.energy_device.nvidia_device import NvidiaGPUDevice, NvidiaGPUDomain
from ...utils.fake_nvidia_api import no_gpu_api, one_gpu_api, two_gpu_api
from ...utils.rapl_fs import fs_pkg_one_socket, fs_pkg_dram_one_socket, empty_fs


def test_create_devices_with_one_rapl_package_domain_return_one_correctly_configured_rapl_device(fs_pkg_dram_one_socket):
    domains = [RaplPackageDomain(0)]
    devices = EnergyDeviceFactory.create_devices(domains)

    assert len(devices) == 1
    assert isinstance(devices[0], RaplDevice)
    assert devices[0].get_configured_domains() == domains


def test_create_devices_with_rapl_package_and_dram_domains_return_one_correctly_configured_rapl_device(fs_pkg_dram_one_socket):
    domains = [RaplPackageDomain(0), RaplDramDomain(0)]
    devices = EnergyDeviceFactory.create_devices(domains)

    assert len(devices) == 1
    assert isinstance(devices[0], RaplDevice)
    assert devices[0].get_configured_domains() == domains


def test_create_devices_with_dram_rapl_domain_without_dram_support_raise_NoSuchDomainError(fs_pkg_one_socket):
    with pytest.raises(NoSuchDomainError):
        EnergyDeviceFactory.create_devices([RaplDramDomain(0)])

def test_create_devices_to_monitor_rapl_without_rapl_api_raise_NoSuchEnergyDeviceError(empty_fs):
    with pytest.raises(NoSuchEnergyDeviceError):
        EnergyDeviceFactory.create_devices([RaplDramDomain(0)])
        
def test_create_devices_to_monitor_gpu0_with_one_gpu_api_return_one_correctly_configured_nvidia_gpu_device(one_gpu_api):
    domains = [NvidiaGPUDomain(0)]
    devices = EnergyDeviceFactory.create_devices(domains)

    assert len(devices) == 1
    assert isinstance(devices[0], NvidiaGPUDevice)
    assert devices[0].get_configured_domains() == domains


def test_create_devices_to_monitor_gpu0_and_gpu1_with_two_gpu_api_return_one_correctly_configured_nvidia_gpu_device(two_gpu_api):
    domains = [NvidiaGPUDomain(0), NvidiaGPUDomain(1)]
    devices = EnergyDeviceFactory.create_devices(domains)

    assert len(devices) == 1
    assert isinstance(devices[0], NvidiaGPUDevice)
    assert devices[0].get_configured_domains() == domains


def test_create_devices_to_monitor_gpu0_without_gpu_api_raise_NoSuchEnergyDeviceError(no_gpu_api):
    with pytest.raises(NoSuchEnergyDeviceError):
        EnergyDeviceFactory.create_devices([NvidiaGPUDomain(0)])

def test_create_devices_to_monitor_gpu1_with_only_one_gpu_api_raise_NoSuchDomainError(one_gpu_api):
    with pytest.raises(NoSuchDomainError):
        EnergyDeviceFactory.create_devices([NvidiaGPUDomain(1)])

def test_create_devices_to_monitor_gpu0_and_package_0_machine_with_two_gpu_and_package_dram_api_create_one_nvidia_gpu_device_and_rapl_device_configured_for_package(two_gpu_api, fs_pkg_dram_one_socket):
    devices = EnergyDeviceFactory.create_devices([RaplPackageDomain(0), NvidiaGPUDomain(0)])

    assert len(devices) == 2
    assert isinstance(devices[1], NvidiaGPUDevice)
    assert devices[1].get_configured_domains() == [NvidiaGPUDomain(0)]
    assert isinstance(devices[0], RaplDevice)
    assert devices[0].get_configured_domains() == [RaplPackageDomain(0)]

        
def test_create_devices_with_default_values_on_machine_with_only_rapl_pkg_and_dram_api_create_one_device_configured_for_dram_and_rapl(fs_pkg_dram_one_socket):
    devices = EnergyDeviceFactory.create_devices()

    assert len(devices) == 1
    assert isinstance(devices[0], RaplDevice)
    assert devices[0].get_configured_domains() == [RaplPackageDomain(0), RaplDramDomain(0)]


def test_create_devices_with_default_values_on_machine_with_only_one_gpu_create_one_nvidia_gpu_device(one_gpu_api, empty_fs):
    devices = EnergyDeviceFactory.create_devices()

    assert len(devices) == 1
    assert isinstance(devices[0], NvidiaGPUDevice)
    assert devices[0].get_configured_domains() == [NvidiaGPUDomain(0)]


def test_create_devices_with_default_values_on_machine_with_one_gpu_and_package_api_create_one_nvidia_gpu_device_and_rapl_device_configured_for_package(one_gpu_api, fs_pkg_one_socket):
    devices = EnergyDeviceFactory.create_devices()

    assert len(devices) == 2
    assert isinstance(devices[1], NvidiaGPUDevice)
    assert devices[1].get_configured_domains() == [NvidiaGPUDomain(0)]
    assert isinstance(devices[0], RaplDevice)
    assert devices[0].get_configured_domains() == [RaplPackageDomain(0)]
