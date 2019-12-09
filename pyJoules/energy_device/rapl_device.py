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

from . import EnergyDevice, EnergyDomain


class RaplDomain(EnergyDomain):

    def __init__(self, socket : int):
        EnergyDomain.__init__(self)
        self.socket = socket


class RaplCoreDomain(RaplDomain):

    def __repr__(self) -> str:
        raise NotImplementedError()


class RaplUncoreDomain(RaplDomain):

    def __repr__(self) -> str:
        raise NotImplementedError()


class RaplDramDomain(RaplDomain):

    def __repr__(self) -> str:
        raise NotImplementedError()


class RaplPackageDomain(RaplDomain):

    def __repr__(self) -> str:
        raise NotImplementedError()


class RaplDevice(EnergyDevice):
    """
    Interface to get energy consumption of CPU domains
    """

    def __init__(self):
        """
        :raise NoSuchEnergyDeviceError: if no RAPL API is available on this machine
        """
        raise NotImplementedError()

    @staticmethod
    def available_package_domains() -> List[RaplPackageDomain]:
        """
        return a the list of the available energy Package domains
        """
        raise NotImplementedError()

    @staticmethod
    def available_dram_domains() -> List[RaplDramDomain]:
        """
        return a the list of the available energy Dram domains
        """
        raise NotImplementedError()

    @staticmethod
    def available_core_domains() -> List[RaplCoreDomain]:
        """
        return a the list of the available energy Core domains
        """
        raise NotImplementedError()

    @staticmethod
    def available_uncore_domains() -> List[RaplUncoreDomain]:
        """
        return a the list of the available energy Uncore domains
        """
        raise NotImplementedError()
