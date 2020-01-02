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

from pyJoules.energy_meter import EnergyState, NoNextStateException, StateIsNotFinalError


TS_FIRST = 1.0
TS_SECOND = 2.0

E_FIRST_DOMAIN0 = 1.0
E_FIRST_DOMAIN1 = 7.2

E_SECOND_DOMAIN0 = 2.0
E_SECOND_DOMAIN1 = 9.4


@pytest.fixture
def alone_state():
    return EnergyState(TS_FIRST, 'first', [[E_FIRST_DOMAIN0, E_FIRST_DOMAIN1]])


@pytest.fixture
def two_states(alone_state):
    state2 = EnergyState(TS_SECOND, 'second', [[E_SECOND_DOMAIN0, E_SECOND_DOMAIN1]])
    alone_state.add_next_state(state2)
    return alone_state


###########
# IS_LAST #
###########
def test_new_state_are_last_sate_of_trace(alone_state):
    assert alone_state.is_last()


def test_add_a_state_to_new_state_make_it_not_being_last_state_of_trace(alone_state):
    assert alone_state.is_last()
    alone_state.add_next_state(EnergyState(1, 'second', [1, 1]))
    assert not alone_state.is_last()


###########
# COMPUTE #
###########
def test_compute_duration_from_last_state_raise_NoNextStateException(alone_state):
    with pytest.raises(NoNextStateException):
        alone_state.compute_duration()


def test_compute_energy_from_last_state_raise_NoNextStateException(alone_state):
    with pytest.raises(NoNextStateException):
        alone_state.compute_energy([])


def test_compute_duration_between_two_state_return_correct_values(two_states):
    print(two_states.next_state)
    assert two_states.compute_duration() == TS_SECOND - TS_FIRST


def test_compute_energy_between_two_state_return_correct_values(two_states):
    energy = two_states.compute_energy(['domain0', 'domain1'])
    assert len(energy) == 2
    assert energy['domain0'] == E_SECOND_DOMAIN0 - E_FIRST_DOMAIN0
    assert energy['domain1'] == E_SECOND_DOMAIN1 - E_FIRST_DOMAIN1


##################
# ADD_NEXT_STATE #
##################
def test_add_a_state_to_non_final_state_raise_StateIsNotFinalError(two_states):
    with pytest.raises(StateIsNotFinalError):
        two_states.add_next_state(EnergyState(1, 'third', [1, 2]))
