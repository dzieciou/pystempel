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
from sortedcontainers import SortedDict

from stempel.streams import DataInputStream, DataOutputStream

DASH_COMMAND = '-'
DELETE_COMMAND = 'D'
INSERT_COMMAND = 'I'
REPLACE_COMMAND = 'R'


def reverse(s):
    return s[::-1]


class Cell:
    """
    A Cell is a portion of a trie.
    """

    def __init__(self, ref=-1, cmd=-1, cnt=0, skip=0):
        """
        :param ref: next row id in this way
        :param cmd: command of the cell
        :param cnt: how many cmd-s was in subtrie before pack()
        :param skip: how many chars would be discarded from input key in this
                     way
        """
        self.ref = ref
        self.cmd = cmd
        self.cnt = cnt
        self.skip = skip

    @classmethod
    def from_cell(cls, old):
        """
        Construct a Cell using the properties of the given Cell.
        :param old: a the Cell whose properties will be used
        """
        return Cell(ref=old.ref, cmd=old.cmd, cnt=old.cnt, skip=old.skip)

    def is_in_use(self):
        return self.cmd >= 0 or self.ref >= 0

    def __str__(self):
        return 'ref(%s)cmd(%s)cnt(%s)skp({%s})'.format(self.ref,
                                                       self.cmd,
                                                       self.cnt,
                                                       self.skip)

    def __repr__(self):
        return self.__str__()


class Row:
    """
    The Row class represents a row in a matrix representation of a trie.
    """
    uniform_cnt = 0
    uniform_skip = 0

    @classmethod
    def from_stream(cls, stream: DataInputStream):
        cells = SortedDict()
        cells_count = stream.read_int()
        for _ in range(cells_count):
            ch = stream.read_char()
            cell = Cell(cmd=stream.read_int(),
                        cnt=stream.read_int(),
                        ref=stream.read_int(),
                        skip=stream.read_int())
            cells[ch] = cell
        return Row(cells)

    @classmethod
    def from_row(cls, old):
        # TODO mutability! perhaps copying content instead of assigning pointer
        return Row(old.cells)

    def __init__(self, cells=None):
        self.cells = SortedDict() if cells is None else cells

    def set_cmd(self, way, cmd):
        """
        Set the command in the Cell of the given Character to the given integer.
        :param way: the Character defining the Cell
        :param cmd: the new command
        """
        try:
            cell = self.cells[way]
            cell.cmd = cmd
        except KeyError:
            cell = Cell(cmd=cmd)
            self.cells[way] = cell
        cell.cnt = 1 if cmd >= 0 else 0

    def set_ref(self, way, ref):
        """
        Set the reference to the next row in the Cell of the given Character to
        the given integer.
        :param way: the Character defining the Cell
        :param ref: The new ref value
        """
        try:
            cell = self.cells[way]
            cell.ref = ref
        except KeyError:
            cell = Cell(ref=ref)
            self.cells[way] = cell

    def get_cells(self):
        """
        Return the number of cells in use.
        """
        return sum([cell.is_in_use() for _, cell in self.cells.items()])

    def get_cells_pnt(self):
        """
        Return the number of references (how many transitions) to other rows.
        """
        return sum([(cell.ref >= 0) for _, cell in self.cells.items()])

    def get_cells_val(self):
        """
        Return the number of patch commands saved in this Row.
        """
        return sum([(cell.cmd >= 0) for _, cell in self.cells.items()])

    def get_cmd(self, way):
        """
        Return the command in the Cell associated with the given Character.
        :param way: the Character associated with the Cell holding the desired
        command
        :return: the command, or -1 if no Cell defined for the given way
        """
        try:
            return self.cells[way].cmd
        except KeyError:
            return -1

    def get_cnt(self, way):
        """
        Return the number of patch commands were in the Cell associated with the
        given Character before the Trie containing this Row was reduced.
        :param way: he Character associated with the desired Cell
        :return: the number of patch commands before reduction, or -1 if no Cell
         defined for the given way
        """
        try:
            return self.cells[way].cnt
        except KeyError:
            return -1

    def get_ref(self, way):
        """
        Return the reference to the next Row in the Cell associated with the
        given Character.
        :param way: the Character associated with the desired Cell
        :return:  the reference, or -1 if no Cell defined for the given way
        """
        try:
            return self.cells[way].ref
        except KeyError:
            return -1

    def store(self, out: DataOutputStream):
        """
        Write the contents of this Row to the given output stream.
        :param out: the output stream
        """
        for c, cell in self.cells.items():
            if cell.is_in_use():
                out.write_char(c)
                out.write_int(cell.cmd)
                out.write_int(cell.cnt)
                out.write_int(cell.ref)
                out.write_int(cell.skip)

    def uniform_cmd(self, eq_skip):
        """
        Return the number of identical Cells (containing patch commands) in this
        Row.
        :param eq_skip: when set to <tt>false</tt> the removed patch commands
               are considered
        :return: the number of identical Cells, or -1 if there are (at least)
                 two different cells
        """

        ret = -1
        self.uniform_cnt = 1
        self.uniform_skip = 0
        for _, cell in self.cells.items():
            if cell.ref >= 0:
                return -1
            if cell.cmd >= 0:
                if ret >= 0:
                    return -1
                elif ret == cell.cmd:
                    if eq_skip:
                        if self.uniform_skip == cell.skip:
                            self.uniform_cnt += 1
                        else:
                            return -1
                    else:
                        self.uniform_cnt += 1
                else:
                    ret = cell.cmd
                    self.uniform_skip = cell.skip
        return ret


