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

from . import EnergyDevice


class RaplDevice(EnergyDevice):
    """
    Interface to get energy consumption of CPU domains
    """

    _PACKAGE = 'PKG'
    _UNCORE = 'UNCORE'
    _CORE = 'CORE'
    _DRAM = 'DRAM'

    def __init__(self):
        """
        :raise NoSuchEnergyDeviceError: if no RAPL API is available on this machine
        """

    @staticmethod
    def package(socket_id: int) -> str:
        """
        Get the domain string name to get package power consumption for the given CPU socket
        :param socket_id: the CPU socket to get the power consumption
        :return: the package domain name for the given CPU socket
        """
        raise NotImplementedError()

    @staticmethod
    def uncore(socket_id: int) -> str:
        """
        Get the domain string name to get uncore power consumption for the given CPU socket
        :param socket_id: the CPU socket to get the power consumption
        :return: the uncore domain name for the given CPU socket
        """
        raise NotImplementedError()

    @staticmethod
    def core(socket_id: int) -> str:
        """
        Get the domain string name to get core power consumption for the given CPU socket
        :param socket_id: the CPU socket to get the power consumption
        :return: the core domain name for the given CPU socket
        """
        raise NotImplementedError()

    @staticmethod
    def dram(socket_id: int) -> str:
        """
        Get the domain string name to get dram power consumption for the given CPU socket
        :param socket_id: the CPU socket to get the power consumption
        :return: the dram domain name for the given CPU socket
        """
        raise NotImplementedError()
