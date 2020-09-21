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
import pandas

from pyJoules.energy_handler import PandasHandler, NoSampleProcessedError, UnconsistantSamplesError
from pyJoules import EnergySample


@pytest.fixture
def sample1():
    return EnergySample(1, 'sample1', 2, {'d1': 1, 'd2': 2})


@pytest.fixture
def sample2():
    return EnergySample(2, 'sample2', 3, {'d1': 3, 'd2': 4})

@pytest.fixture
def bad_sample():
    return EnergySample(2, 'toto', 3, {'d3': 3})


def test_create_a_pandas_handler_and_get_dataframe_must_raise_NoSampleProcessedError():
    handler = PandasHandler()
    with pytest.raises(NoSampleProcessedError):
        df = handler.get_dataframe()


def test_process_one_sample_and_get_dataframe_must_return_dataframe_of_len_1(sample1):
    handler = PandasHandler()
    handler.process(sample1)
    df = handler.get_dataframe()
    assert len(df) == 1


def test_process_two_sample_and_get_dataframe_must_return_dataframe_of_len_2(sample1, sample2):
    handler = PandasHandler()
    handler.process(sample1)
    handler.process(sample2)
    df = handler.get_dataframe()
    assert len(df) == 2


def test_process_sample_and_get_dataframe_must_return_good_column_names(sample1):
    handler = PandasHandler()
    handler.process(sample1)
    df = handler.get_dataframe()
    assert df.columns[0] == 'timestamp'
    assert df.columns[1] == 'tag'
    assert df.columns[2] == 'duration'

    i = 3
    for domain_name in sample1.energy:
        assert df.columns[i] == domain_name
        i += 1

def test_process_sample_and_get_dataframe_must_return_good_values(sample1):
    handler = PandasHandler()
    handler.process(sample1)
    df = handler.get_dataframe()
    df['timestamp'][0] == sample1.timestamp
    df['tag'][0] == sample1.tag
    df['duration'][0] == sample1.duration

    for domain_name in sample1.energy:
        assert df[domain_name][0] == sample1.energy[domain_name]


def test_process_two_sample_and_get_dataframe_must_return_good_values_for_second_sample(sample1, sample2):
    handler = PandasHandler()
    handler.process(sample1)
    handler.process(sample2)
    df = handler.get_dataframe()
    df['timestamp'][1] == sample2.timestamp
    df['tag'][1] == sample2.tag
    df['duration'][1] == sample2.duration

    for domain_name in sample2.energy:
        assert df[domain_name][1] == sample2.energy[domain_name]


def test_process_two_different_sample_and_get_dataframe_must_raise_UnconsistantSamplesError(sample1, bad_sample):
    handler = PandasHandler()
    handler.process(sample1)
    handler.process(bad_sample)
    with pytest.raises(UnconsistantSamplesError):
        df = handler.get_dataframe()
