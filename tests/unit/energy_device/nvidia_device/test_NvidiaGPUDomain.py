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

from pyJoules.energy_device.nvidia_device import NvidiaGPUDomain, NvidiaGPUDevice


@pytest.fixture(params=[-1, 0, 1])
def integer_value(request):
    """parametrize a test function with negative, null and positive integers
    """
    return request.param


def test_repr_return_nvidia_gpu_underscore_device_id(integer_value):
    domain = NvidiaGPUDomain(integer_value)
    assert str(domain) == 'nvidia_gpu_' + str(integer_value)


def test_get_device_type_return_NvidiaGPUDevice():
    domain = NvidiaGPUDomain(0)
    assert domain.get_device_type() == NvidiaGPUDevice