def __str__(self):
    return str(['[%s:%s]'.format(ch, cell)
                for ch, cell
                in self.cells.items()])


class Reduce:
    """
    The Reduce object is used to remove gaps in a Trie which stores a
    dictionary.
    """

    def optimize(self, orig):
        """
        Optimize (remove holes in the rows) the given Trie and return the
        restructured Trie.
        :param orig: the Trie to optimize
        :return: the restructured Trie
        """
        rows = []
        remap = [-1] * len(orig.rows)
        rows = self._remove_gaps(ind=orig.root,
                                 old_rows=rows,
                                 to_rows=[],
                                 remap=remap)
        return Trie(forward=orig.forward,
                    root=remap[orig.root],
                    cmds=orig.cmds,
                    rows=rows)

    def _remove_gaps(self, ind, old_rows, to_rows, remap):
        remap[ind] = len(to_rows)
        now = old_rows[ind]
        to_rows.append(now)
        for _, cell in now.cells.items():
            if cell.ref >= 0 > remap[cell.ref]:
                self._remove_gaps(cell.ref, old_rows, to_rows, remap)
        to_rows[remap[ind]] = Remap(now, remap)
        return to_rows


class Trie:

    @classmethod
    def from_stream(cls, stream: DataInputStream):
        forward = stream.read_boolean()
        root = stream.read_int()
        cmds = []
        cmds_count = stream.read_int()
        for _ in range(cmds_count):
            cmds.append(stream.read_utf())
        rows = []
        rows_count = stream.read_int()
        for _ in range(rows_count):
            rows.append(Row.from_stream(stream))
        return Trie(forward=forward, root=root, cmds=cmds, rows=rows)

    def __init__(self, forward=False, root=0, cmds=None, rows=None):
        self.rows = [Row()] if rows is None else rows
        self.cmds = [] if cmds is None else cmds
        self.root = root
        self.forward = forward

    def __get_row(self, index):
        try:
            return self.rows[index]
        except IndexError:
            return None

    def get_cells(self):
        return sum([row.get_cells() for row in self.rows])

    def get_cells_pnt(self):
        return sum([row.get_cells_pnt() for row in self.rows])

    def get_cells_val(self):
        return sum([row.get_cells_val() for row in self.rows])

    def get_fully(self, key):
        """
        Return the element that is stored in a cell associated with the given
        key.
        :param key: the key
        :return: the associated element
        """
        now = self.__get_row(self.root)
        cmd = -1
        if not self.forward:
            key = reverse(key)

        i = 0
        while i < len(key):
            ch = key[i]
            i += 1

            cell = now.cells[ch]
            if cell is None:
                return None

            cmd = cell.cmd

            skip = cell.skip
            while skip > 0:
                if cell.skip > 0:
                    if i >= len(key):
                        return None
                    i += 1
                    skip -= 1

            w = now.get_ref(ch)
            if w >= 0:
                now = self.__get_row(w)
            elif i < len(key):
                return None

        return None if cmd == -1 else self.cmds[cmd]

    def get_last_on_path(self, key):
        """
        Return the element that is stored as last on a path associated with the
        given key.
        :param key: the key associated with the desired element
        :return:  the last on path element
        """
        last = None
        now = self.__get_row(self.root)
        if not self.forward:
            key = reverse(key)
        for ch in key[:-1]:
            w = now.get_cmd(ch)
            if w >= 0:
                last = self.cmds[w]
            w = now.get_ref(ch)
            if w >= 0:
                now = self.__get_row(w)
            else:
                return last
        w = now.get_cmd(key[-1])
        return self.cmds[w] if w >= 0 else last

    def store(self, out: DataOutputStream):
        out.write_boolean(self.forward)
        out.write_int(self.root)
        out.write_int(len(self.cmds))
        for cmd in self.cmds:
            out.write_utf(cmd)
        out.write_int(len(self.rows))
        for row in self.rows:
            row.store(out)

    def add(self, key, cmd):
        """
        Add the given key associated with the given patch command. If either
        parameter is null this method will return without executing.
        :param key: the key
        :param cmd: the patch command
        """
        if key is None or cmd is None:
            return
        if not cmd:
            return

        try:
            id_cmd = self.cmds.index(cmd)
        except ValueError:
            id_cmd = len(self.cmds)
            self.cmds.append(cmd)

        node = self.root
        row = self.__get_row(node)
        if not self.forward:
            key = reverse(key)
        for ch in key[:-1]:
            node = row.get_ref(ch)
            if node >= 0:
                row = self.__get_row(node)
            else:
                node = len(self.rows)
                new = Row()
                self.rows.append(new)
                row.set_ref(ch, node)
                row = new

        row.set_cmd(key[-1], id_cmd)

    def reduce(self, by: Reduce):
        """
        Remove empty rows from the given Trie and return the newly reduced Trie.
        :param by: the Trie to reduce
        :return: the newly reduced Trie
        """
        return by.optimize(self)

    def print_info(self, prefix):
        print('prefix %s nds %d cmds %d '
              'cells %s valcells %s'
              'pntcells %s'.format(prefix,
                                   len(self.rows),
                                   len(self.cmds),
                                   self.get_cells(),
                                   self.get_cells_val(),
                                   self.get_cells_pnt()
                                   ))


