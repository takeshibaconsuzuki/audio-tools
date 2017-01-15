#!/usr/bin/env python3
import os
import shutil
import sys

from common import *


def main(argc, argv):
    if (argc != 3):
        print('usage: %s in_dir out_dir' % (argv[0],))
        sys.exit(1)

    in_dir = argv[1]
    out_dir = argv[2]
    files_to_copy = rec_get_files(in_dir, required_ext='.mp3')
    files_to_copy.sort()
    for f in files_to_copy:
        same_path_part = f[len(in_dir):]
        while (same_path_part[0] == '/'):
            same_path_part = same_path_part[1:]
        out_file_path = os.path.join(out_dir, same_path_part)
        os.makedirs(os.path.dirname(out_file_path), exist_ok=True)
        shutil.copyfile(f, out_file_path)
        print('copied "%s" to "%s"' % (f, out_file_path))

if (__name__ == '__main__'):
    main(len(sys.argv), sys.argv)
