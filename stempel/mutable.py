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


class MutableString(object):
    def __init__(self, data):
        if not isinstance(data, str):
            raise ValueError
        self.data = list(data)

    def __repr__(self):
        return ''.join(self.data)

    def __setitem__(self, index, value):
        self.data[index] = value

    def __getitem__(self, index):
        if type(index) == slice:
            return ''.join(self.data[index])
        return self.data[index]

    def __delitem__(self, index):
        del self.data[index]

    def __add__(self, other):
        self.data.extend(list(other))

    def __len__(self):
        return len(self.data)

    def insert(self, index, obj):
        self.data.insert(index, obj)
