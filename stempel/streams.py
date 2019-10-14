"""
Licensed to the Apache Software Foundation (ASF) under one or more
contributor license agreements.  See the NOTICE file distributed with
this work for additional information regarding copyright ownership.
The ASF licenses this file to You under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with
the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import struct
from tqdm import tqdm

class ProgressStream:

    def __init__(self, stream, total_bytes):
        self.stream = stream
        self.pbar = tqdm(total=total_bytes, desc='Loading', unit='bytes')

    def read(self, size):
        self.pbar.update(size)
        return self.stream.read(size)


class DataInputStream:
    def __init__(self, stream, total_bytes = None):
        if total_bytes is None:
            self.stream = stream
        else:
            self.stream = ProgressStream(stream, total_bytes)

    def read_boolean(self):
        return struct.unpack('?', self.stream.read(1))[0]

    def read_byte(self):
        return struct.unpack('b', self.stream.read(1))[0]

    def read_unsigned_byte(self):
        return struct.unpack('B', self.stream.read(1))[0]

    def read_char(self):
        return chr(struct.unpack('>H', self.stream.read(2))[0])

    def read_double(self):
        return struct.unpack('>d', self.stream.read(8))[0]

    def read_float(self):
        return struct.unpack('>f', self.stream.read(4))[0]

    def read_short(self):
        return struct.unpack('>h', self.stream.read(2))[0]

    def read_unsigned_short(self):
        return struct.unpack('>H', self.stream.read(2))[0]

    def read_long(self):
        return struct.unpack('>q', self.stream.read(8))[0]

    def read_utf(self):
        utf_length = struct.unpack('>H', self.stream.read(2))[0]
        return self.stream.read(utf_length).decode('utf-8')

    def read_int(self):
        return struct.unpack('>i', self.stream.read(4))[0]


class DataOutputStream:
    def __init__(self, stream):
        self.stream = stream

    def write_int(self, i):
        self.stream.write(struct.pack('>i', i))

    def write_char(self, ch):
        self.stream.write(struct.pack('>H', ch))

    def write_utf(self, s):
        self.stream.write(s.encode('utf-8'))

    def write_boolean(self, b):
        self.stream.write(struct.pack('?', b))