class Remap(Row):
    """
    This class is part of the Egothor Project
    """

    def __init__(self, old_row, remap):
        super().__init__()
        for ch, cell in old_row.cells.items():
            new_cell = Cell.from_cell(cell)
            if cell.ref >= 0:
                new_cell.ref = remap[new_cell.ref]
            self.cells[ch] = new_cell


class Optimizer(Reduce):

    def optimize(self, orig):
        cmds = orig.cmds
        rows = []
        orig_rows = orig.rows
        remap = [0] * len(orig.rows)

        for j in range(len(orig_rows) - 1, -1, -1):

            now = Remap(orig_rows[j], remap)
            merged = False

            for i in range(len(rows)):
                q = self._merge_rows(now, rows[i])
                if q is not None:
                    rows[i] = q
                    merged = True
                    remap[j] = i
                    break

            if not merged:
                remap[j] = len(rows)
                rows.append(now)

        root = remap[orig.root]
        remap = [-1] * len(orig.rows)
        rows = self._remove_gaps(root, rows, [], remap)
        return Trie(orig.forward, remap[root], cmds, rows)

    def _merge_rows(self, master, existing):
        """
        Merge the given rows and return the resulting Row.
        :param master: the master Row
        :param existing:  the existing Row
        :return: the resulting Row, or None if the operation cannot be
                 realized
        """
        new_row = Row()
        for ch in master.cells:
            # TODO (from original author) XXX also must handle Cnt and Skip !!
            a = master.cells[ch]
            try:
                b = existing.cells[ch]
            except KeyError:
                b = None
            s = Cell.from_cell(a) if b is None else self._merge_cells(a, b)
            if s is None:
                return None
            new_row.cells[ch] = s
        for ch, cmd in existing.cells.items():
            if master.get_cmd(ch) is not None:
                continue
            new_row.cells[ch] = existing.get_cmd[ch]
        return new_row

    def _merge_cells(self, m, e):
        """
        Merge the given Cells and return the resulting Cell.
        :param m: the master Cell
        :param e: the existing Cell
        :return: the resulting Cell, or None if the operation cannot be
                 realized
        """

        n = Cell()
        if m.skip != e.skip:
            return None

        if m.cmd >= 0:
            if e.cmd >= 0:
                if m.cmd == e.cmd:
                    n.cmd = m.cmd
                else:
                    return None
            else:
                n.cmd = m.cmd
        else:
            n.cmd = e.cmd

        if m.ref >= 0:
            if e.ref >= 0:
                if m.ref == e.ref:
                    if m.skip == e.skip:
                        n.ref = m.ref
                    else:
                        return None
                else:
                    return None
            else:
                n.ref = m.ref
        else:
            n.ref = m.ref

        n.cnt = m.cnt + e.cnt
        n.skip = m.skip
        return n


