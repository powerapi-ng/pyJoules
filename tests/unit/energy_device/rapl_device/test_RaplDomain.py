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

import pytest

from pyJoules.energy_device.rapl_device import RaplDevice, RaplCoreDomain, RaplDramDomain, RaplPackageDomain, RaplUncoreDomain


@pytest.fixture(params=[-1, 0, 1])
def integer_value(request):
    """parametrize a test function with negative, null and positive integers
    """
    return request.param


def test_uncore_repr_return_uncore_underscore_socket_id(integer_value):
    domain = RaplUncoreDomain(integer_value)
    assert str(domain) == 'uncore_' + str(integer_value)


def test_core_repr_return_core_underscore_socket_id(integer_value):
    domain = RaplCoreDomain(integer_value)
    assert str(domain) == 'core_' + str(integer_value)


def test_package_repr_return_package_underscore_socket_id(integer_value):
    domain = RaplPackageDomain(integer_value)
    assert str(domain) == 'package_' + str(integer_value)


def test_dram_repr_return_dram_underscore_socket_id(integer_value):
    domain = RaplDramDomain(integer_value)
    assert str(domain) == 'dram_' + str(integer_value)

def test_uncore_get_device_type_return_RaplDevice():
    domain = RaplUncoreDomain(0)
    assert domain.get_device_type() == RaplDevice

def test_core_get_device_type_return_RaplDevice():
    domain = RaplCoreDomain(0)
    assert domain.get_device_type() == RaplDevice


def test_package_get_device_type_return_RaplDevice():
    domain = RaplPackageDomain(0)
    assert domain.get_device_type() == RaplDevice


def test_dram_get_device_type_return_RaplDevice():
    domain = RaplDramDomain(0)
    assert domain.get_device_type() == RaplDevice
