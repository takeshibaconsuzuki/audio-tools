#!/usr/bin/env python3
import os
import sys

from common import *


def main(argc, argv):
    if (argc != 2):
        print('usage: %s directory_path' % (argv[0],))
        sys.exit(1)

    directory_path = argv[1]
    files_to_convert = rec_get_files(directory_path, required_ext='.m4a')
    files_to_convert += rec_get_files(directory_path, required_ext='.ape')
    for f in files_to_convert:
        cmd = [
            'ffmpeg',
            '-i', f,
            '-c:a', 'flac',
            os.path.splitext(f)[0] + '.flac',
        ]
        is_success = exec_cmd(cmd) == 0
        if (is_success):
            os.remove(f)

if (__name__ == '__main__'):
    main(len(sys.argv), sys.argv)
