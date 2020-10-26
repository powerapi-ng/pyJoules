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

"""
Test to measure energy consumption of a trace only with the energy meter
"""
import pytest

from mock import patch
from pyJoules.device import DeviceFactory
from pyJoules.device.rapl_device import RaplDevice, RaplPackageDomain, RaplDramDomain
from pyJoules.device.nvidia_device import NvidiaGPUDevice, NvidiaGPUDomain
from pyJoules.energy_meter import EnergyMeter
from ..utils.rapl_fs import fs_pkg_dram_one_socket
from ..utils.fake_nvidia_api import one_gpu_api
from ..utils.fake_api import CorrectTrace
from ..utils.sample import assert_sample_are_equals


# We mock time.time function that is used by pyfakefs each time an operation on filesystem is done. we have to give
# consistant time return value to time.time that will be used by pyfakefs
INIT_TS = [0] * 5
FIRST_TS = [1.1] * 7
SECOND_TS = [2.2] * 7
THIRD_TS = [3.3] * 7
MOCKED_TIMESTAMP_TRACE = INIT_TS + FIRST_TS + SECOND_TS + THIRD_TS
TIMESTAMP_TRACE = [1.1, 2.2, 3.3]


@patch('time.time', side_effect=MOCKED_TIMESTAMP_TRACE)
def test_measure_rapl_device_all_domains(_mocked_time_ns, fs_pkg_dram_one_socket, one_gpu_api):
    domains = [RaplPackageDomain(0), RaplDramDomain(0), NvidiaGPUDomain(0)]

    correct_trace = CorrectTrace(domains, [fs_pkg_dram_one_socket, one_gpu_api], TIMESTAMP_TRACE)  # test

    rapl = RaplDevice()
    rapl.configure(domains=[RaplPackageDomain(0), RaplDramDomain(0)])

    nvidia = NvidiaGPUDevice()
    nvidia.configure(domains=[NvidiaGPUDomain(0)])

    meter = EnergyMeter([rapl, nvidia])

    correct_trace.add_new_sample('foo')  # test
    meter.start(tag="foo")

    correct_trace.add_new_sample('bar')  # test
    meter.record(tag="bar")

    correct_trace.add_new_sample('')  # test
    meter.stop()

    for sample1, sample2 in zip(correct_trace, meter.get_trace()):  # test
        assert_sample_are_equals(sample1, sample2)  # test


@patch('time.time', side_effect=MOCKED_TIMESTAMP_TRACE)
def test_measure_rapl_device_all_domains_configuration_with_factory(_mocked_time_ns, fs_pkg_dram_one_socket, one_gpu_api):
    domains = [RaplPackageDomain(0), RaplDramDomain(0), NvidiaGPUDomain(0)]

    correct_trace = CorrectTrace(domains, [fs_pkg_dram_one_socket, one_gpu_api], TIMESTAMP_TRACE)  # test

    devices = DeviceFactory.create_devices(domains)

    meter = EnergyMeter(devices)

    correct_trace.add_new_sample('foo')  # test
    meter.start(tag="foo")

    correct_trace.add_new_sample('bar')  # test
    meter.record(tag="bar")

    correct_trace.add_new_sample('')  # test
    meter.stop()

    for sample1, sample2 in zip(correct_trace, meter.get_trace()):  # test
        assert_sample_are_equals(sample1, sample2)  # test


INIT_TS2 = [0] * 9
MOCKED_TIMESTAMP_TRACE2 = INIT_TS2 + FIRST_TS + SECOND_TS + THIRD_TS

@patch('time.time', side_effect=MOCKED_TIMESTAMP_TRACE2)
def test_measure_rapl_device_all_domains_configuration_with_factory_with_default_values(_mocked_time_ns, fs_pkg_dram_one_socket, one_gpu_api):
    domains = [RaplPackageDomain(0), RaplDramDomain(0), NvidiaGPUDomain(0)]

    correct_trace = CorrectTrace(domains, [fs_pkg_dram_one_socket, one_gpu_api], TIMESTAMP_TRACE)  # test

    devices = DeviceFactory.create_devices()

    meter = EnergyMeter(devices)

    correct_trace.add_new_sample('foo')  # test
    meter.start(tag="foo")

    correct_trace.add_new_sample('bar')  # test
    meter.record(tag="bar")

    correct_trace.add_new_sample('')  # test
    meter.stop()

    for sample1, sample2 in zip(correct_trace, meter.get_trace()):  # test
        assert_sample_are_equals(sample1, sample2)  # test
