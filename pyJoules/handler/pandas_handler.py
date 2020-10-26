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
from typing import Iterable

try:
    import pandas
except ImportError:
    import logging
    logging.getLogger().info("Pandas is not installed.")

from . import EnergyHandler, UnconsistantSamplesError
from ..energy_trace import EnergyTrace, EnergySample


def _gen_column_names(samples):
    sample = samples[0]
    names = ['timestamp', 'tag', 'duration']

    for domain_name in sample.energy:
        names.append(domain_name)
    return names


def _gen_data(samples):
    data = []
    for sample in samples:
        data.append(_gen_row(sample))
    return data


def _gen_row(sample):
    row = [sample.timestamp, sample.tag, sample.duration]

    for domain_name in sample.energy:
        row.append(sample.energy[domain_name])
    return row


def trace_to_dataframe(trace: Iterable[EnergySample]) -> pandas.DataFrame:
    """
    convert an energy trace into a pandas DataFrame
    """
    if len(trace) == 0:
        return pandas.DataFrame()

    return pandas.DataFrame(columns=_gen_column_names(trace), data=_gen_data(trace))


class NoSampleProcessedError(Exception):
    """
    Exception raised when trying to get dataframe from pandas handler without process any sample before
    """


class PandasHandler(EnergyHandler):
    """
    handle energy sample to convert them into pandas DataFrame
    """
    def __init__(self):
        EnergyHandler.__init__(self)
        self.traces = []

    def process(self, trace: EnergyTrace):
        self.traces.append(trace)

    def get_dataframe(self) -> pandas.DataFrame:
        """
        return the DataFrame containing the processed samples
        """
        if len(self.traces) > 0:
            faltened_trace = self._flaten_trace()
            return trace_to_dataframe(faltened_trace)
        raise NoSampleProcessedError()