class Optimizer2(Optimizer):
    """
    The Optimizer class is a Trie that will be reduced (have empty rows
    removed).

    This is the result of allowing a joining of rows when there is no collision
    between non-None values in the rows. Information loss, resulting in
    the stemmer not being able to recognize words (as in Optimizer), is
    curtailed, allowing the stemmer to recognize words for which the original
    trie was built. Use of this class allows the stemmer to be self-teaching.
    """

    def _merge_cells(self, m, e):
        """
        Merge the given Cells and return the resulting Cell.
        :param m: the master Cell
        :param e: the existing Cell
        :return: the resulting Cell, or <tt>null</tt> if the operation cannot
                 be realized
        """
        if m.cmd == e.cmd and m.ref == e.ref and m.skip == e.skip:
            c = Cell.from_cell(m)
            c.cnt += e.cnt
            return c
        else:
            return None


class Gener(Reduce):
    """
    The Gener object helps in the discarding of nodes which break the reduction
    effort and defend the structure against large reductions.
    """

    def optimize(self, orig):
        """
        Return a Trie with infrequent values occurring in the given Trie
        removed.
        :param orig: the Trie to optimize
        :return: a new optimized Trie
        """
        cmds = orig.cmds
        orig_rows = orig.rows
        remap = [1] * len(orig_rows)

        j = len(orig_rows) - 1
        while j >= 0:
            if self.__eat(orig_rows[j], remap):
                remap[j] = 0
            j -= 1

        remap = [-1] * len(orig_rows)
        rows = self._remove_gaps(ind=orig.root, old_rows=orig_rows,
                                 to_rows=[], remap=remap)
        return Trie(forward=orig.forward, root=remap[orig.root], cmds=cmds,
                    rows=rows)

    @staticmethod
    def __eat(in_row, remap):
        """
        Test whether the given Row of Cells in a Trie should be included in an
        optimized Trie.
        :param in_row: the Row to test
        :param remap:
        :return:  True if the Row should remain, False otherwise
        """
        sum_ = 0
        for _, cell in in_row.cells.items():
            sum_ += cell.cnt
            if cell.ref >= 0 and remap[cell.ref] == 0:
                cell.ref = -1

        frame = int(sum_ / 10)
        live = False
        for _, cell in in_row.cells.items():
            if cell.cnt < frame and cell.cmd > 0:
                cell.cnt = 0
                cell.cmd = -1
            if cell.cmd >= 0 or cell.ref >= 0:
                live |= True

        return not live


