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
from pyJoules.device import Device, Domain
from pyJoules.energy_trace import EnergyTrace
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

TIMESTAMP_TRACE = [1.1, 3.2, 3.3, 4.4, 5.5]


class DomainDevice1Domain1(Domain):
    def __repr__(self):
        return 'device1_domain1'


class DomainDevice1Domain2(Domain):
    def __repr__(self):
        return 'device1_domain2'


class DomainDevice2Domain1(Domain):
    def __repr__(self):
        return 'device2_domain1'


class MockedDevice1(Device):

    def __init__(self):
        Device.__init__(self)
        self.iterator = DEVICE1_ENERGY_TRACE.__iter__()

    @staticmethod
    def available_domains():
        return [DomainDevice1Domain1(), DomainDevice1Domain2()]

    def configure(self, domains=None):
        Device.configure(self, domains)

    def get_energy(self):
        return self.iterator.__next__()


class MockedDevice2(Device):

    def __init__(self):
        Device.__init__(self)
        self.iterator = DEVICE2_ENERGY_TRACE.__iter__()

    @staticmethod
    def available_domains():
        return [DomainDevice2Domain1()]

    def configure(self, domains=None):
        Device.configure(self, domains)

    def get_energy(self):
        return self.iterator.__next__()


@pytest.fixture
def energy_meter():
    device1 = MockedDevice1()
    device1.configure()
    device2 = MockedDevice2()
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


def test_resume_a_non_stoped_energy_meter_raise_EnergyMeterNotStoppedError(energy_meter):
    with pytest.raises(EnergyMeterNotStoppedError):
        energy_meter.start()
        energy_meter.resume()


####################
# TRACE GENERATION #
####################
@pytest.fixture
def sample1():
    ts = TIMESTAMP_TRACE[0]
    tag = ''
    duration = TIMESTAMP_TRACE[1] - TIMESTAMP_TRACE[0]
    energy = {str(DomainDevice1Domain1()): DEVICE1_ENERGY_TRACE[1][0] - DEVICE1_ENERGY_TRACE[0][0],
              str(DomainDevice1Domain2()): DEVICE1_ENERGY_TRACE[1][1] - DEVICE1_ENERGY_TRACE[0][1],
              str(DomainDevice2Domain1()): DEVICE2_ENERGY_TRACE[1][0] - DEVICE2_ENERGY_TRACE[0][0]}
    return EnergySample(ts, tag, duration, energy)


@pytest.fixture
def sample2():
    ts = TIMESTAMP_TRACE[1]
    tag = ''
    duration = TIMESTAMP_TRACE[2] - TIMESTAMP_TRACE[1]
    energy = {str(DomainDevice1Domain1()): DEVICE1_ENERGY_TRACE[2][0] - DEVICE1_ENERGY_TRACE[1][0],
              str(DomainDevice1Domain2()): DEVICE1_ENERGY_TRACE[2][1] - DEVICE1_ENERGY_TRACE[1][1],
              str(DomainDevice2Domain1()): DEVICE2_ENERGY_TRACE[2][0] - DEVICE2_ENERGY_TRACE[1][0]}
    return EnergySample(ts, tag, duration, energy)


@pytest.fixture
def sample2_5():
    ts = TIMESTAMP_TRACE[2]
    tag = ''
    duration = TIMESTAMP_TRACE[3] - TIMESTAMP_TRACE[2]
    energy = {str(DomainDevice1Domain1()): DEVICE1_ENERGY_TRACE[3][0] - DEVICE1_ENERGY_TRACE[2][0],
              str(DomainDevice1Domain2()): DEVICE1_ENERGY_TRACE[3][1] - DEVICE1_ENERGY_TRACE[2][1],
              str(DomainDevice2Domain1()): DEVICE2_ENERGY_TRACE[3][0] - DEVICE2_ENERGY_TRACE[2][0]}
    return EnergySample(ts, tag, duration, energy)


