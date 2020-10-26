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

from pyJoules.energy_trace import EnergyTrace, EnergySample


SAMPLE_1 = EnergySample('123', 'tag1', 10, {'domain1': 1, 'domain2': 2})
SAMPLE_2 = EnergySample('456', 'tag2', 20, {'domain2': 2, 'domain3': 3})

IDLE_1 = {'domain1': 1, 'domain2': 1}
IDLE_2 = {'domain2': 1, 'domain3': 2}

NEGATIVE_SAMPLE_1 = EnergySample('123', 'tag1', 10, {'domain1': -1, 'domain2': 2})
NEGATIVE_SAMPLE_2 = EnergySample('456', 'tag2', 20, {'domain2': 2, 'domain3': -3})


@pytest.fixture
def trace_with_one_sample():
    return EnergyTrace([SAMPLE_1])


@pytest.fixture
def trace_with_two_sample():
    return EnergyTrace([SAMPLE_1, SAMPLE_2])


@pytest.fixture
def negative_trace():
    return EnergyTrace([NEGATIVE_SAMPLE_1, NEGATIVE_SAMPLE_2])


@pytest.fixture
def semi_negative_trace():
    return EnergyTrace([SAMPLE_1, NEGATIVE_SAMPLE_2])


##########
# LENGTH #
##########
def test_length_of_zero_element_trace_is_zero():
    assert len(EnergyTrace([])) == 0
    

def test_length_of_one_element_trace_is_one(trace_with_one_sample):
    assert len(trace_with_one_sample)


def test_length_of_two_elements_trace_is_two(trace_with_two_sample):
    assert len(trace_with_two_sample)


##################
# LIST INTERFACE #
##################
def test_create_trace_with_one_sample_and_get_second_element_must_raise_IndexError(trace_with_one_sample):
    with pytest.raises(IndexError):
        trace_with_one_sample[1]


def test_create_trace_with_one_sample_and_get_first_element_must_return_first_element(trace_with_one_sample):
    assert trace_with_one_sample[0] == SAMPLE_1


def test_create_trace_with_two_sample_and_get_second_element_must_return_second_element(trace_with_two_sample):
    assert trace_with_two_sample[1] == SAMPLE_2


def test_create_a_trace_from_a_localy_defined_list_and_modify_the_list_musnt_modify_the_trace():
    locale_list = [SAMPLE_1]
    trace = EnergyTrace(locale_list)
    locale_list[0] = 0
    assert trace[0] != 0


def test_append_sample_to_a_trace_with_one_sample_create_a_trace_with_two_sample(trace_with_one_sample):
    trace_with_one_sample.append(SAMPLE_1)
    assert len(trace_with_one_sample) == 2


def test_append_sample_to_a_trace_with_one_sample_create_a_trace_with_two_correct_sample(trace_with_one_sample):
    trace_with_one_sample.append(SAMPLE_2)
    assert trace_with_one_sample[0] == SAMPLE_1
    assert trace_with_one_sample[1] == SAMPLE_2


def test_append_sample_to_a_trace_with_one_sample_create_a_trace_with_two_correct_sample(trace_with_one_sample):
    trace_with_one_sample.append(SAMPLE_2)
    assert trace_with_one_sample[0] == SAMPLE_1
    assert trace_with_one_sample[1] == SAMPLE_2


def test_add_two_trace_with_one_sample_produce_a_trace_of_length_two(trace_with_one_sample):
    assert len(trace_with_one_sample + trace_with_one_sample) == 2


def test_add_one_trace_with_one_sample_and_one_trace_with_two_sample_tproduce_a_trace_of_length_three(trace_with_one_sample, trace_with_two_sample):
    assert len(trace_with_one_sample + trace_with_two_sample) == 3


def test_add_two_trace_with_one_sample_produce_a_trace_with_correct_values(trace_with_one_sample):
    trace = trace_with_one_sample + trace_with_one_sample
    assert trace[0] == SAMPLE_1
    assert trace[1] == SAMPLE_1


def test_add_one_trace_with_one_sample_and_one_trace_with_two_sample_tproduce_a_trace_with_correct_values(trace_with_one_sample, trace_with_two_sample):
    trace = trace_with_one_sample + trace_with_two_sample
    assert trace[0] == SAMPLE_1
    assert trace[1] == SAMPLE_1
    assert trace[2] == SAMPLE_2


def test_iadd_a_trace_with_one_sample_to_a_trace_with_one_sample_create_a_trace_with_two_sample(trace_with_one_sample):
    trace_with_one_sample += trace_with_one_sample
    assert len(trace_with_one_sample) == 2


def test_iadd_a_trace_with_one_sample_to_a_trace_with_one_sample_create_a_trace_with_two_correct_sample(trace_with_one_sample):
    trace_with_one_sample += trace_with_one_sample
    assert trace_with_one_sample[0] == SAMPLE_1
    assert trace_with_one_sample[1] == SAMPLE_1


def test_iadd_a_trace_with_two_sample_to_a_trace_with_one_sample_create_a_trace_with_three_sample(trace_with_one_sample, trace_with_two_sample):
    trace_with_one_sample += trace_with_two_sample
    assert len(trace_with_one_sample) == 3


def test_iadd_a_trace_with_two_sample_to_a_trace_with_one_sample_create_a_trace_with_three_correct_sample(trace_with_one_sample, trace_with_two_sample):
    trace_with_one_sample += trace_with_two_sample
    assert trace_with_one_sample[0] == SAMPLE_1
    assert trace_with_one_sample[1] == SAMPLE_1
    assert trace_with_one_sample[2] == SAMPLE_2

