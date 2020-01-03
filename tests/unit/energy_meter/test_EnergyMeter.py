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

from mock import patch

from pyJoules.energy_meter import EnergyMeter, EnergySample
from pyJoules.energy_meter import EnergyMeterNotStartedError, EnergyMeterNotStoppedError, SampleNotFoundError
from pyJoules.energy_device import EnergyDevice, EnergyDomain
from ...utils.sample import assert_sample_are_equals

DEVICE1_ENERGY_TRACE = [[1.0, 1.1],
                        [2.0, 2.2],
                        [3.0, 3.4],
                        [4.0, 4.6],
                        [5.0, 5.8]]

DEVICE2_ENERGY_TRACE = [[4.0],
                        [6.2],
                        [8.0],
                        [10.3],
                        [11.123]]

TIMESTAMP_TRACE = [1.1, 2.2, 3.3, 4.4, 5.5]


class EnergyDomainDevice1Domain1(EnergyDomain):
    def __repr__(self):
        return 'device1_domain1'


class EnergyDomainDevice1Domain2(EnergyDomain):
    def __repr__(self):
        return 'device1_domain2'


class EnergyDomainDevice2Domain1(EnergyDomain):
    def __repr__(self):
        return 'device2_domain1'


class MockedEnergyDevice1(EnergyDevice):

    def __init__(self):
        EnergyDevice.__init__(self)
        self.iterator = DEVICE1_ENERGY_TRACE.__iter__()

    @staticmethod
    def available_domains():
        return [EnergyDomainDevice1Domain1(), EnergyDomainDevice1Domain2()]

    def configure(self, domains=None):
        EnergyDevice.configure(self, domains)

    def get_energy(self):
        return self.iterator.__next__()


class MockedEnergyDevice2(EnergyDevice):

    def __init__(self):
        EnergyDevice.__init__(self)
        self.iterator = DEVICE2_ENERGY_TRACE.__iter__()

    @staticmethod
    def available_domains():
        return [EnergyDomainDevice2Domain1()]

    def configure(self, domains=None):
        EnergyDevice.configure(self, domains)

    def get_energy(self):
        return self.iterator.__next__()


@pytest.fixture
def energy_meter():
    device1 = MockedEnergyDevice1()
    device1.configure()
    device2 = MockedEnergyDevice2()
    device2.configure()
    return EnergyMeter([device1, device2])


############################
# NON STARTED ERRORS TESTS #
############################
def test_record_on_non_started_energy_meter_raise_EnergyMeterNotStartedError(energy_meter):
    with pytest.raises(EnergyMeterNotStartedError):
        energy_meter.record()


def test_stop_a_non_started_energy_meter_raise_EnergyMeterNotStartedError(energy_meter):
    with pytest.raises(EnergyMeterNotStartedError):
        energy_meter.stop()


def test_iter_on_a_non_started_energy_meter_raise_EnergyMeterNotStartedError(energy_meter):
    with pytest.raises(EnergyMeterNotStartedError):
        energy_meter.__iter__()


def test_get_sample_on_a_non_started_energy_meter_raise_EnergyMeterNotStartedError(energy_meter):
    with pytest.raises(EnergyMeterNotStartedError):
        energy_meter.get_sample('toto')


############################
# NON STOPPED ERRORS TESTS #
############################
def test_iter_on_a_non_stopped_energy_meter_raise_EnergyMeterNotStoppedError(energy_meter):
    energy_meter.start()
    with pytest.raises(EnergyMeterNotStoppedError):
        energy_meter.__iter__()


def test_get_sample_on_a_non_stopped_energy_meter_raise_EnergyMeterNotStopdError(energy_meter):
    energy_meter.start()
    with pytest.raises(EnergyMeterNotStoppedError):
        energy_meter.get_sample('toto')


####################
# GET ENERGY TRACE #
####################
def test_iter_on_one_sample_trace_should_return_one_sample(energy_meter):
    energy_meter.start()
    energy_meter.stop()
    samples = []

    for sample in energy_meter:
        samples.append(sample)

    assert len(samples) == 1


@pytest.fixture
def sample1():
    ts = TIMESTAMP_TRACE[0]
    tag = ''
    duration = TIMESTAMP_TRACE[1] - TIMESTAMP_TRACE[0]
    energy = {str(EnergyDomainDevice1Domain1()): DEVICE1_ENERGY_TRACE[1][0] - DEVICE1_ENERGY_TRACE[0][0],
              str(EnergyDomainDevice1Domain2()): DEVICE1_ENERGY_TRACE[1][1] - DEVICE1_ENERGY_TRACE[0][1],
              str(EnergyDomainDevice2Domain1()): DEVICE2_ENERGY_TRACE[1][0] - DEVICE2_ENERGY_TRACE[0][0]}
    return EnergySample(ts, tag, duration, energy)


