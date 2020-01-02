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

from pyJoules.energy_device.rapl_device import RaplDevice, RaplPackageDomain, RaplDramDomain, RaplCoreDomain
from pyJoules.energy_meter import EnergyMeter, EnergySample
from .. utils.rapl_fs import *


TIMESTAMP_TRACE = [1.1, 2.2, 3.3, 4.4, 5.5]

# @patch('pyJoules.energy_handler.EnergyHandler')
@patch('time.perf_counter', side_effect=TIMESTAMP_TRACE)
def test_measure_rapl_device_all_domains(_mocked_perf_counter, fs_pkg_dram_one_socket):
    meter = EnergyMeter([RaplPackageDomain(0), RaplDramDomain(0)])
    meter.start(tag="foo")
    meter.record(tag="bar")
    meter.stop()
    samples = meter.compute()
    ConsolePrinter.process(samples)

    sample = samples.get_sample("bar")
