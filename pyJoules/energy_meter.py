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
import time
import operator
import functools

from functools import reduce
from typing import List, Optional, Dict

from .exception import PyJoulesException
from .device import Device, Domain, DeviceFactory
from .handler import EnergyHandler, PrintHandler
from .energy_trace import EnergySample, EnergyTrace

class NoNextStateException(PyJoulesException):
    """Exception raised when trying to compute duration or energy from a state
    which is the last state of an energy trace.
    """


class StateIsNotFinalError(PyJoulesException):
    """Exception raised when trying to add a state to a non final state on an energy trace
    """


class EnergyMeterNotStartedError(PyJoulesException):
    """
    Exception raised when trying to stop or record on a non started EnergyMeter instance
    """


class EnergyMeterNotStoppedError(PyJoulesException):
    """
    Exception raised when trying to get energy samples from non stopped EnergyMeter instance
    """


class SampleNotFoundError(PyJoulesException):
    """
    Exception raised when trying to retrieve a sample that does not exist on trace
    """


class EnergyMeter:
    """
    Tool used to record the energy consumption of given devices
    """

    def __init__(self, devices: List[Device], default_tag: str = ''):
        """
        :param devices: list of the monitored devices
        :param default_tag: tag given if no tag were given to a measure
        """
        self.devices = devices
        self.default_tag = default_tag

        self._last_state = None
        self._first_state = None

    def _measure_new_state(self, tag):
        timestamp = time.time()
        values = [device.get_energy() for device in self.devices]

        return EnergyState(timestamp, tag if tag is not None else self.default_tag, values)

    def _append_new_state(self, new_state):
        self._last_state.add_next_state(new_state)
        self._last_state = new_state

    def _is_meter_started(self):
        return not self._first_state is None

    def _is_meter_stoped(self):
        return self._last_state.tag == '__stop__'

    def _reinit(self):
        self._first_state = None
        self._last_state = None

    def start(self, tag: Optional[str] = None):
        """
        Begin a new energy trace

        :param tag: sample name
        """
        new_state = self._measure_new_state(tag)
        self._first_state = new_state
        self._last_state = new_state

    def record(self, tag: Optional[str] = None):
        """
        Add a new state to the Trace

        :param tag: sample name
        :raise EnergyMeterNotStartedError: if the energy meter isn't started
        """
        if not self._is_meter_started():
            raise EnergyMeterNotStartedError()

        new_state = self._measure_new_state(tag)
        self._append_new_state(new_state)

    def resume(self, tag: Optional[str] = None):
        """
        resume the energy Trace (if no energy trace was launched, start a new one

        :param tag: sample name
        :raise EnergyMeterNotStoppedError: if the energy meter isn't stopped
        """
        if not self._is_meter_started():
            return self.start(tag)
        
        if not self._is_meter_stoped():
            raise EnergyMeterNotStoppedError()

        new_state = self._measure_new_state(tag)
        self._append_new_state(new_state)

    def stop(self):
        """
        Set the end of the energy trace

        :raise EnergyMeterNotStartedError: if the energy meter isn't started
        """
        if not self._is_meter_started():
            raise EnergyMeterNotStartedError()

        new_state = self._measure_new_state('__stop__')
        self._append_new_state(new_state)

    def get_trace(self) -> EnergyTrace:
        """
        return the last trace measured

        :raise EnergyMeterNotStoppedError: if the energy meter isn't stopped
        """
        if not self._is_meter_started():
            return EnergyTrace([])

        if not self._is_meter_stoped():
            raise EnergyMeterNotStoppedError()

        return self._generate_trace()

    def _get_domain_list(self):
        """
        return the list of all monitored domains for each monitored energy devices
        """
        return reduce(operator.add, [device.get_configured_domains() for device in self.devices])

    def _generate_trace(self):
        domains = self._get_domain_list()
        generator = TraceGenerator(self._first_state, domains)
        return generator.generate()

    def gen_idle(self, trace: EnergyTrace) -> List[Dict[str, float]]:
        """
        generate idle values of an energy trace
        for each sample, wait for the duraction of a sample and measure the energy consumed during this period

        :return: the list of idle energy consumption for each sample in the trace
        """
        self._reinit()
        idle_values = []

        for sample in trace:
            self.resume()
            time.sleep(sample.duration / 1000000000)
            self.stop()

        for sample in self.get_trace():
            idle_values.append(sample.energy)

        return idle_values