@pytest.fixture
def sample3():
    ts = TIMESTAMP_TRACE[3]
    tag = ''
    duration = TIMESTAMP_TRACE[4] - TIMESTAMP_TRACE[3]
    energy = {str(DomainDevice1Domain1()): DEVICE1_ENERGY_TRACE[4][0] - DEVICE1_ENERGY_TRACE[3][0],
              str(DomainDevice1Domain2()): DEVICE1_ENERGY_TRACE[4][1] - DEVICE1_ENERGY_TRACE[3][1],
              str(DomainDevice2Domain1()): DEVICE2_ENERGY_TRACE[4][0] - DEVICE2_ENERGY_TRACE[3][0]}
    return EnergySample(ts, tag, duration, energy)


def test_get_trace_on_a_non_stopped_energy_meter_raise_EnergyMeterNotStoppedError(energy_meter):
    energy_meter.start()
    with pytest.raises(EnergyMeterNotStoppedError):
        energy_meter.get_trace()


def test_get_trace_on_a_non_started_energy_meter_return_empty_trace(energy_meter):
        assert len(energy_meter.get_trace()) == 0


@patch('time.time', side_effect=TIMESTAMP_TRACE)
def test_start_and_stop_EnergyMeter_should_return_one_sample_trace(_mocked_fun, energy_meter):
    energy_meter.start()
    energy_meter.stop()

    assert len(energy_meter.get_trace()) == 1


@patch('time.time', side_effect=TIMESTAMP_TRACE)
def test_start_and_stop_EnergyMeter_should_return_correct_values(_mocked_fun, energy_meter, sample1):
    energy_meter.start()
    energy_meter.stop()

    for sample in energy_meter.get_trace():
        assert_sample_are_equals(sample, sample1)


@patch('time.time', side_effect=TIMESTAMP_TRACE)
def test_resume_and_stop_EnergyMeter_should_return_one_sample_trace(_mocked_fun, energy_meter):
    energy_meter.resume()
    energy_meter.stop()

    assert len(energy_meter.get_trace()) == 1


@patch('time.time', side_effect=TIMESTAMP_TRACE)
def test_resume_and_stop_EnergyMeter_should_return_correct_values(_mocked_fun, energy_meter, sample1):
    energy_meter.resume()
    energy_meter.stop()

    for sample in energy_meter.get_trace():
        assert_sample_are_equals(sample, sample1)


@patch('time.time', side_effect=TIMESTAMP_TRACE)
def test_start_record_and_stop_EnergyMeter_should_return_two_sample_trace(_mocked_fun, energy_meter):
    energy_meter.start()
    energy_meter.record()
    energy_meter.stop()

    assert len(energy_meter.get_trace())


@patch('time.time', side_effect=TIMESTAMP_TRACE)
def test_start_record_and_stop_EnergyMeter_should_return_correct_values(_mocked_fun, energy_meter, sample1, sample2):
    energy_meter.start()
    energy_meter.record()
    energy_meter.stop()

    for sample, correct_sample in zip(energy_meter.get_trace(), [sample1, sample2]):
        assert_sample_are_equals(sample, correct_sample)


@patch('time.time', side_effect=TIMESTAMP_TRACE)
def test_start_stop_resume_stop_EnergyMeter_should_return_two_sample_trace(_mocked_fun, energy_meter):
    energy_meter.start()
    energy_meter.stop()
    energy_meter.resume()
    energy_meter.stop()

    assert len(energy_meter.get_trace()) == 2


@patch('time.time', side_effect=TIMESTAMP_TRACE)
def test_start_stop_resume_and_stop_EnergyMeter_should_return_correct_values(_mocked_fun, energy_meter, sample1, sample2_5):
    energy_meter.start()
    energy_meter.stop()
    energy_meter.resume()
    energy_meter.stop()

    for sample, correct_sample in zip(energy_meter.get_trace(), [sample1, sample2_5]):
        assert_sample_are_equals(sample, correct_sample)


