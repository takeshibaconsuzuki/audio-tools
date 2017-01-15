#!/usr/bin/env python3
import os
import subprocess


def rec_get_files(directory_path, required_ext=None):
    ret = []
    for item in os.listdir(directory_path):
        if (item.startswith('.')):
            continue
        item_path = os.path.join(directory_path, item)
        if (os.path.isdir(item_path)):
            ret += rec_get_files(item_path, required_ext=required_ext)
        else:
            if (required_ext):
                if (item.endswith(required_ext)):
                    ret.append(item_path)
            else:
                ret.append(item_path)
    return ret


def exec_cmd(cmd):
    spo = subprocess.run(cmd,
                         stderr=subprocess.STDOUT,
                         stdout=subprocess.PIPE,
                         universal_newlines=True)
    if (spo.stdout != ''):
        print(spo.stdout, end='', flush=True)
    return spo.returncode
