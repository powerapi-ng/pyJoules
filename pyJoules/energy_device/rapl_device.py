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
import os
from typing import List

from . import EnergyDevice, EnergyDomain, NotConfiguredDeviceException
from pyJoules.exception import NoSuchEnergyDeviceError


class RaplDomain(EnergyDomain):

    def __init__(self, socket: int):
        EnergyDomain.__init__(self)
        self.socket = socket
        self._repr = self.get_domain_name() + '_' + str(socket)

    def get_device_type(self):
        return RaplDevice

    def get_domain_name(self) -> str:
        """
        :return: domain name without socket identifier
        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        """
        :return: domain name with socket identifier
        """
        return self._repr

    def __eq__(self, other) -> bool:
        return isinstance(other, RaplDomain) and self.__repr__() == other.__repr__()

    def __lt__(self, other) -> bool:
        if isinstance(other, RaplDomain):
            return self.__repr__() < other.__repr__()
        raise ValueError()

    def __gt__(self, other) -> bool:
        if isinstance(other, RaplDomain):
            return self.__repr__() > other.__repr__()
        raise ValueError()


class RaplCoreDomain(RaplDomain):
    def get_domain_name(self):
        return "core"


class RaplUncoreDomain(RaplDomain):
    def get_domain_name(self):
        return "uncore"


class RaplDramDomain(RaplDomain):
    def get_domain_name(self):
        return "dram"


class RaplPackageDomain(RaplDomain):
    def get_domain_name(self):
        return "package"


RAPL_API_DIR = '/sys/class/powercap/intel-rapl'


class RaplDevice(EnergyDevice):
    """
    Interface to get energy consumption of CPU domains
    """

    def __init__(self):
        """
        :raise NoSuchEnergyDeviceError: if no RAPL API is available on this machine
        """
        EnergyDevice.__init__(self)
        self._api_files = None

    @staticmethod
    def _rapl_api_available():
        return os.path.exists(RAPL_API_DIR)

    @staticmethod
    def available_domains() -> List[RaplDomain]:
        """
        return a the list of the available energy domains
        """
        if not RaplDevice._rapl_api_available():
            raise NoSuchEnergyDeviceError()

        return (RaplDevice.available_package_domains() + RaplDevice.available_dram_domains() +
                RaplDevice.available_core_domains() + RaplDevice.available_uncore_domains())

    @staticmethod
    def _get_socket_id_list():
        socket_id_list = []
        socket_id = 0
        while True:
            name = RAPL_API_DIR + '/intel-rapl:' + str(socket_id)
            if os.path.exists(name):
                socket_id_list.append(socket_id)
                socket_id += 1
            else:
                return socket_id_list

    @staticmethod
    def available_package_domains() -> List[RaplPackageDomain]:
        """
        return a the list of the available energy Package domains
        """
        package_domains = []

        for socket_id in RaplDevice._get_socket_id_list():
            domain_name_file_str = RAPL_API_DIR + '/intel-rapl:' + str(socket_id) + '/name'
            if os.path.exists(domain_name_file_str):
                domain_name_file = open(domain_name_file_str)
                if domain_name_file.readline() == 'package-' + str(socket_id) + '\n':
                    package_domains.append(RaplPackageDomain(socket_id))
        return package_domains

    @staticmethod
    def _domain_exist_on_socket(socket_id, domain_name):
        domain_id = 0
        while True:
            domain_name_file_str = (RAPL_API_DIR + '/intel-rapl:' + str(socket_id) + '/intel-rapl:' + str(socket_id) +
                                    ':' + str(domain_id) + '/name')
            if os.path.exists(domain_name_file_str):
                domain_name_file = open(domain_name_file_str)
                if domain_name_file.readline() == domain_name + '\n':
                    return True
                domain_id += 1
            else:
                return False

    @staticmethod
    def available_dram_domains() -> List[RaplDramDomain]:
        """
        return a the list of the available energy Dram domains
        """
        dram_domains = []
        for socket_id in RaplDevice._get_socket_id_list():
            if RaplDevice._domain_exist_on_socket(socket_id, 'dram'):
                dram_domains.append(RaplDramDomain(socket_id))
        return dram_domains

    @staticmethod
    def available_core_domains() -> List[RaplCoreDomain]:
        """
        return a the list of the available energy Core domains
        """
        core_domains = []
        for socket_id in RaplDevice._get_socket_id_list():
            if RaplDevice._domain_exist_on_socket(socket_id, 'core'):
                core_domains.append(RaplCoreDomain(socket_id))
        return core_domains

    @staticmethod
    def available_uncore_domains() -> List[RaplUncoreDomain]:
        """
        return a the list of the available energy Uncore domains
        """
        uncore_domains = []
        for socket_id in RaplDevice._get_socket_id_list():
            if RaplDevice._domain_exist_on_socket(socket_id, 'uncore'):
                uncore_domains.append(RaplUncoreDomain(socket_id))
        return uncore_domains

    def _get_domain_file_name(self, domain):
        socket_id = domain.socket

        if isinstance(domain, RaplPackageDomain):
            return RAPL_API_DIR + '/intel-rapl:' + str(socket_id) + '/energy_uj'

        domain_id = 0
        while True:
            domain_name_file_str = (RAPL_API_DIR + '/intel-rapl:' + str(socket_id) + '/intel-rapl:' + str(socket_id) +
                                    ':' + str(domain_id) + '/name')
            if os.path.exists(domain_name_file_str):
                domain_name_file = open(domain_name_file_str)
                if domain_name_file.readline() == domain.get_domain_name() + '\n':
                    return (RAPL_API_DIR + '/intel-rapl:' + str(socket_id) + '/intel-rapl:' + str(socket_id) +
                            ':' + str(domain_id) + '/energy_uj')
                else:
                    domain_id += 1
            else:
                raise ValueError()

    def _open_api_files(self, domain_list):
        api_files = []
        for domain in domain_list:
            domain_file_name = self._get_domain_file_name(domain)
            api_files.append(open(domain_file_name))
        return api_files

    def configure(self, domains=None):
        EnergyDevice.configure(self, domains)

        self._api_files = self._open_api_files(self._configured_domains)

    def _read_energy_value(self, api_file):
        api_file.seek(0, 0)
        return float(api_file.readline())

    def get_energy(self):
        return [self._read_energy_value(api_file) for api_file in self._api_files]
