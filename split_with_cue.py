#!/usr/bin/env python3
import os
import shutil
import sys

from common import *


def remove_bom_header(bom_file):
    s = open(bom_file, mode='r', encoding='utf-8-sig').read()
    open(bom_file, mode='w', encoding='utf-8').write(s)


def tag_new_flacs(prev_flac_files, curr_flac_files, cf, src_flac):
    new_flacs = list(set(curr_flac_files) - set(prev_flac_files))
    for f in new_flacs:
        if (os.path.basename(f).startswith('00 - ')):  # remove pregap tracks
            os.remove(f)
            curr_flac_files.remove(f)
            new_flacs.remove(f)
    new_flacs.sort()  # track order
    if (shutil.which('cuetag.sh') != None):
        cmd = ['cuetag.sh', cf] + new_flacs
    elif (shutil.which('cuetag') != None):
        cmd = ['cuetag', cf] + new_flacs
    else:
        print('cuetools is not installed')
        return
    is_success = exec_cmd(cmd) == 0
    if (is_success):
        os.remove(cf)
        os.remove(src_flac)


def main(argc, argv):
    if (argc != 2):
        print('usage: %s directory_path' % (argv[0],))
        sys.exit(1)

    directory_path = argv[1]
    cue_files = rec_get_files(directory_path, '.cue')
    prev_flac_files = rec_get_files(directory_path, '.flac')
    for cf in cue_files:
        remove_bom_header(cf)  # cuetag.sh doesn't like BOMs
        src_flac = os.path.splitext(cf)[0]
        if (not src_flac.endswith('.flac')):
            src_flac += '.flac'
        if (not os.path.isfile(src_flac)):
            continue
        cf_dir = os.path.dirname(cf)
        cmd = [
            'shnsplit',
            '-d', cf_dir,
            '-f', cf,
            '-o', 'flac',
            '-t', '%n - %t',
            src_flac,
        ]
        print('============================================================')
        print('Doing "%s"...' % (os.path.basename(src_flac),))
        print('============================================================')
        is_success = exec_cmd(cmd) == 0
        curr_flac_files = rec_get_files(directory_path, '.flac')
        if (is_success):
            tag_new_flacs(prev_flac_files, curr_flac_files, cf, src_flac)
        prev_flac_files = curr_flac_files

if (__name__ == '__main__'):
    main(len(sys.argv), sys.argv)
