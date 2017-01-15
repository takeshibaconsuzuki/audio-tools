#!/usr/bin/env python3
import os
import sys
import taglib

from common import *


def sort_by_album_tag(flac_files):
    ret = {}
    for f in flac_files:
        song = taglib.File(f)
        k = ''
        if ('ALBUMARTIST' in song.tags):
            k = '; '.join(song.tags['ALBUMARTIST'])
        elif ('ALBUM ARTIST' in song.tags):
            k = '; '.join(song.tags['ALBUM ARTIST'])
        elif ('ARTIST' in song.tags):
            k = '; '.join(song.tags['ARTIST'])
        else:
            print('warning: ' + f + ' has no artist, skipping')
            continue
        if ('ALBUM' not in song.tags):
            print('warning: ' + f + ' has no album, skipping')
            continue
        k += ' - ' + song.tags['ALBUM'][-1]
        if (k in ret):
            ret[k].append(f)
        else:
            ret[k] = [f]
    return ret


def show_prompt_get_resp(sorted_by_album):
    nothing_to_do = True
    for k, songs in sorted_by_album.items():
        if (songs == None):
            continue
        nothing_to_do = False
        print('"' + k + '":')
        for song in songs:
            print('\t' + os.path.basename(song))
    if (nothing_to_do):
        print('nothing to do')
        sys.exit(1)
    resp = input('\nDoes this look right to you? [Y/n]: ')
    if (resp == 'n' or resp == 'N'):
        sys.exit(1)


def main(argc, argv):
    if (argc != 2):
        print('usage: %s directory_path' % (argv[0],))
        sys.exit(1)

    flac_files = rec_get_files(argv[1], required_ext='.flac')
    flac_files.sort()

    sorted_by_album = sort_by_album_tag(flac_files)

    for k, v in sorted_by_album.items():
        has_replaygain = True
        for f in v:
            song = taglib.File(f)
            if ('REPLAYGAIN_ALBUM_GAIN' not in song.tags or
                'REPLAYGAIN_ALBUM_PEAK' not in song.tags or
                'REPLAYGAIN_TRACK_GAIN' not in song.tags or
                'REPLAYGAIN_TRACK_PEAK' not in song.tags or
                'REPLAYGAIN_REFERENCE_LOUDNESS' not in song.tags):
                has_replaygain = False
                break
        if (has_replaygain):
            sorted_by_album[k] = None

    show_prompt_get_resp(sorted_by_album)

    for k, songs in sorted_by_album.items():
        if (songs == None):
            continue
        print('"' + k + '"...')
        cmd = ['metaflac', '--add-replay-gain'] + songs
        exec_cmd(cmd)

if (__name__ == '__main__'):
    main(len(sys.argv), sys.argv)