class Lift(Reduce):
    """
    The Lift class is a data structure that is a variation of a Patricia trie.
    Lift's raison d'etre is to implement reduction of the trie via the
    Lift-Up method., which makes the data structure less liable to overstemming.
    """

    def __init__(self, change_skip):
        """
        Constructor for the Lift object.
        :param change_skip: when set to <tt>true</tt>, comparison of two Cells
               takes a skip command into account
        """
        super().__init__()
        self.change_skip = change_skip

    def optimize(self, orig):
        # TODO Original implementation didn't care about mutability! Do we?
        cmds = orig.cmds
        orig_rows = orig.rows
        for j in range(len(orig_rows) - 1, -1, -1):
            self.__lift_up(orig_rows[j], orig_rows)

        remap = [-1] * len(orig.rows)
        rows = self._remove_gaps(ind=orig.root, old_rows=orig_rows,
                                 to_rows=[], remap=remap)
        # TODO When to provide parameter names in invokation?
        return Trie(orig.forward, remap[orig.root], cmds, rows)

    def __lift_up(self, in_row, nodes):
        for _, cell in in_row.cells.items():

            if cell.ref < 0:
                continue

            to_row = nodes[cell.ref]
            sum_ = to_row.uniform_cmd(self.change_skip)
            if sum_ < 0:
                continue

            if sum_ == cell.cmd:
                if self.change_skip:
                    if cell.skip != to_row.uniform_skip + 1:
                        continue
                    # TODO Hmm, skip will be updated to X if it is already
                    #      equal to X
                    #      Perhaps I should check the original algorithm?
                    cell.skip = to_row.uniform_skip + 1
                else:
                    cell.skip = 0
                cell.cnt += to_row.uniform_cnt
                cell.ref = -1
            elif cell.cmd < 0:
                cell.cnt = to_row.uniform_cnt
                cell.cmd = sum_
                cell.ref = -1
                if self.change_skip:
                    cell.skip = to_row.uniform_skip + 1
                else:
                    cell.skip = 0


class MultiTrie(Trie):
    """
    The MultiTrie is a Trie of Tries. It stores words and their associated patch
    commands. The MultiTrie handles patch commands individually (each command by
    itself).
    """

    EOM = '*'
    EOM_NODE = EOM


    BY = 1

    @classmethod
    def from_stream(cls, stream: DataOutputStream, constructor):
        t = constructor()
        t.forward = stream.read_boolean()
        t.BY = stream.read_int()
        tries_count = stream.read_int()
        for _ in range(tries_count):
            t.tries.append(Trie.from_stream(stream))
        return t

    def __init__(self, forward=True):
        """
        Constructor for the MultiTrie object
        :param forward: set to True if the elements should be read left to
             right
        """
        super().__init__(forward=forward)
        self.tries = []

    def get_fully(self, key):
        """
        Return the element that is stored in a cell associated with the given
        key.
        :param key: the key to the cell holding the desired element
        :return: the element
        """
        result = ''
        for trie in self.tries:
            r = trie.get_fully(key)
            if r is None or (len(r) == 1 and r[0] == self.EOM):
                return result
            result += r
        return result

    def get_last_on_path(self, key):
        """
         Return the element that is stored as last on a path belonging to the
         given key.
        :param key: the key associated with the desired element
        :return: the element that is stored as last on a path
        """
        result = ''
        for trie in self.tries:
            r = trie.get_last_on_path(key)
            if r is None or (len(r) == 1 and r[0] == self.EOM):
                return result
            result += r
        return result

    def store(self, output: DataOutputStream):
        """
        Write this data structure to the given output stream.
        :param output: the output stream
        """
        output.write_boolean(self.forward)
        output.write_int(self.BY)
        output.write_int(len(self.tries))
        for trie in self.tries:
            trie.store(output)

    def add(self, key, cmd):
        """
        Add an element to this structure consisting of the given key and patch
        command.

        This method will return without executing if the <tt>cmd</tt>
        parameter's length is 0.

        :param key: the key
        :param cmd: the patch command
        :return:
        """
        if not cmd:
            return
        levels = int(len(cmd) / self.BY)
        while levels >= len(self.tries):
            self.tries.append(Trie(forward=self.forward))
        for i in range(0, levels):
            start = self.BY * i
            end = start + self.BY
            self.tries[i].add(key, cmd[start:end])
        self.tries[levels].add(key, self.EOM_NODE)

    def reduce(self, by):
        """
        Remove empty rows from the given Trie and return the newly reduced Trie.
        :param by: the Trie to reduce
        :return: the newly reduced Trie
        """
        h = []
        for trie in self.tries:
            h.append(trie.reduce(by))

        m = MultiTrie(forward=self.forward)
        m.tries = h
        return m

    def print_info(self, prefix):
        c = 0
        for trie in self.tries:
            c += 1
            trie.print_info('%s [%d] '.format(prefix, c))