class TraceGenerator:

    def __init__(self, first_state, domains):
        self.domains = domains
        self._current_state = first_state

    def generate(self):
        def generate_next(current_state, samples):
            if current_state.next_state is None:
                return samples
            if current_state.tag == '__stop__':
                return generate_next(current_state.next_state, samples)

            sample = self._gen_sample(current_state)
            samples.append(sample)
            return generate_next(current_state.next_state, samples)

        samples = generate_next(self._current_state, [])
        return EnergyTrace(samples)

    def _gen_sample(self, state):
        return EnergySample(state.timestamp, state.tag, state.compute_duration(), state.compute_energy(self.domains))


class EnergyState:
    """
    Internal class that record the current energy state of the monitored device
    """

    def __init__(self, timestamp: float, tag: str, values: List[Dict[str, float]]):
        """
        :param timstamp: timestamp of the measure
        :param tag: tag of the measure
        :param values: energy consumption measure, this is the list of measured energy consumption values for each
                       monitored device. This list contains the energy consumption since the last device reset to the
                       end of this sample
        """
        self.timestamp = timestamp
        self.tag = tag
        self.values = values
        self.next_state = None

    def is_last(self) -> bool:
        """
        indicate if the current state is the last state of the trace or not
         :return: True if the current state is the last state of the trace False otherwise
        """
        return self.next_state is None

    def compute_duration(self) -> float:
        """
        :return: compute the time elipsed between the current state and the next state
        :raise NoNextStateException: if the state is the last state of the trace
        """
        if self.next_state is None:
            raise NoNextStateException()

        return self.next_state.timestamp - self.timestamp

    def compute_energy(self, domains) -> List[float]:
        """
        :return: compute the energy consumed between the current state and the next state
        :raise NoNextStateException: if the state is the last state of the trace
        """
        if self.next_state is None:
            raise NoNextStateException()

        energy = []
        for next_state_device, current_state_device in zip(self.next_state.values, self.values):
            for next_value, current_value in zip(next_state_device, current_state_device):
                energy.append(next_value - current_value)

        values_dict = {}
        for value, key in zip(energy, domains):
            values_dict[str(key)] = value
        return values_dict

    def add_next_state(self, state: 'EnergyState'):
        """
        :param previous: next state for the same energy trace
        :raise StateIsNotFinalError: if there are already a next state
        """
        if self.next_state is not None:
            raise StateIsNotFinalError()
        self.next_state = state


def measure_energy(func=None ,handler: EnergyHandler = PrintHandler(), domains: Optional[List[Domain]] = None):
    """
    Measure the energy consumption of monitored devices during the execution of the decorated function

    :param handler: handler instance that will receive the power consummation data
    :param domains: list of the monitored energy domains
    """
    def decorator_measure_energy(func):

        devices = DeviceFactory.create_devices(domains)
        energy_meter = EnergyMeter(devices)

        @functools.wraps(func)
        def wrapper_measure(*args, **kwargs):
            energy_meter.start(tag=func.__name__)
            val = func(*args, **kwargs)
            energy_meter.stop()
            handler.process(energy_meter.get_trace())
            return val
        return wrapper_measure

    if func is None:
        # to ensure the working system when you call it with parameters or without parameters
        return decorator_measure_energy
    else:
        return decorator_measure_energy(func)


class EnergyContext():

    def __init__(self, handler: EnergyHandler = PrintHandler(), domains: Optional[List[Domain]] = None, start_tag: str = 'start'):
        """
        Measure the energy consumption of monitored devices during the execution of the contextualized code

        :param handler: handler instance that will receive the power consummation data
        :param domains: list of the monitored energy domains
        :param start_tag: first tag of the trace
        """
        self.handler = handler
        self.start_tag = start_tag

        devices = DeviceFactory.create_devices(domains)
        self.energy_meter = EnergyMeter(devices)

    def __enter__(self) -> EnergyMeter:
        self.energy_meter.start(self.start_tag)
        return self.energy_meter

    def __exit__(self, type, value, traceback):
        self.energy_meter.stop()
        self.handler.process(self.energy_meter.get_trace())
