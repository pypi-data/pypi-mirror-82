# -*- coding: utf-8 -*-
# Copyright 2018-2020 releng-tool

from __future__ import print_function
from ..util.log import err
from ..util.log import log
from ..util.log import note
import contextlib
import os
import sys

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

#: size of blocks read when downloading a resource
REQUEST_READ_BLOCKSIZE = 8192

def fetch(opts):
    """
    support fetching from url sources

    With provided fetch options (``RelengFetchOptions``), the fetch stage will
    be processed.

    Args:
        opts: fetch options

    Returns:
        ``True`` if the fetch stage is completed; ``False`` otherwise
    """

    assert opts
    cache_file = opts.cache_file
    name = opts.name
    site = opts.site

    filename = os.path.basename(cache_file)

    note('fetching {}...'.format(name))
    sys.stdout.flush()

    log('requesting: ' + site)
    try:
        with contextlib.closing(urlopen(site)) as rsp:
            total = 0
            if 'content-length' in rsp.headers:
                try:
                    total = int(rsp.headers['content-length'])
                    total_str = display_size(total)
                except ValueError:
                    pass

            read = 0
            with open(cache_file, 'wb') as f:
                while True:
                    buf = rsp.read(REQUEST_READ_BLOCKSIZE)
                    if not buf:
                        break
                    read += len(buf)
                    read_str = display_size(read)

                    if total != read:
                        if total > 0:
                            pct = 100 * float(read) / float(total)
                            print('[{:02.0f}%] {}: {} of {}            '.format(
                                pct, filename, read_str, total_str), end='\r')
                        else:
                            print(' {}: {}            '.format(
                                filename, read_str), end='\r')

                    f.write(buf)
    except Exception as e:
        err('failed to download resource')
        err('    {}'.format(e))
        return None

    log('completed download ({})', display_size(read))
    return cache_file

def display_size(val):
    """
    return a human-readable count value for the provided byte count

    Accepts a byte count value and returns a string with a count value and
    binary prefix which describes the respective size.

    Args:
        val: the value (in bytes) to interpret

    Returns:
        the human-readable size
    """
    for unit in ['B', 'KiB', 'MiB', 'GiB']:
        if abs(val) < 1024.:
            return '{:3.1f} {}'.format(val, unit)
        val /= 1024.

    return '{:.1f} TiB'.format(val)
