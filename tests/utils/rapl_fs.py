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
import random
import pytest
import pyfakefs

from pyJoules.energy_device.rapl_device import RaplDevice
from .fake_api import FakeAPI


SOCKET_0_DIR_NAME = '/sys/class/powercap/intel-rapl/intel-rapl:0'
SOCKET_1_DIR_NAME = '/sys/class/powercap/intel-rapl/intel-rapl:1'

PKG_0_FILE_NAME = SOCKET_0_DIR_NAME + '/energy_uj'
PKG_0_VALUE = 12345
PKG_1_FILE_NAME = SOCKET_1_DIR_NAME + '/energy_uj'
PKG_1_VALUE = 54321

DRAM_0_DIR_NAME = SOCKET_0_DIR_NAME + '/intel-rapl:0:0'
DRAM_1_DIR_NAME = SOCKET_1_DIR_NAME + '/intel-rapl:1:0'

DRAM_0_FILE_NAME = DRAM_0_DIR_NAME + '/energy_uj'
DRAM_0_VALUE = 6789
DRAM_1_FILE_NAME = DRAM_1_DIR_NAME + '/energy_uj'
DRAM_1_VALUE = 9876

CORE_0_DIR_NAME = SOCKET_0_DIR_NAME + '/intel-rapl:0:1'
CORE_1_DIR_NAME = SOCKET_1_DIR_NAME + '/intel-rapl:1:1'

CORE_0_FILE_NAME = CORE_0_DIR_NAME + '/energy_uj'
CORE_1_FILE_NAME = CORE_1_DIR_NAME + '/energy_uj'


class RaplFS(FakeAPI):

    def __init__(self, fs):
        self.fs = fs
        self.domains_current_energy = {}
        self.domains_energy_file = {}

    def add_domain(self, domain_dir_name, domain_name, domain_id):
        self.fs.create_file(domain_dir_name + '/name', contents=domain_name + '\n')
        energy_value = random.random()
        self.fs.create_file(domain_dir_name + '/energy_uj', contents=str(energy_value) + '\n')
        self.domains_energy_file[domain_id] = domain_dir_name + '/energy_uj'
        self.domains_current_energy[domain_id] = energy_value

    def reset_values(self):
        for key in self.domains_energy_file:
            new_val = random.random()
            self.domains_current_energy[key] = new_val
            with open(self.domains_energy_file[key], 'w') as energy_file:
                energy_file.write(str(new_val) + '\n')

    def get_device_type(self):
        return RaplDevice



@pytest.fixture
def empty_fs(fs):
    """
    filesystem describing a machine with one CPU but no RAPL API
    """
    return RaplFS(fs)


@pytest.fixture
def fs_pkg_one_socket(fs):
    """
    filesystem describing a machine with one CPU and RAPL API for package
    """
    rapl_fs = RaplFS(fs)
    rapl_fs.add_domain(SOCKET_0_DIR_NAME, 'package-0', 'package_0')
    rapl_fs.reset_values()
    return rapl_fs


@pytest.fixture
def fs_pkg_dram_one_socket(fs):
    """
    filesystem describing a machine with one CPU and RAPL API for package and dram
    """
    rapl_fs = RaplFS(fs)
    rapl_fs.add_domain(SOCKET_0_DIR_NAME, 'package-0', 'package_0')
    rapl_fs.add_domain(DRAM_0_DIR_NAME, 'dram', 'dram_0')
    rapl_fs.reset_values()
    return rapl_fs


@pytest.fixture
def fs_pkg_psys_one_socket(fs):
    """
    filesystem describing a machine with one CPU and RAPL API for package and psys
    """
    rapl_fs = RaplFS(fs)
    rapl_fs.add_domain(SOCKET_0_DIR_NAME, 'package-0', 'package_0')
    rapl_fs.add_domain('/sys/class/powercap/intel-rapl/intel-rapl:1', 'psys', 'psys')
    rapl_fs.reset_values()
    return rapl_fs


@pytest.fixture
def fs_pkg_dram_core_one_socket(fs):
    """
    filesystem describing a machine with one CPU and RAPL API for package dram and core
    """
    rapl_fs = RaplFS(fs)
    rapl_fs.add_domain(SOCKET_0_DIR_NAME, 'package-0', 'package_0')
    rapl_fs.add_domain(DRAM_0_DIR_NAME, 'dram', 'dram_0')
    rapl_fs.add_domain(CORE_0_DIR_NAME, 'core', 'core_0')
    rapl_fs.reset_values()
    return rapl_fs

@pytest.fixture
def fs_pkg_dram_uncore_one_socket(fs):
    """
    filesystem describing a machine with one CPU and RAPL API for package dram and core
    """
    rapl_fs = RaplFS(fs)
    rapl_fs.add_domain(SOCKET_0_DIR_NAME, 'package-0', 'package_0')
    rapl_fs.add_domain(DRAM_0_DIR_NAME, 'dram', 'dram_0')
    rapl_fs.add_domain(CORE_0_DIR_NAME, 'uncore', 'uncore_0')
    rapl_fs.reset_values()
    return rapl_fs


@pytest.fixture
def fs_pkg_two_socket(fs):
    """
    filesystem describing a machine with two CPU and RAPL API for package
    """
    rapl_fs = RaplFS(fs)
    rapl_fs.add_domain(SOCKET_0_DIR_NAME, 'package-0', 'package_0')
    rapl_fs.add_domain(SOCKET_1_DIR_NAME, 'package-1', 'package_1')
    rapl_fs.reset_values()
    return rapl_fs


@pytest.fixture
def fs_pkg_dram_two_socket(fs):
    """
    filesystem describing a machine with two CPU and RAPL API for package and dram
    """
    rapl_fs = RaplFS(fs)
    rapl_fs.add_domain(SOCKET_0_DIR_NAME, 'package-0', 'package_0')
    rapl_fs.add_domain(SOCKET_1_DIR_NAME, 'package-1', 'package_1')
    rapl_fs.add_domain(DRAM_0_DIR_NAME, 'dram', 'dram_0')
    rapl_fs.add_domain(DRAM_1_DIR_NAME, 'dram', 'dram_1')
    rapl_fs.reset_values()
    return rapl_fs


@pytest.fixture
def fs_pkg_psys_two_socket(fs):
    """
    filesystem describing a machine with two CPU and RAPL API for package
    """
    rapl_fs = RaplFS(fs)
    rapl_fs.add_domain(SOCKET_0_DIR_NAME, 'package-0', 'package_0')
    rapl_fs.add_domain(SOCKET_1_DIR_NAME, 'package-1', 'package_1')

    rapl_fs.add_domain('/sys/class/powercap/intel-rapl/intel-rapl:2/name', 'psys', 'psys')
    rapl_fs.reset_values()
    return fs
