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
from typing import List, Optional

from .exception import PyJoulesException
from .energy_device import EnergyDevice, EnergyDomain
from .energy_handler import EnergyHandler
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


class EnergyMeterNotStopedError(PyJoulesException):
    """
    Exception raised when trying to get energy samples from non stoped EnergyMeter instance
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

    def start(self, tag: Optional[str] = None):
        """
        Begin a new energy trace
        :param tag: sample name
        """
        raise NotImplementedError()

    def record(self, tag: Optional[str] = None):
        """
        Add a new state to the Trace
        :param tag: sample name
        :raise EnergyMeterNotStartedError: if the energy meter isn't started
        """
        raise NotImplementedError()

    def stop(self):
        """
        Set the end of the energy trace
        :raise EnergyMeterNotStartedError: if the energy meter isn't started
        """
        raise NotImplementedError()

    def get_sample(self, tag: str) -> EnergySample:
        """
        Retrieve the first sample in the trace with the given tag
        :param tag: tag of the sample to get
        :return: the sample with the given tag, if many sample have the same tag, the first sample created is returned
        :raise EnergyMeterNotStopedError: if the energy meter isn't stoped
        :raise SampleNotFoundError: if the trace doesn't contains a sample with the given tag name
        """
        raise NotImplementedError()

    def __iter__(self):
        """
        iterate on the energy sample of the last trace
        :raise EnergyMeterNotStopedError: if the energy meter isn't stoped
        """
        raise NotImplementedError()

    def __next__(self):
        raise NotImplementedError()


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
        raise NotImplementedError()

    def compute_duration(self) -> float:
        """
        :return: compute the time elipsed between the current state and the next state
        :raise NoNextStateException: if the state is the last state of the trace
        """
        raise NotImplementedError()

    def compute_energy(self) -> List[float]:
        """
        :return: compute the energy consumed between the current state and the next state
        :raise NoNextStateException: if the state is the last state of the trace
        """
        raise NotImplementedError()

    def add_next_state(self, state: EnergyState):
        """
        :param previous: next state for the same energy trace
        """
        raise NotImplementedError()


def measureit(handler: EnergyHandler, domains: List[EnergyDomain]):
    """
    Measure the energy consumption of monitored devices during the execution of the decorated function
    :param handler: handler instance that will receive the power consummation data
    :param domains: list of the monitored energy domains
    """
    raise NotImplementedError()


class EnergyContext():

    def __init__(self, handler: EnergyHandler, domains: List[EnergyDomain]):
        raise NotImplementedError()

    def record(self, tag: Optional[str]):
        raise NotImplementedError()

    def __enter__(self) -> EnergyMeter:
        raise NotImplementedError()

    def __exit__(self, type, value, traceback):
        raise NotImplementedError()
