"""
                    Egothor Software License version 1.00
                    Copyright (C) 1997-2004 Leo Galambos.
                 Copyright (C) 2002-2004 "Egothor developers"
                      on behalf of the Egothor Project.
                             All rights reserved.

   This  software  is  copyrighted  by  the "Egothor developers". If this
   license applies to a single file or document, the "Egothor developers"
   are the people or entities mentioned as copyright holders in that file
   or  document.  If  this  license  applies  to the Egothor project as a
   whole,  the  copyright holders are the people or entities mentioned in
   the  file CREDITS. This file can be found in the same location as this
   license in the distribution.

   Redistribution  and  use  in  source and binary forms, with or without
   modification, are permitted provided that the following conditions are
   met:
    1. Redistributions  of  source  code  must retain the above copyright
       notice, the list of contributors, this list of conditions, and the
       following disclaimer.
    2. Redistributions  in binary form must reproduce the above copyright
       notice, the list of contributors, this list of conditions, and the
       disclaimer  that  follows  these  conditions  in the documentation
       and/or other materials provided with the distribution.
    3. The name "Egothor" must not be used to endorse or promote products
       derived  from  this software without prior written permission. For
       written permission, please contact Leo.G@seznam.cz
    4. Products  derived  from this software may not be called "Egothor",
       nor  may  "Egothor"  appear  in  their name, without prior written
       permission from Leo.G@seznam.cz.

   In addition, we request that you include in the end-user documentation
   provided  with  the  redistribution  and/or  in the software itself an
   acknowledgement equivalent to the following:
   "This product includes software developed by the Egothor Project.
    http://egothor.sf.net/"

   THIS  SOFTWARE  IS  PROVIDED  ``AS  IS''  AND ANY EXPRESSED OR IMPLIED
   WARRANTIES,  INCLUDING,  BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
   MERCHANTABILITY  AND  FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
   IN  NO  EVENT  SHALL THE EGOTHOR PROJECT OR ITS CONTRIBUTORS BE LIABLE
   FOR   ANY   DIRECT,   INDIRECT,  INCIDENTAL,  SPECIAL,  EXEMPLARY,  OR
   CONSEQUENTIAL  DAMAGES  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
   SUBSTITUTE  GOODS  OR  SERVICES;  LOSS  OF  USE,  DATA, OR PROFITS; OR
   BUSINESS  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
   WHETHER  IN  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
   OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
   IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

   This  software  consists  of  voluntary  contributions  made  by  many
   individuals  on  behalf  of  the  Egothor  Project  and was originally
   created by Leo Galambos (Leo.G@seznam.cz).
"""

import pytest

from pystempel.egothor import (
    Trie,
    MultiTrie,
    MultiTrie2,
    Optimizer,
    Optimizer2,
    Gener,
    Lift,
)


def test_trie_forward():
    trie = Trie(forward=True)

    keys = ["a", "ba", "bb", "c"]
    vals = ["1", "2", "2", "4"]
    for key, val in zip(keys, vals):
        trie.add(key, val)

    assert 0 == trie.root
    assert 2 == len(trie.rows)
    assert 3 == len(trie.cmds)
    assert_trie_content(trie, keys, vals)


def test_trie_backward():
    trie = Trie(forward=False)

    keys = ["a", "ba", "bb", "c"]
    vals = ["1", "2", "2", "4"]
    for key, val in zip(keys, vals):
        trie.add(key, val)

    assert_trie_content(trie, keys, vals)


@pytest.mark.parametrize("forward", [True, False])
def test_multitrie(forward):
    trie = MultiTrie(forward=forward)

    keys = ["a", "ba", "bb", "c"]
    vals = ["1", "2", "2", "4"]
    for key, val in zip(keys, vals):
        trie.add(key, val)

    assert_trie_content(trie, keys, vals)


@pytest.mark.parametrize("forward", [True, False])
def test_multitrie2(forward):
    trie = MultiTrie2(forward=forward)

    keys = ["a", "ba", "bb", "c"]
    # FIXME short vals won't work, see line 155 for example
    #       the IOOBE is caught (wierd), but shouldnt affect patch cmds?
    vals = ["1111", "2222", "2223", "4444"]
    for key, val in zip(keys, vals):
        trie.add(key, val)

    assert_trie_content(trie, keys, vals)


def assert_trie_content(trie, keys, vals):
    tries = [
        trie,
        trie.reduce(Optimizer()),
        trie.reduce(Optimizer2()),
        trie.reduce(Gener()),
        trie.reduce(Lift(change_skip=True)),
        trie.reduce(Lift(change_skip=False)),
    ]
    for trie in tries:
        for key, val in zip(keys, vals):
            assert val == trie.get_fully(key)
            assert val == trie.get_last_on_path(key)
