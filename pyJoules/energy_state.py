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

from typing import List


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
        self.next_sample = None

    def compute_duration(self) -> float:
        """
        :return: compute the time elipsed between the current state and the next state
        """
        raise NotImplementedError()

    def compute_energy(self) -> List[float]:
        """
        :return: compute the energy consumed between the current state and the next state
        """
        raise NotImplementedError()

    def add_next_state(self, sample: EnergyState):
        """
        :param previous: next state for the same energy trace
        """
        raise NotImplementedError()
