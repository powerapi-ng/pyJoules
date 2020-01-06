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

from .... utils.rapl_fs import *

from pyJoules.energy_device import NotConfiguredDeviceException
from pyJoules.energy_device.rapl_device import RaplDevice, RaplPackageDomain, RaplDramDomain, RaplCoreDomain
from pyJoules.energy_device.rapl_device import RaplUncoreDomain
from pyJoules.exception import NoSuchEnergyDeviceError, NoSuchDomainError

##############
# INIT TESTS #
##############
def test_create_RaplDevice_with_no_rapl_api_raise_NoSuchEnergyDeviceError(empty_fs):
    with pytest.raises(NoSuchEnergyDeviceError):
        RaplDevice()

def test_create_RaplDevice(fs_pkg_one_socket):
    device = RaplDevice()
    assert device is not None
    assert isinstance(device, RaplDevice)


###########################
# AVAILABLE DOMAINS TESTS #
###########################
def test_available_domains_with_no_rapl_api_raise_NoSuchEnergyDeviceError(empty_fs):
    with pytest.raises(NoSuchEnergyDeviceError):
        RaplDevice.available_domains()


def test_available_domains_with_pkg_rapl_api_return_correct_values(fs_pkg_one_socket):
    returned_values = RaplDevice.available_domains()
    correct_values = [RaplPackageDomain(0)]
    assert sorted(correct_values) == sorted(returned_values)


def test_available_domains_with_pkg_and_dram_rapl_api_return_correct_values(fs_pkg_dram_one_socket):
    returned_values = RaplDevice.available_domains()
    correct_values = [RaplPackageDomain(0), RaplDramDomain(0)]
    assert sorted(correct_values) == sorted(returned_values)

def test_available_domains_with_pkg_core_and_dram_rapl_api_return_correct_values(fs_pkg_dram_core_one_socket):
    returned_values = RaplDevice.available_domains()
    correct_values = [RaplPackageDomain(0), RaplDramDomain(0), RaplCoreDomain(0)]
    assert sorted(correct_values) == sorted(returned_values)


def test_available_domains_with_pkg_uncore_and_dram_rapl_api_return_correct_values(fs_pkg_dram_uncore_one_socket):
    returned_values = RaplDevice.available_domains()
    correct_values = [RaplPackageDomain(0), RaplDramDomain(0), RaplUncoreDomain(0)]
    assert sorted(correct_values) == sorted(returned_values)


def test_available_domains_with_pkg_psys_rapl_api_return_correct_values(fs_pkg_psys_one_socket):
    returned_values = RaplDevice.available_domains()
    correct_values = [RaplPackageDomain(0)]
    assert sorted(correct_values) == sorted(returned_values)


def test_available_domains_with_pkg_dram_rapl_api_two_cpu_return_correct_values(fs_pkg_dram_two_socket):
    returned_values = RaplDevice.available_domains()
    correct_values = [RaplPackageDomain(0), RaplDramDomain(0), RaplPackageDomain(1), RaplDramDomain(1)]
    assert sorted(correct_values) == sorted(returned_values)


###################
# CONFIGURE TESTS #
###################
def test_configure_device_to_get_dram_energy_with_no_rapl_dram_api_raise_NoSuchDomainError(fs_pkg_one_socket):
    device = RaplDevice()

    with pytest.raises(NoSuchDomainError):
        device.configure([RaplDramDomain(0)])

def test_configure_device_to_get_pkg_energy_on_cpu1_with_no_cpu1_raise_NoSuchDomainError(fs_pkg_dram_one_socket):
    device = RaplDevice()

    with pytest.raises(NoSuchDomainError):
        device.configure([RaplPackageDomain(1)])

def test_get_configured_domains_on_non_configured_device_raise_NotConfiguredDeviceException(fs_pkg_dram_one_socket):
    device = RaplDevice()

    with pytest.raises(NotConfiguredDeviceException):
        device.get_configured_domains()


def test_get_configured_domains_with_default_values_on_pkg_rapl_api_return_correct_values(fs_pkg_one_socket):
    configured_domains = [RaplPackageDomain(0)]
    device = RaplDevice()
    device.configure()
    assert configured_domains == device.get_configured_domains()


def test_get_configured_domains_with_default_values_on_pkg_dram_rapl_api_return_correct_values(fs_pkg_dram_one_socket):
    configured_domains = [RaplPackageDomain(0), RaplDramDomain(0)]
    device = RaplDevice()
    device.configure()
    assert configured_domains == device.get_configured_domains()


def test_get_configured_domains_with_pkg_values_on_pkg_dram_rapl_api_return_correct_values(fs_pkg_dram_one_socket):
    configured_domains = [RaplPackageDomain(0)]
    device = RaplDevice()
    device.configure(configured_domains)
    assert configured_domains == device.get_configured_domains()


########################################
# GET ENERGY WITH DEFAULT VALUES TESTS #
########################################
def test_get_default_energy_values_with_pkg_rapl_api(fs_pkg_one_socket):
    device = RaplDevice()
    device.configure()
    assert device.get_energy() == [fs_pkg_one_socket.domains_current_energy['package_0']]


