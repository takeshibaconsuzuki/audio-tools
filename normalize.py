#!/usr/bin/env python3
import re
import sys
import taglib

from common import *

ACCEPTABLE_TAGS = [
    'ALBUM',
    # 'ALBUMARTIST',
    'ARTIST',
    # 'COUNTRY',
    'DATE',
    # 'DESCRIPTION',
    'DISCNUMBER',
    'GENRE',
    # 'CATALOGNUMBER',
    # 'ORGANIZATION',
    # 'RELEASEDATE',
    # 'SOURCEMEDIUM',
    'TITLE',
    'TRACKNUMBER',
    re.compile(r'^REPLAYGAIN_*'),
]


def remove_pictures(f):
    cmd = [
        'metaflac',
        '--remove',
        '--block-type=PICTURE',
        '--dont-use-padding',
        f,
    ]
    exec_cmd(cmd)


def is_acceptable_tag(t):
    for e in ACCEPTABLE_TAGS:
        if (isinstance(e, str)):
            if (e == t):
                return True
        else:
            if (e.match(t)):
                return True
    return False


def normalize_tags(f):
    song = taglib.File(f)
    for t in list(song.tags):
        if (not is_acceptable_tag(t)):
            del song.tags[t]
        if (t == 'TRACKNUMBER' or t == 'DISCNUMBER'):
            foo = song.tags[t][-1]
            if ('/' in foo):  # fix number/total form
                slash_index = foo.index('/')
                foo = foo[:slash_index]
            if (len(foo) == 1):
                foo = '0' + foo  # pad single digits with 0
            song.tags[t] = [foo]
    ret = song.save()
    if (ret):
        for k in ret.keys():
            print('%s: failed to save tag "%s"' % (f, k))


def main(argc, argv):
    if (argc != 2):
        print('usage: ' + argv[0] + ' in_dir')
        sys.exit(1)

    flac_files = rec_get_files(argv[-1], required_ext='.flac')
    for f in flac_files:
        remove_pictures(f)
        normalize_tags(f)

if (__name__ == '__main__'):
    main(len(sys.argv), sys.argv)
