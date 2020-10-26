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
from typing import Dict, Any, List, Callable
from functools import reduce
from operator import and_


class EnergySample:
    """
    :var timestamp: begining timestamp
    :vartype timestamp: float
    :var tag: sample tag
    :vartype tag: str
    :var duration: duration of the sample in seconds
    :vartype duration: float
    :var energy: dictionary that contains the energy consumed during this sample
    :vartype energy: Dict[str, float]
    """
    def __init__(self, timestamp: float, tag: str, duration: float, energy: Dict[str, float]):
        self.timestamp = timestamp
        self.tag = tag
        self.duration = duration
        self.energy = energy


class EnergyTrace:
    """
    Trace of all EnergySample collected by a meter
    """
    def __init__(self, samples: List[EnergySample]):
        """
        :param samples: samples containing in the trace
        """
        self._samples = []
        for sample in samples:
            self._samples.append(sample)

    def _get_sample_from_tag(self, tag):
        for sample in self._samples:
            if sample.tag == tag:
                return sample

    def __getitem__(self, key: Any) -> EnergySample:
        """
        Return the n-th EnergySample on the trace or the first sample with the given tag

        :param key: integer to get the n-th EnergySample or the tag of the needed sample
        :return: An EnergySample
        :raise KeyError: if no sample match the given tag
        :raise IndexError: if no sample match the given index
        """
        if isinstance(key, int):
            if key > len(self._samples):
                raise IndexError('Trace index out of range : ' + str(key))
            return self._samples[key]

        sample = self._get_sample_from_tag(key)
        if sample is None:
            raise KeyError('this tag doesn\'t match any sample : ' + str(key))
        return sample

    def __iter__(self):
        """
        Iterate on the trace's samples
        """
        return self._samples.__iter__()

    def __len__(self) -> int:
        """
        return the number of sample in the trace
        """
        return len(self._samples)

    def __contains__(self, key: str):
        return not self._get_sample_from_tag(key) is None

    def __add__(self, trace:  'EnergySample'):
        samples = self._samples + trace._samples
        return EnergyTrace(samples)

    def __iadd__(self, trace: 'EnergySample'):
        self._samples += trace._samples
        return self

    def append(self, sample: EnergySample):
        """
        append a new sample to the trace
        """
        self._samples.append(sample)

    def remove_idle(self, idle: List[Dict[str, float]]):
        """
        substract idle energy values from the current trace

        :param idle: list of idle consumption values to substract to current trace
                     idle consumption values must be grouped in a dictionary with their domain as key
        :raise ValueError: if the number of values in the list doesn't match the number of sample in the trace
                           or if a domain of the trace is not in the idle values
        """
        if len(idle) != len(self._samples):
            raise ValueError('idle list havn\'t the same length than the trace')

        for idle_energy, sample in zip(idle, self._samples):
            for domain in sample.energy:
                if domain not in idle_energy:
                    raise ValueError('domain not present in idle values : ' + domain)
                sample.energy[domain] -= idle_energy[domain]

    def _sample_havnt_negative_values(self, sample):
        for val in sample.energy.values():
            if val < 0:
                return False
        return True

    def clean_data(self, guards: List[Callable[[EnergySample], bool]] = []):
        """
        Remove sample with negative energy values from the trace
        Guards can be added to specify rules to remove sample

        :param guards: list of function that is used as rules to remove samples. A guard is a function that take a
                       sample as parameter and return True if it must be keept in the trace, False otherwise
        """

        extended_guards = [lambda s: self._sample_havnt_negative_values(s)] + guards

        valid_samples = []
        for sample in self._samples:

            validity_list = [guard(sample) for guard in extended_guards]
            if reduce(and_, validity_list):
                valid_samples.append(sample)
        self._samples = valid_samples
