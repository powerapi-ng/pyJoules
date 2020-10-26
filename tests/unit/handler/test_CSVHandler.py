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
import pyfakefs
import os.path

from pyJoules.handler.csv_handler import CSVHandler
from pyJoules.handler import UnconsistantSamplesError
from pyJoules.energy_trace import EnergySample, EnergyTrace


@pytest.fixture
def non_writable_folder(fs):
    """
    A filesystem with a /dir directory that is not writable
    """
    fs.create_dir('/dir', perm_bits=000)
    return fs


@pytest.fixture
def sample1():
    return EnergySample(1, 'sample1', 2, {'d1': 1, 'd2': 2})


@pytest.fixture
def sample2():
    return EnergySample(2, 'sample2', 3, {'d1': 3, 'd2': 4})


@pytest.fixture
def bad_sample():
    return EnergySample(2, 'sample2', 3, {'d1': 3, 'd3': 4})


@pytest.fixture
def bad_trace(bad_sample):
    return EnergyTrace([bad_sample])


@pytest.fixture
def trace1(sample1):
    return EnergyTrace([sample1])


@pytest.fixture
def trace2(sample1, sample2):
    return EnergyTrace([sample1, sample2])


def test_record_data_on_non_writable_file_raise_IOError(non_writable_folder, trace1):
    handler = CSVHandler('/dir/file.csv')
    handler.process(trace1)
    with pytest.raises(IOError):
        handler.save_data()


def test_record_trace_with_unconsistent_sample_raise_UnconsistantSamplesError(fs, trace1, bad_trace):
    handler = CSVHandler('/file.csv')
    handler.process(trace1)
    handler.process(bad_trace)
    with pytest.raises(UnconsistantSamplesError):
        handler.save_data()


def test_record_trace_with_unconsistent_sample_must_not_write_in_file(fs, trace1, bad_trace):
    handler = CSVHandler('/file.csv')
    handler.process(trace1)
    handler.process(bad_trace)
    try:
        handler.save_data()
    except UnconsistantSamplesError:
        pass
    assert not os.path.exists('/file.csv')

def test_process_one_trace_and_record_produce_a_file_with_one_correct_line(fs, trace1):
    handler = CSVHandler('/file.csv')
    handler.process(trace1)
    handler.save_data()

    assert os.path.exists('/file.csv')
    with open('/file.csv', 'r') as csv:
        lines = []
        for line in csv:
            lines.append(line)

        assert len(lines) == 2
        assert lines[0] == 'timestamp;tag;duration;d1;d2\n'
        assert lines[1] == '1;sample1;2;1;2\n'


def test_process_two_trace_and_record_produce_a_file_with_two_correct_lines(fs, trace1):
    handler = CSVHandler('/file.csv')
    handler.process(trace1)
    handler.process(trace1)
    handler.save_data()

    assert os.path.exists('/file.csv')
    with open('/file.csv', 'r') as csv:
        lines = []
        for line in csv:
            lines.append(line)

        assert len(lines) == 3
        assert lines[0] == 'timestamp;tag;duration;d1;d2\n'
        assert lines[1] == '1;sample1;2;1;2\n'
        assert lines[2] == '1;sample1;2;1;2\n'


def test_process_one_trace_with_one_sample_and_one_trace_with_two_sample_and_record_produce_a_file_with_three_correct_lines(fs, trace1, trace2):
    handler = CSVHandler('/file.csv')
    handler.process(trace1)
    handler.process(trace2)
    handler.save_data()

    assert os.path.exists('/file.csv')
    with open('/file.csv', 'r') as csv:
        lines = []
        for line in csv:
            lines.append(line)

        assert len(lines) == 4
        assert lines[0] == 'timestamp;tag;duration;d1;d2\n'
        assert lines[1] == '1;sample1;2;1;2\n'
        assert lines[2] == '1;sample1;2;1;2\n'
        assert lines[3] == '2;sample2;3;3;4\n'


def test_process_one_trace_and_record_in_existing_file_only_append_one_correct_line(fs, trace1):
    fs.create_file('/file.csv', contents='timestamp;tag;duration;d1;d2\n1;sample1;2;1;2\n')

    handler = CSVHandler('/file.csv')
    handler.process(trace1)
    handler.save_data()

    assert os.path.exists('/file.csv')
    with open('/file.csv', 'r') as csv:
        lines = []
        for line in csv:
            lines.append(line)

        assert len(lines) == 3
        assert lines[0] == 'timestamp;tag;duration;d1;d2\n'
        assert lines[1] == '1;sample1;2;1;2\n'
        assert lines[1] == '1;sample1;2;1;2\n'