##################
# DICT INTERFACE #
##################
def test_create_trace_with_one_sample_and_get_bad_tag_must_raise_KeyError(trace_with_one_sample):
    with pytest.raises(KeyError):
        trace_with_one_sample['bad_tag']


def test_create_trace_with_one_sample_and_get_tag_of_the_first_element_must_return_first_element(trace_with_one_sample):
    assert trace_with_one_sample['tag1'] == SAMPLE_1


def test_create_trace_with_two_sample_and_get_tag_of_the_second_element_must_return_second_element(trace_with_two_sample):
    assert trace_with_two_sample['tag2'] == SAMPLE_2


def test_create_trace_with_one_sample_and_use_in_keyword_to_check_if_tag_is_present_return_true(trace_with_one_sample):
    assert 'tag1' in trace_with_one_sample


def test_create_trace_with_one_sample_and_use_in_keyword_to_check_if_bad_tag_is_present_return_false(trace_with_one_sample):
    assert not 'bad_tag' in trace_with_one_sample


def test_get_sample_on_a_two_sample_trace_with_same_names_return_first_sample():
    s1 = EnergySample('123', 'tag1', 10, {'domain1': 1, 'domain2': 2})
    s2 = EnergySample('456', 'tag1', 20, {'domain2': 2, 'domain3': 3})

    trace = EnergyTrace([s1, s2])

    assert trace['tag1'] == s1


###########
# ITERATE #
###########
def test_create_trace_with_one_sample_and_iter_on_it_must_iter_on_one_element(trace_with_one_sample):
    l = []
    for s in trace_with_one_sample:
        l.append(s)
    assert l[0] == SAMPLE_1

def test_create_trace_with_two_sample_and_iter_on_it_must_iter_on_two_elements(trace_with_two_sample):
    l = []
    for s in trace_with_two_sample:
        l.append(s)
    assert l[0] == SAMPLE_1
    assert l[1] == SAMPLE_2


###############
# REMOVE_IDLE #
###############
def test_create_trace_with_two_element_and_remove_idle_with_one_value_must_raise_ValueError(trace_with_two_sample):
    with pytest.raises(ValueError):
        trace_with_two_sample.remove_idle([IDLE_1])


def test_create_trace_with_two_element_and_remove_idle_with_three_value_must_raise_ValueError(trace_with_two_sample):
    with pytest.raises(ValueError):
        trace_with_two_sample.remove_idle([IDLE_1, IDLE_1, IDLE_2])


def test_create_trace_with_two_element_and_remove_idle_with_value_with_bad_tag_must_raise_ValueError(trace_with_two_sample):
    with pytest.raises(ValueError):
        trace_with_two_sample.remove_idle([IDLE_2, IDLE_1])


def test_create_trace_with_two_element_and_remove_idle_must_return_good_values(trace_with_two_sample):
    trace_with_two_sample.remove_idle([IDLE_1, IDLE_2])
    assert trace_with_two_sample[0].energy['domain1'] == 0
    assert trace_with_two_sample[0].energy['domain2'] == 1
    assert trace_with_two_sample[1].energy['domain2'] == 1
    assert trace_with_two_sample[1].energy['domain3'] == 1


##############
# CLEAN_DATA #
##############
def test_clean_trace_without_negative_value_must_return_the_same_trace(trace_with_two_sample):
    trace_with_two_sample.clean_data()
    assert len(trace_with_two_sample) == 2


def test_create_trace_with_two_element_with_negative_energy_values_and_clean_data_must_remove_all_elements(negative_trace):
    negative_trace.clean_data()
    assert len(negative_trace) == 0


def test_create_trace_with_two_element_with_one_element_with_negative_energy_values_and_clean_data_must_remove_one_element(semi_negative_trace):
    semi_negative_trace.clean_data()
    assert len(semi_negative_trace) == 1
    assert semi_negative_trace[0] == SAMPLE_1


def test_clean_with_guard_a_trace_without_negative_sample_but_a_bad_sample_must_remove_this_sample(trace_with_two_sample):
    trace_with_two_sample.clean_data(guards=[lambda sample: False if 'domain3' in sample.energy else True])
    assert len(trace_with_two_sample) == 1
    assert trace_with_two_sample[0] == SAMPLE_1


def test_clean_with_guard_a_trace_without_negative_sample_but_two_bad_sample_must_remove_all_samples(trace_with_two_sample):
    trace_with_two_sample.clean_data(guards=[lambda sample: False if 'domain2' in sample.energy else True])
    assert len(trace_with_two_sample) == 0


def test_clean_with_guard_a_trace_with_a_negative_and_bad_sample_must_remove_this_samples():
    trace = EnergyTrace([SAMPLE_1, NEGATIVE_SAMPLE_2])
    trace.clean_data(guards=[lambda sample: False if 'domain3' in sample.energy else True])
    assert len(trace) == 1
    assert trace[0] == SAMPLE_1

def test_clean_with_guard_a_trace_with_a_negative_sample_and_a_bad_sample_must_remove_all_samples():
    trace = EnergyTrace([SAMPLE_1, NEGATIVE_SAMPLE_2])
    trace.clean_data(guards=[lambda sample: False if 'domain1' in sample.energy else True])
    assert len(trace) == 0
