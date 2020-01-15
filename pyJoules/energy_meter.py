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
from __future__ import annotations

import time
import operator
import functools

from functools import reduce
from typing import List, Optional

from .exception import PyJoulesException
from .energy_device import EnergyDevice, EnergyDomain, EnergyDeviceFactory
from .energy_handler import EnergyHandler, PrintHandler
from . import EnergySample

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

    def __init__(self, devices: List[EnergyDevice], default_tag: str = ''):
        """
        :param devices: list of the monitored devices
        :param default_tag: tag given if no tag were given to a measure
        """
        self.devices = devices
        self.default_tag = default_tag

        self._last_state = None
        self._first_state = None

    def _measure_new_state(self, tag):
        timestamp = time.perf_counter()
        values = [device.get_energy() for device in self.devices]

        return EnergyState(timestamp, tag if tag is not None else self.default_tag, values)

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
        if self._first_state is None:
            raise EnergyMeterNotStartedError()

        new_state = self._measure_new_state(tag)
        self._last_state.add_next_state(new_state)
        self._last_state = new_state

    def stop(self):
        """
        Set the end of the energy trace
        :raise EnergyMeterNotStartedError: if the energy meter isn't started
        """
        if self._first_state is None:
            raise EnergyMeterNotStartedError()

        new_state = self._measure_new_state('__stop__')
        self._last_state.add_next_state(new_state)
        self._last_state = new_state

    def get_sample(self, tag: str) -> EnergySample:
        """
        Retrieve the first sample in the trace with the given tag
        :param tag: tag of the sample to get
        :return: the sample with the given tag, if many sample have the same tag, the first sample created is returned
        :raise EnergyMeterNotStoppedError: if the energy meter isn't stopped
        :raise SampleNotFoundError: if the trace doesn't contains a sample with the given tag name
        """
        if self._first_state is None:
            raise EnergyMeterNotStartedError()

        if not self._last_state.tag == '__stop__':
            raise EnergyMeterNotStoppedError()

        for sample in self:
            if sample.tag == tag:
                return sample
        raise SampleNotFoundError()

    def _get_domain_list(self):
        """
        return the list of all monitored domains for each monitored energy devices
        """
        return reduce(operator.add, [device.get_configured_domains() for device in self.devices])

    def __iter__(self):
        """
        iterate on the energy sample of the last trace
        :raise EnergyMeterNotStoppedError: if the energy meter isn't stopped
        """
        if self._first_state is None:
            raise EnergyMeterNotStartedError()

        if not self._last_state.tag == '__stop__':
            raise EnergyMeterNotStoppedError()
        domains = self._get_domain_list()
        return SampleIterator(self._first_state, domains)

class SampleIterator:

    def __init__(self, first_state, domains):
        self.domains = domains
        self._current_state = first_state

    def _gen_sample(self, state):
        return EnergySample(state.timestamp, state.tag, state.compute_duration(), state.compute_energy(self.domains))

    def __next__(self):
        if self._current_state.next_state is None:
            raise StopIteration()

        sample = self._gen_sample(self._current_state)
        self._current_state = self._current_state.next_state
        return sample


class EnergyState:
    """
    Internal class that record the current energy state of the monitored device
    """

    def __init__(self, timestamp: float, tag: str, values: List[float]):
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

    def add_next_state(self, state: EnergyState):
        """
        :param previous: next state for the same energy trace
        :raise StateIsNotFinalError: if there are already a next state
        """
        if self.next_state is not None:
            raise StateIsNotFinalError()
        self.next_state = state


def measureit(handler: EnergyHandler = PrintHandler(), domains: Optional[List[EnergyDomain]] = None):
    """
    Measure the energy consumption of monitored devices during the execution of the decorated function
    :param handler: handler instance that will receive the power consummation data
    :param domains: list of the monitored energy domains
    """
    def decorator_measure_energy(func):

        devices = EnergyDeviceFactory.create_devices(domains)
        energy_meter = EnergyMeter(devices)

        @functools.wraps(func)
        def wrapper_measure(*args, **kwargs):
            energy_meter.start(tag=func.__name__)
            val = func(*args, **kwargs)
            energy_meter.stop()
            for sample in energy_meter:
                handler.process(sample)
            return val
        return wrapper_measure

    return decorator_measure_energy


class EnergyContext():

    def __init__(self, handler: EnergyHandler = PrintHandler(), domains: Optional[List[EnergyDomain]] = None, start_tag='start'):
        self.handler = handler
        self.start_tag = start_tag

        devices = EnergyDeviceFactory.create_devices(domains)
        self.energy_meter = EnergyMeter(devices)

    def __enter__(self) -> EnergyMeter:
        self.energy_meter.start(self.start_tag)
        return self.energy_meter

    def __exit__(self, type, value, traceback):
        self.energy_meter.stop()
        for sample in self.energy_meter:
            self.handler.process(sample)
