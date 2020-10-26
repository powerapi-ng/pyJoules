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

from pyJoules.device.rapl_device import RaplDevice, RaplPackageDomain, RaplDramDomain
from pyJoules.device.nvidia_device import NvidiaGPUDomain
from pyJoules.energy_meter import EnergyMeter, EnergyContext
from pyJoules.handler.csv_handler import CSVHandler
from .. utils.rapl_fs import fs_pkg_dram_one_socket
from ..utils.fake_nvidia_api import one_gpu_api
from .. utils.fake_api import CorrectTrace
from ..utils.sample import assert_sample_are_equals


# We mock time.time function that is used by pyfakefs each time an operation on filesystem is done. we have to give
# consistant time return value to time.time that will be used by pyfakefs
FIRST_TS = [1.1] * 12
SECOND_TS = [2.2] * 7
THIRD_TS = [3.3] * 7
CSV_WRITING_TS = [1] * 3
MOCKED_TIMESTAMP_TRACE = FIRST_TS + SECOND_TS + THIRD_TS + CSV_WRITING_TS
TIMESTAMP_TRACE = [1.1, 2.2, 3.3]

@patch('time.time', side_effect=MOCKED_TIMESTAMP_TRACE)
@patch('pyJoules.handler.EnergyHandler')
def test_measure_rapl_device_all_domains(mocked_handler, _mocked_time, fs_pkg_dram_one_socket, one_gpu_api):
    print('init--------------')
    domains = [RaplPackageDomain(0), RaplDramDomain(0), NvidiaGPUDomain(0)]

    correct_trace = CorrectTrace(domains, [fs_pkg_dram_one_socket, one_gpu_api], TIMESTAMP_TRACE)  # test


    csv_handler = CSVHandler('result.csv')
    print('1--------------')
    correct_trace.add_new_sample('foo')
    with EnergyContext(handler=csv_handler, domains=domains, start_tag='foo') as ctx:
        print('2--------------')
        correct_trace.add_new_sample('bar')
        ctx.record(tag='bar')
        print('3--------------')
        correct_trace.add_new_sample('')
    print('save--------------')
    print(csv_handler.traces)
    csv_handler.save_data()
    print('test--------------')
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


    assert float(lines[2][0]) == TIMESTAMP_TRACE[1]
    assert lines[2][1] == 'bar'
    assert float(lines[2][2]) == TIMESTAMP_TRACE[2] - TIMESTAMP_TRACE[1]
    correct_sample = correct_trace.get_trace()[1]

    for key in correct_sample.energy:
        assert key in lines[0]
        assert correct_sample.energy[key] == float(lines[2][lines[0].index(key)])
