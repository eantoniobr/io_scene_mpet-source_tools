# ioutil.py - Just some simple utilities for reading/writing C-style data.
# Every project has to have it's own little utility functions. It sucks but
# it's better than repeating yourself ad nauseum.

import struct

def wraptext(s, w):
    return [s[i:i + w] for i in range(0, len(s), w)]

# read_struct reads struct data from a file-like object
def read_struct(file, fmt):
    size = struct.calcsize(fmt)
    data = file.read(size)

    if len(data) < size:
        print('warning: short struct read (%i < %i)' % (len(data), size))

    return struct.unpack(fmt, data)


# write_struct writes struct data to a file-like object
def write_struct(file, fmt, *args):
    file.write(struct.pack(fmt, *args))


# read_cstr reads a C-style string (and returns a `bytes` object.)
def read_cstr(file):
    buf = bytearray()
    while True:
        b = file.read(1)
        if b == '' or b == b'\x00':
            return bytes(buf)
        else:
            buf.append(ord(b))

# write_cstr writes a C-style string
def write_cstr(file, buf):
    file.write(buf + '\x00')


def read_fixed_string(file):
    length, = read_struct(file, '<I')

    if length <= 0:
        return b''
    
    return read_struct(file, "<{}s".format(length))[0].split(b'\x00')[0]

def write_fixed_string(file, buff):
    length = len(buff)

    write_struct(file, '<I', length)

    if length > 0:
        file.write(buff)