@patch('time.time', side_effect=TIMESTAMP_TRACE)
def test_start_record_stop_resume_stop_EnergyMeter_should_return_three_sample_trace(_mocked_fun, energy_meter):
    energy_meter.start()
    energy_meter.record()
    energy_meter.stop()
    energy_meter.resume()
    energy_meter.stop()

    assert len(energy_meter.get_trace()) == 3


@patch('time.time', side_effect=TIMESTAMP_TRACE)
def test_start_record_stop_resume_and_stop_EnergyMeter_should_return_correct_values(_mocked_fun, energy_meter, sample1, sample2, sample3):
    energy_meter.start()
    energy_meter.record()
    energy_meter.stop()
    energy_meter.resume()
    energy_meter.stop()

    for sample, correct_sample in zip(energy_meter.get_trace(), [sample1, sample2, sample3]):
        assert_sample_are_equals(sample, correct_sample)


@patch('time.time', side_effect=TIMESTAMP_TRACE)
def test_second_start_on_an_energy_meter_should_restart_the_trace(_mocked_fun, energy_meter, sample3):
    energy_meter.start()
    energy_meter.record()
    energy_meter.stop()
    energy_meter.start()
    energy_meter.stop()

    samples = []
    for sample in energy_meter.get_trace():
        samples.append(sample)

    assert len(samples) == 1
    assert_sample_are_equals(samples[0], sample3)


############
# TEST TAG #
############
def test_define_energy_meter_with_default_tag_create_sample_with_default_tag():

    device1 = MockedDevice1()
    device1.configure()
    device2 = MockedDevice2()
    device2.configure()
    meter = EnergyMeter([device1, device2], default_tag='tag')

    meter.start()
    meter.stop()

    trace = meter.get_trace()

    sample = trace['tag']
    assert sample.tag == 'tag'


############
# GEN_IDLE #
############
def test_gen_idle_on_empty_trace_return_empty_list(energy_meter):
    trace = EnergyTrace([])
    assert energy_meter.gen_idle(trace) == []


def test_gen_idle_on_one_sample_trace_must_return_list_with_one_value(energy_meter, sample1):
    trace = EnergyTrace([sample1])
    assert len(energy_meter.gen_idle(trace)) == 1


def test_gen_idle_on_two_sample_trace_must_return_list_with_two_value(energy_meter, sample1, sample2):
    trace = EnergyTrace([sample1, sample2])
    assert len(energy_meter.gen_idle(trace)) == 2


@patch('time.sleep', side_effect=TIMESTAMP_TRACE)
def test_gen_idle_on_one_sample_trace_must_wait_same_duration_of_sample_in_second(mocked_time, energy_meter, sample1):
    trace = EnergyTrace([sample1])
    energy_meter.gen_idle(trace)
    assert mocked_time.call_args[0][0] == sample1.duration / 1000000000


@patch('time.sleep', side_effect=TIMESTAMP_TRACE)
def test_gen_idle_on_two_sample_trace_must_wait_same_duration_of_samples_in_second(mocked_time, energy_meter, sample1, sample2):
    trace = EnergyTrace([sample1, sample2])
    energy_meter.gen_idle(trace)
    assert mocked_time.call_args_list[0][0][0] == pytest.approx(sample1.duration / 1000000000)
    assert mocked_time.call_args_list[1][0][0] == pytest.approx(sample2.duration / 1000000000)


@patch('time.sleep', side_effect=TIMESTAMP_TRACE)
def test_gen_idle_on_one_sample_trace_must_return_idle_value(mocked_time, energy_meter, sample1, sample3):
    trace = EnergyTrace([sample1])
    idle = energy_meter.gen_idle(trace)

    # sample1 is the sample measured during idle period
    assert idle[0] == sample1.energy

@patch('time.sleep', side_effect=TIMESTAMP_TRACE)
def test_measure_trace_with_one_sample_and_gen_idle_from_this_trace_must_generate_one_idle_value(mocked_time, energy_meter):
    energy_meter.start()
    energy_meter.stop()

    trace = energy_meter.get_trace()
    assert len(energy_meter.gen_idle(trace)) == 1
