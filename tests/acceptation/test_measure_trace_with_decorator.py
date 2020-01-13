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

from pyJoules.energy_device.rapl_device import RaplDevice, RaplPackageDomain, RaplDramDomain
from pyJoules.energy_meter import EnergyMeter, measureit
from pyJoules.energy_device.nvidia_device import NvidiaGPUDomain
from .. utils.rapl_fs import fs_pkg_dram_one_socket
from ..utils.fake_nvidia_api import one_gpu_api
from .. utils.fake_api import CorrectTrace
from ..utils.sample import assert_sample_are_equals

TIMESTAMP_TRACE = [1.1, 2.2, 3.3, 4.4, 5.5]

@patch('pyJoules.energy_handler.EnergyHandler')
@patch('time.perf_counter', side_effect=TIMESTAMP_TRACE)
def test_measure_rapl_device_all_domains(mocked_handler, _mocked_perf_counter, fs_pkg_dram_one_socket, one_gpu_api):

    domains = [RaplPackageDomain(0), RaplDramDomain(0), NvidiaGPUDomain(0)]

    correct_trace = CorrectTrace(domains, [fs_pkg_dram_one_socket, one_gpu_api], TIMESTAMP_TRACE)  # test

    @measureit(handler=mocked_handler, domains=domains)
    def measured_function(val):
        correct_trace.add_new_sample('measured_function')  # test
        return val + 1

    assert mocked_handler.process.call_count == 0   # test
    returned_value = measured_function(1)
    assert mocked_handler.process.call_count == 1   # test

    assert returned_value == 2

    for correct_sample, processed_arg in zip(correct_trace, mocked_handler.process.call_args_list):  # test
        measured_sample = processed_arg[0][0]  # test
        assert_sample_are_equals(correct_sample, measured_sample)  # test
