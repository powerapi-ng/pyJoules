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
decorate a function and measure its energy consumption, output the energy consumption in a csv file
"""
import pytest
from mock import patch

from pyJoules.device.rapl_device import RaplDevice, RaplPackageDomain, RaplDramDomain
from pyJoules.energy_meter import EnergyMeter, measure_energy
from pyJoules.device.nvidia_device import NvidiaGPUDomain
from pyJoules.handler.csv_handler import CSVHandler
from .. utils.rapl_fs import fs_pkg_dram_one_socket
from ..utils.fake_nvidia_api import one_gpu_api
from .. utils.fake_api import CorrectTrace
from ..utils.sample import assert_sample_are_equals


# We mock time.time function that is used by pyfakefs each time an operation on filesystem is done. we have to give
# consistant time return value to time.time that will be used by pyfakefs
INIT_TS = [0] * 5
FIRST_TS = [1.1] * 7
SECOND_TS = [2.2] * 7
CSV_WRITING_TS = [1, 2, 3, 5, 6, 7, 8, 9]
MOCKED_TIMESTAMP_TRACE = INIT_TS + FIRST_TS + SECOND_TS + CSV_WRITING_TS
TIMESTAMP_TRACE = [1.1, 2.2]


@patch('time.time', side_effect=MOCKED_TIMESTAMP_TRACE)
def test_measure_rapl_device_all_domains(_mocked_time, fs_pkg_dram_one_socket, one_gpu_api):
    domains = [RaplPackageDomain(0), RaplDramDomain(0), NvidiaGPUDomain(0)]
    correct_trace = CorrectTrace(domains, [fs_pkg_dram_one_socket, one_gpu_api], TIMESTAMP_TRACE)

    csv_handler = CSVHandler('result.csv')
    @measure_energy(handler=csv_handler, domains=domains)
    def foo():
        correct_trace.add_new_sample('stop')
        return 1
    correct_trace.add_new_sample('begin')
    foo()
    csv_handler.save_data()
    csv_file = open('result.csv', 'r')

    lines = []

    for line in csv_file:
        lines.append(line.strip().split(';'))
    assert float(lines[1][0]) == TIMESTAMP_TRACE[0]
    assert lines[1][1] == 'foo'
    assert float(lines[1][2]) == TIMESTAMP_TRACE[1] - TIMESTAMP_TRACE[0]
    correct_sample = correct_trace.get_trace()[0]

    for key in correct_sample.energy:
        assert key in lines[0]
        assert correct_sample.energy[key] == float(lines[1][lines[0].index(key)])