@pytest.fixture
def sample2():
    ts = TIMESTAMP_TRACE[1]
    tag = ''
    duration = TIMESTAMP_TRACE[2] - TIMESTAMP_TRACE[1]
    energy = {str(EnergyDomainDevice1Domain1()): DEVICE1_ENERGY_TRACE[2][0] - DEVICE1_ENERGY_TRACE[1][0],
              str(EnergyDomainDevice1Domain2()): DEVICE1_ENERGY_TRACE[2][1] - DEVICE1_ENERGY_TRACE[1][1],
              str(EnergyDomainDevice2Domain1()): DEVICE2_ENERGY_TRACE[2][0] - DEVICE2_ENERGY_TRACE[1][0]}
    return EnergySample(ts, tag, duration, energy)


@pytest.fixture
def sample3():
    ts = TIMESTAMP_TRACE[3]
    tag = ''
    duration = TIMESTAMP_TRACE[4] - TIMESTAMP_TRACE[3]
    energy = {str(EnergyDomainDevice1Domain1()): DEVICE1_ENERGY_TRACE[4][0] - DEVICE1_ENERGY_TRACE[3][0],
              str(EnergyDomainDevice1Domain2()): DEVICE1_ENERGY_TRACE[4][1] - DEVICE1_ENERGY_TRACE[3][1],
              str(EnergyDomainDevice2Domain1()): DEVICE2_ENERGY_TRACE[4][0] - DEVICE2_ENERGY_TRACE[3][0]}
    return EnergySample(ts, tag, duration, energy)


@patch('time.perf_counter', side_effect=TIMESTAMP_TRACE)
def test_iter_on_one_sample_trace_should_return_correct_values(_mocked_fun, energy_meter, sample1):
    energy_meter.start()
    energy_meter.stop()
    samples = []

    for sample in energy_meter:
        assert_sample_are_equals(sample, sample1)


@patch('time.perf_counter', side_effect=TIMESTAMP_TRACE)
def test_iter_on_two_sample_trace_should_return_two_sample(_mocked_fun, energy_meter):
    energy_meter.start()
    energy_meter.record()
    energy_meter.stop()

    samples = []
    for sample in energy_meter:
        samples.append(sample)

    assert len(samples) == 2


@patch('time.perf_counter', side_effect=TIMESTAMP_TRACE)
def test_iter_on_two_sample_trace_should_return_correct_values(_mocked_fun, energy_meter, sample1, sample2):
    energy_meter.start()
    energy_meter.record()
    energy_meter.stop()

    for sample, correct_sample in zip(energy_meter, [sample1, sample2]):
        assert_sample_are_equals(sample, correct_sample)


@patch('time.perf_counter', side_effect=TIMESTAMP_TRACE)
def test_get_sample_on_a_one_sample_trace_return_correct_values(_mocked_fun, energy_meter, sample1):
    energy_meter.start()
    energy_meter.stop()
    assert_sample_are_equals(energy_meter.get_sample(''), sample1)


@patch('time.perf_counter', side_effect=TIMESTAMP_TRACE)
def test_get_sample_on_a_two_sample_trace_with_same_names_return_first_sample(_mocked_fun, energy_meter, sample1):
    energy_meter.start()
    energy_meter.record()
    energy_meter.stop()

    assert_sample_are_equals(energy_meter.get_sample(''), sample1)


@patch('time.perf_counter', side_effect=TIMESTAMP_TRACE)
def test_get_sample_by_their_names_return_correct_samples(_mocked_fun, energy_meter, sample1, sample2):
    energy_meter.start('sample1')
    energy_meter.record('sample2')
    energy_meter.stop()

    sample1.tag = 'sample1'
    sample2.tag = 'sample2'

    assert_sample_are_equals(energy_meter.get_sample('sample1'), sample1)
    assert_sample_are_equals(energy_meter.get_sample('sample2'), sample2)


def test_get_sample_that_does_not_exist_raise_SampleNotFoundError(energy_meter):
    energy_meter.start()
    energy_meter.stop()

    with pytest.raises(SampleNotFoundError):
        energy_meter.get_sample('sample1')


@patch('time.perf_counter', side_effect=TIMESTAMP_TRACE)
def test_second_start_on_an_energy_meter_should_restart_the_trace(_mocked_fun, energy_meter, sample3):
    energy_meter.start()
    energy_meter.record()
    energy_meter.stop()
    energy_meter.start()
    energy_meter.stop()

    samples = []
    for sample in energy_meter:
        samples.append(sample)

    assert len(samples) == 1
    assert_sample_are_equals(samples[0], sample3)


############
# TEST TAG #
############
def test_define_energy_meter_with_default_tag_create_sample_with_default_tag():

    device1 = MockedEnergyDevice1()
    device1.configure()
    device2 = MockedEnergyDevice2()
    device2.configure()
    meter = EnergyMeter([device1, device2], default_tag='tag')

    meter.start()
    meter.stop()

    sample = meter.get_sample('tag')
    assert sample.tag == 'tag'