def test_get_default_energy_values_with_pkg_dram_rapl_api(fs_pkg_dram_one_socket):
    device = RaplDevice()
    device.configure()
    assert device.get_energy() == [fs_pkg_dram_one_socket.domains_current_energy['package_0'],
                                   fs_pkg_dram_one_socket.domains_current_energy['dram_0']]


def test_get_default_energy_values_with_pkg_dram_rapl_api_two_sockets(fs_pkg_dram_two_socket):
    device = RaplDevice()
    device.configure()
    assert device.get_energy() == [fs_pkg_dram_two_socket.domains_current_energy['package_0'],
                                   fs_pkg_dram_two_socket.domains_current_energy['package_1'],
                                   fs_pkg_dram_two_socket.domains_current_energy['dram_0'],
                                   fs_pkg_dram_two_socket.domains_current_energy['dram_1']]


##################################
# CONFIGURE AND GET ENERGY TESTS #
##################################
def test_get_package_energy_with_only_pkg_rapl_api_return_correct_value(fs_pkg_one_socket):
    """
    Create a RaplDevice instance on a machine with package rapl api with on one socket
    configure it to monitor package domain
    use the `get_energy` method and check if:
    - the returned list contains one element
    - this element is the power consumption of the package on socket 0
    """
    device = RaplDevice()
    device.configure([RaplPackageDomain(0)])
    assert device.get_energy() == [fs_pkg_one_socket.domains_current_energy['package_0']]


def test_get_dram_energy_with_pkg_dram_rapl_api_return_correct_value(fs_pkg_dram_one_socket):
    """
    Create a RaplDevice instance on a machine with package and dram rapl api with on one socket
    configure it to monitor dram domain
    use the `get_energy` method and check if:
    - the returned list contains one element
    - this element is the power consumption of the dram on socket 0
    """
    device = RaplDevice()
    device.configure([RaplDramDomain(0)])
    assert device.get_energy() == [fs_pkg_dram_one_socket.domains_current_energy['dram_0']]


def test_get_package_dram_energy_with_pkg_dram_rapl_api_return_correct_value(fs_pkg_dram_one_socket):
    """
    Create a RaplDevice instance on a machine with package and dram rapl api with on one socket
    configure it to monitor package and dram domains
    use the `get_energy` method and check if:
    - the returned list contains two elements
    - these elements are the power consumption of the package and dram on socket 0
    """
    device = RaplDevice()
    device.configure([RaplPackageDomain(0), RaplDramDomain(0)])
    assert device.get_energy() == [fs_pkg_dram_one_socket.domains_current_energy['package_0'],
                                   fs_pkg_dram_one_socket.domains_current_energy['dram_0']]


def test_get_dram_package_energy_with_pkg_dram_rapl_api_return_correct_values_in_correct_order(fs_pkg_dram_one_socket):
    """
    Create a RaplDevice instance on a machine with package and dram rapl api with on one socket
    configure it to monitor dram and package domains
    use the `get_energy` method and check if:
    - the returned list contains two elements
    - these elements are the power consumption of the dram and package on socket 0
    """
    device = RaplDevice()
    device.configure([RaplDramDomain(0), RaplPackageDomain(0)])
    assert device.get_energy() == [fs_pkg_dram_one_socket.domains_current_energy['dram_0'],
                                   fs_pkg_dram_one_socket.domains_current_energy['package_0']]


def test_get_package_dram_energy_with_pkg_dram_rapl_api_two_sockets_return_correct_value(fs_pkg_dram_two_socket):
    """
    Create a RaplDevice instance on a machine with package and dram rapl api with on two socket
    configure it to monitor package and dram domains
    use the `get_energy` method and check if:
    - the returned list contains 4 elements
    - these elements are the power consumption of the package and dram on socket 0 and socket 1
    """
    device = RaplDevice()
    device.configure([RaplPackageDomain(0), RaplDramDomain(0), RaplPackageDomain(1), RaplDramDomain(1)])
    assert device.get_energy() == [fs_pkg_dram_two_socket.domains_current_energy['package_0'],
                                   fs_pkg_dram_two_socket.domains_current_energy['dram_0'],
                                   fs_pkg_dram_two_socket.domains_current_energy['package_1'],
                                   fs_pkg_dram_two_socket.domains_current_energy['dram_1']]


def test_get_package0_and_all_dram_energy_with_pkg_dram_rapl_api_two_sockets_return_correct_value(fs_pkg_dram_two_socket):
    """
    Create a RaplDevice instance on a machine with package and dram rapl api with on two socket
    configure it to monitor package domains on socket 0 and dram domains on socket 0 and 1
    use the `get_energy` method and check if:
    - the returned list contains 3 elements
    - these elements are the power consumption of the package on socket 0 and dram on socket 0 and socket 1
    """
    device = RaplDevice()
    device.configure([RaplPackageDomain(0), RaplDramDomain(0), RaplDramDomain(1)])
    assert device.get_energy() == [fs_pkg_dram_two_socket.domains_current_energy['package_0'],
                                   fs_pkg_dram_two_socket.domains_current_energy['dram_0'],
                                   fs_pkg_dram_two_socket.domains_current_energy['dram_1']]
