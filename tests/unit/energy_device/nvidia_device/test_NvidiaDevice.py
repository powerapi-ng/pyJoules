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
import pynvml
from mock import patch
from ....utils.fake_nvidia_api import no_gpu_api, one_gpu_api, two_gpu_api
from pyJoules.energy_device.nvidia_device import NvidiaGPUDevice, NvidiaGPUDomain
from pyJoules.energy_device import NotConfiguredDeviceException
from pyJoules.exception import NoSuchEnergyDeviceError, NoSuchDomainError

##############
# INIT TESTS #
##############
def test_create_NvidiaDevice_with_no_gpu_api_raise_NoSuchEnergyDeviceError(no_gpu_api):
    with pytest.raises(NoSuchEnergyDeviceError):
        NvidiaGPUDevice()

###########################
# AVAILABLE DOMAINS TESTS #
###########################
def test_available_domains_with_no_gpu_api_raise_NoSuchEnergyDeviceError(no_gpu_api):
    with pytest.raises(NoSuchEnergyDeviceError):
        NvidiaGPUDevice.available_domains()


def test_available_domains_with_one_gpu_api_return_correct_values(one_gpu_api):
    returned_values = NvidiaGPUDevice.available_domains()
    correct_values = [NvidiaGPUDomain(0)]
    assert sorted(correct_values) == sorted(returned_values)


def test_available_domains_with_two_gpu_api_return_correct_values(two_gpu_api):
    returned_values = NvidiaGPUDevice.available_domains()
    correct_values = [NvidiaGPUDomain(0), NvidiaGPUDomain(1)]
    assert sorted(correct_values) == sorted(returned_values)


###################
# CONFIGURE TESTS #
###################
def test_configure_device_to_get_second_gpu_energy_with_no_second_gpu_api_raise_NoSuchDomainError(one_gpu_api):
    device = NvidiaGPUDevice()

    with pytest.raises(NoSuchDomainError):
        device.configure([NvidiaGPUDomain(1)])


def test_get_configured_domains_on_non_configured_device_raise_NotConfiguredDeviceException(one_gpu_api):
    device = NvidiaGPUDevice()

    with pytest.raises(NotConfiguredDeviceException):
        device.get_configured_domains()


def test_get_configured_domains_with_default_values_with_one_gpu_api_return_correct_values(one_gpu_api):
    configured_domains = [NvidiaGPUDomain(0)]
    device = NvidiaGPUDevice()
    device.configure()
    assert configured_domains == device.get_configured_domains()


def test_get_configured_domains_with_default_values_on_two_gpu_api_return_correct_values(two_gpu_api):
    configured_domains = [NvidiaGPUDomain(0), NvidiaGPUDomain(1)]
    device = NvidiaGPUDevice()
    device.configure()
    assert configured_domains == device.get_configured_domains()


########################################
# GET ENERGY WITH DEFAULT VALUES TESTS #
########################################
def test_get_default_energy_values_with_one_gpu_api(one_gpu_api):
    device = NvidiaGPUDevice()
    device.configure()
    assert device.get_energy() == [one_gpu_api.domains_current_energy['nvidia_gpu_0']]


def test_get_default_energy_values_with_two_gpu_api(two_gpu_api):
    device = NvidiaGPUDevice()
    device.configure()
    assert device.get_energy() == [two_gpu_api.domains_current_energy['nvidia_gpu_0'],
                                   two_gpu_api.domains_current_energy['nvidia_gpu_1']]


##################################
# CONFIGURE AND GET ENERGY TESTS #
##################################
def test_get_gpu0_energy_with_only_one_gpu_api_return_correct_value(one_gpu_api):
    """
    Create a NvidiaGpuDevice instance on a machine with one gpu
    configure it to monitor the gpu 0
    use the `get_energy` method and check if:
    - the returned list contains one element
    - this element is the energy consumption of the gpu 0
    """
    device = NvidiaGPUDevice()
    device.configure([NvidiaGPUDomain(0)])
    assert device.get_energy() == [one_gpu_api.domains_current_energy['nvidia_gpu_0']]


def test_get_gpu0_energy_with_two_gpu_api_return_correct_value(two_gpu_api):
    """
    Create a NvidiaGpuDevice instance on a machine with two gpu
    configure it to monitor the gpu 0
    use the `get_energy` method and check if:
    - the returned list contains one element
    - this element is the energy consumption of the gpu 0
    """
    device = NvidiaGPUDevice()
    device.configure([NvidiaGPUDomain(0)])
    assert device.get_energy() == [two_gpu_api.domains_current_energy['nvidia_gpu_0']]

def test_get_gpu0_and_gpu1_energy_with_two_gpu_api_return_correct_value(two_gpu_api):
    """
    Create a NvidiaGpuDevice instance on a machine with two gpu
    configure it to monitor the gpu 0 and gpu 1
    use the `get_energy` method and check if:
    - the returned list contains two elements
    - theses elements are the energy consumption of the gpu 0 and 1
    """
    device = NvidiaGPUDevice()
    device.configure([NvidiaGPUDomain(0), NvidiaGPUDomain(1)])
    assert device.get_energy() == [two_gpu_api.domains_current_energy['nvidia_gpu_0'],
                                   two_gpu_api.domains_current_energy['nvidia_gpu_1']]
