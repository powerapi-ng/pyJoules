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
import os.path

from . import EnergyHandler

class CSVHandler(EnergyHandler):

    def __init__(self, filename: str):
        """
        :param filename: file name to store processed trace
        """
        EnergyHandler.__init__(self)

        self._filename = filename

    def _gen_header(self, first_sample):
        domain_names = first_sample.energy.keys()
        return 'timestamp;tag;duration;' + ';'.join(domain_names)

    def _gen_sample_line(self, sample, domain_names):
        line_begining = f'{sample.timestamp};{sample.tag};{sample.duration};'
        energy_values = [str(sample.energy[domain]) for domain in domain_names]
        return line_begining + ';'.join(energy_values)

    def _init_file(self, first_sample):
        if os.path.exists(self._filename):
            csv_file = open(self._filename, 'a+')
            return csv_file
        else:
            csv_file = open(self._filename, 'w+')
            csv_file.write(self._gen_header(first_sample) + '\n')
            return csv_file

    def save_data(self):
        """
        append processed trace to the file
        """
        flatened_trace = self._flaten_trace()
        first_sample = flatened_trace[0]
        domain_names = first_sample.energy.keys()

        csv_file = self._init_file(first_sample)

        for sample in flatened_trace:
            csv_file.write(self._gen_sample_line(sample, domain_names) + '\n')
        csv_file.close()
        self.traces = []
