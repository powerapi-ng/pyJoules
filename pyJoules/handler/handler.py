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

from ..energy_trace import EnergyTrace


class UnconsistantSamplesError(Exception):
    """
    Exception raised when processed sample whith differents energy domain
    """


def _check_samples(samples):
    sample1 = samples[0]

    for sample in samples:
        if len(sample.energy) != len(sample1.energy):
            return False
        for domain_name, domain_name1 in zip(sample.energy, sample1.energy):
            if domain_name != domain_name1:
                return False
    return True


class EnergyHandler:
    """
    An object that can handle the measured value of an energy trace
    """

    def __init__(self):
        self.traces = []

    def process(self, trace: EnergyTrace):
        """
        """
        self.traces.append(trace)

    def _flaten_trace(self):
        flatened_trace = EnergyTrace([])
        for trace in self.traces:
            flatened_trace += trace
        if not _check_samples(flatened_trace):
            raise UnconsistantSamplesError()
        return flatened_trace
