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

from pyJoules.handler.mongo_handler import trace_to_dict
from pyJoules.energy_trace import EnergySample

@pytest.fixture
def sample1():
    return EnergySample(1, 'sample1', 2, {'d1': 1, 'd2': 2})


@pytest.fixture
def sample2():
    return EnergySample(2, 'sample2', 3, {'d1': 3, 'd2': 4})


def test_converting_trace_list_to_dict_must_return_dict_good_name(sample1):
    d = trace_to_dict([sample1], 'trace1')
    assert d['name'] == 'trace1'


def test_converting_empty_list_to_dict_must_return_dict_with_empty_trace():
    d = trace_to_dict([], 'trace1')
    assert d['trace'] == []


def test_converting_one_trace_sample_to_dict_must_return_dict_with_one_sample(sample1):
    d = trace_to_dict([sample1], 'trace1')
    assert len(d['trace']) == 1


def test_converting_one_trace_sample_to_dict_must_return_dict_with_correct_values(sample1):
    d = trace_to_dict([sample1], 'trace1')
    assert d['trace'][0]['timestamp'] == sample1.timestamp
    assert d['trace'][0]['tag'] == sample1.tag
    assert d['trace'][0]['duration'] == sample1.duration
    assert d['trace'][0]['energy'] == sample1.energy


def test_converting_two_trace_sample_to_dict_must_return_dict_with_two_samples(sample1, sample2):
    d = trace_to_dict([sample1, sample2], 'trace1')
    assert len(d['trace']) == 2


def test_converting_two_trace_sample_to_dict_must_return_dict_with_correct_values(sample1, sample2):
    d = trace_to_dict([sample1, sample2], 'trace1')

    assert d['trace'][0]['timestamp'] == sample1.timestamp
    assert d['trace'][0]['tag'] == sample1.tag
    assert d['trace'][0]['duration'] == sample1.duration
    assert d['trace'][0]['energy'] == sample1.energy

    assert d['trace'][1]['timestamp'] == sample2.timestamp
    assert d['trace'][1]['tag'] == sample2.tag
    assert d['trace'][1]['duration'] == sample2.duration
    assert d['trace'][1]['energy'] == sample2.energy
