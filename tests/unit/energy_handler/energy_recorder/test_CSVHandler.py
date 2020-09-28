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

from pyJoules.energy_handler.energy_recorder.csv_handler import CSVHandler
from pyJoules import EnergySample


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


def test_record_data_on_non_writable_file_raise_IOError(non_writable_folder, sample1):
    handler = CSVHandler('/dir/file.csv')
    handler.process(sample1)
    with pytest.raises(IOError):
        handler.save_data()


def test_process_one_sample_and_record_produce_a_file_with_one_correct_line(fs, sample1):
    handler = CSVHandler('/file.csv')
    handler.process(sample1)
    handler.save_data()

    assert os.path.exists('/file.csv')
    with open('/file.csv', 'r') as csv:
        lines = []
        for line in csv:
            lines.append(line)

        assert len(lines) == 2
        assert lines[0] == 'timestamp;tag;duration;d1;d2\n'
        assert lines[1] == '1;sample1;2;1;2\n'


def test_process_two_sample_and_record_produce_a_file_with_two_correct_lines(fs, sample1, sample2):
    handler = CSVHandler('/file.csv')
    handler.process(sample1)
    handler.process(sample2)
    handler.save_data()

    assert os.path.exists('/file.csv')
    with open('/file.csv', 'r') as csv:
        lines = []
        for line in csv:
            lines.append(line)

        assert len(lines) == 3
        assert lines[0] == 'timestamp;tag;duration;d1;d2\n'
        assert lines[1] == '1;sample1;2;1;2\n'
        assert lines[2] == '2;sample2;3;3;4\n'

def test_process_one_sample_record_it_process_another_sample_and_record_it_produce_a_file_with_two_correct_lines(fs, sample1, sample2):
    handler = CSVHandler('/file.csv')
    handler.process(sample1)
    handler.save_data()
    handler.process(sample2)
    handler.save_data()

    assert os.path.exists('/file.csv')
    with open('/file.csv', 'r') as csv:
        lines = []
        for line in csv:
            lines.append(line)

        assert len(lines) == 3
        assert lines[0] == 'timestamp;tag;duration;d1;d2\n'
        assert lines[1] == '1;sample1;2;1;2\n'
        assert lines[2] == '2;sample2;3;3;4\n'


def test_process_one_sample_and_record_in_existing_file_only_append_one_correct_line(fs, sample2):
    fs.create_file('/file.csv', contents='timestamp;tag;duration;d1;d2\n1;sample1;2;1;2\n')

    handler = CSVHandler('/file.csv')
    handler.process(sample2)
    handler.save_data()

    assert os.path.exists('/file.csv')
    with open('/file.csv', 'r') as csv:
        lines = []
        for line in csv:
            lines.append(line)

        assert len(lines) == 3
        assert lines[0] == 'timestamp;tag;duration;d1;d2\n'
        assert lines[1] == '1;sample1;2;1;2\n'
        assert lines[2] == '2;sample2;3;3;4\n'
