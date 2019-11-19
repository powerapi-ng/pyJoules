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

from typing import List, Any
from . import EnergySample


class EnergyTrace:
    """
    A sequence of energy consumption sample
    """

    def __init__(self, domains: List[str]):
        """
        :param domains: list of the monitored domains
        """
        self._domains = domains
        self._end_timestamp = None
        self._first_sample = None
        self._last_sample = None

        # iterator state
        self._current_sample = None

    def record(self, tag: str):
        """
        Add a new sample to the Trace
        :param tag: sample name
        """
        raise NotImplementedError()

    def stop(self):
        """
        Set the end of the energy trace
        """
        raise NotImplementedError()

    def get_sample(self, tag: str) -> EnergySample:
        """
        Retrieve the sample with the given tag
        :param tag: tag of the sample to get
        :return: the sample with the given tag, if many sample have the same tag, the first sample created is returned
        """
        raise NotImplementedError()

    def __add__(self, other_trace: Any) -> EnergyTrace:
        """
        Add two energy traces
        :raise TypeError: if a non EnergyTrace instance is passed as parameter
        """
        raise NotImplementedError()

    def __div__(self, n: Any) -> EnergyTrace:
        """
        Divide the Trace by an integer
        :raise TypeError: if a non integer value is passed as parameter
        """
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

    def __next__(self):
        raise NotImplementedError()