class MultiTrie2(MultiTrie):
    """
    The MultiTrie is a Trie of Tries.

    It stores words and their associated patch commands. The MultiTrie handles
    patch commands broken into their constituent parts, as a MultiTrie does, but
    the commands are delimited by the skip command.
    """

    @classmethod
    def from_stream(cls, stream):
        trie = MultiTrie.from_stream(stream, MultiTrie2)
        return trie

    def __init__(self, forward=True):
        """
        Constructor for the MultiTrie2 object
        :param forward: set to True if the elements should be read left to
                        right
        :return:
        """
        super().__init__(forward)

    def get_fully(self, key):
        result = ''
        last_key = key
        p = [' '] * len(self.tries)
        last_ch = ' '
        for i in range(len(self.tries)):
            r = self.tries[i].get_fully(last_key)
            if r is None or (len(r) == 1 and r[0] == self.EOM):
                return result
            if self.__cannot_follow(last_ch, r[0]):
                return result
            else:
                last_ch = r[len(r) - 2]
            p[i] = r
            if p[i][0] == DASH_COMMAND:
                if i > 0:
                    key = self.__skip(key, self.__length_pp(p[i - 1]))
                key = self.__skip(key, self.__length_pp(p[i]))
            result += r
            if key:
                last_key = key

        return result

    def get_last_on_path(self, key):
        """
        Return the element that is stored as last on a path belonging to the
        given key.
        :param key: the key associated with the desired element
        :return: the element that is stored as last on a path
        """
        # TODO add catching IndexError
        result = ''
        last_key = key
        p = [None] * len(self.tries)
        last_ch = ' '
        for i in range(len(self.tries)):
            r = self.tries[i].get_last_on_path(last_key)
            if r is None or (len(r) == 1 and r[0] == self.EOM):
                return result
            if self.__cannot_follow(last_ch, r[0]):
                return result
            else:
                last_ch = r[-2]
            p[i] = r
            if p[i][0] == DASH_COMMAND:
                if i > 0:
                    key = self.__skip(key, self.__length_pp(p[i - 1]))
                    if key is None:
                        return result
                key = self.__skip(key, self.__length_pp(p[i]))
                if key is None:
                    return result
            result += r
            if key:
                last_key = key

        return result

    def store(self, output: DataOutputStream):
        """
        Write this data structure to the given output stream.
        :param output: the output stream
        """
        super().store(output)

    def add(self, key, cmd):
        if not cmd:
            return

        p = self.__decompose(cmd)
        levels = len(p)
        while levels >= len(self.tries):
            self.tries.append(Trie(self.forward))

        last_key = key
        for i in range(0, levels):
            if key:
                self.tries[i].add(key, p[i])
                last_key = key
            else:
                self.tries[i].add(last_key, p[i])
            if p[i] and p[i][0] == DASH_COMMAND:
                if i > 0:
                    key = self.__skip(key, self.__length_pp(p[i - 1]))
                key = self.__skip(key, self.__length_pp(p[i]))

        if key:
            self.tries[levels].add(key, self.EOM_NODE)
        else:
            self.tries[levels].add(last_key, self.EOM_NODE)

    def __decompose(self, cmd):
        """
        Break the given patch command into its constituent pieces. The pieces
        are delimited by NOOP commands.
        :param cmd: the patch command
        :return: an array containing the pieces of the command
        """
        parts = 0
        i = 0
        while 0 <= i < len(cmd):
            next_ = self.__dash_even(cmd, i)
            parts += 1
            i = next_ + 2 if i == next_ else next_

        part = list(' ' * parts)
        x = 0
        i = 0
        while 0 <= i < len(cmd):
            next_ = self.__dash_even(cmd, i)
            if i == next_:
                part[x] = cmd[i:i + 2]
                i = next_ + 2
            else:
                part[x] = cmd[i:len(cmd)] if next_ < 0 else cmd[i:next_]
                i = next_
            x += 1
        return part

    def reduce(self, by):
        """
        Remove empty rows from the given Trie and return the newly reduced Trie.
        :param by: the Trie to reduce
        :return: the newly reduced Trie
        """
        h = []
        for trie in self.tries:
            h.append(trie.reduce(by))
        m = MultiTrie2(self.forward)
        m.tries = h
        return m

    @staticmethod
    def __cannot_follow(after, goes):
        return after in [DASH_COMMAND, DELETE_COMMAND] and after == goes

    def __skip(self, s, count):
        if self.forward:
            return s[count:len(s)]
        else:
            return None if len(s) < count else s[0:len(s) - count]

    @staticmethod
    def __dash_even(s, from_):
        while from_ < len(s):
            if s[from_] == DASH_COMMAND:
                return from_
            else:
                from_ += 2
        return -1

    @staticmethod
    def __length_pp(cmd):
        length = 0
        i = 0
        while i < len(cmd):
            if cmd[i] in [DASH_COMMAND, DELETE_COMMAND]:
                length += ord(cmd[i + 1]) - ord('a') + 1
            elif cmd[i] == REPLACE_COMMAND:
                length += 1
            elif cmd[i] == INSERT_COMMAND:
                pass
            i += 2

        return length


def apply_patch(destination, patch):
    """
    A patch string is actually a command to a stemmer telling it how to reduce a
    word to its root. For example, to reduce the word teacher to its root teach
    the patch string Db would be generated. This command tells the stemmer to
    delete the last 2 characters from the word teacher to reach the stem (the
    patch commands are applied starting from the last character in order to save
    :param destination: Destination string
    :param patch: Patch string
    """

    def parse(patch):
        for i in range(int(len(patch) / 2)):
            cmd = patch[2 * i]
            letter = patch[2 * i + 1]
            offset = ord(letter) - ord('a')
            yield cmd, letter, offset

    if patch is None:
        return
    if not destination:
        return

    position = len(destination) - 1
    for cmd, letter, offset in parse(patch):
        if cmd == DASH_COMMAND:
            position -= offset
        elif cmd == REPLACE_COMMAND:
            if position < 0 or position >= len(destination):
                return
            destination[position] = letter
        elif cmd == DELETE_COMMAND:
            original_position = position
            position -= offset
            if position < 0 or position >= len(destination):
                return
            destination[position:original_position + 1] = ''
        elif cmd == INSERT_COMMAND:
            position += 1
            if position < 0 or position > len(destination):
                return
            destination.insert(position, letter)
        position -= 1
