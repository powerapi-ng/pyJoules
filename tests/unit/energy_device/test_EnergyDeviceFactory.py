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

from pyJoules.exception import NoSuchDomainError
from pyJoules.energy_device import EnergyDeviceFactory
from pyJoules.energy_device.rapl_device import RaplPackageDomain, RaplDramDomain, RaplDevice

from ...utils.rapl_fs import fs_pkg_one_socket, fs_pkg_dram_one_socket


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

def test_create_devices_with_default_values_on_machine_with_only_rapl_pkg_and_dram_api_create_one_device_configured_for_dram_and_rapl(fs_pkg_dram_one_socket):
    devices = EnergyDeviceFactory.create_devices()

    assert len(devices) == 1
    assert isinstance(devices[0], RaplDevice)
    assert devices[0].get_configured_domains() == [RaplPackageDomain(0), RaplDramDomain(0)]
