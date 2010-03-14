# Copyright (C) 2008 Novell, Inc.
# Written by Brian G. Merrell <bgmerrell@novell.com>

# THIS FILE IS LICENSED UNDER THE MIT LICENSE

from tempfile import mkstemp
from shutil import move, rmtree
from os import remove, close, rename, path, listdir
from subprocess import Popen
import re

LZMA_PATTERN = 'chromium\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.svn[0-9]+\.tar\.lzma'

def get_lzma_name():
    for file_name in listdir("."):
        m = re.match(LZMA_PATTERN, file_name)
        if m is not None:
            return m.group()
    return false

# for now, we'll just require this to be run in the same directory as the
# chromium source
try:
    assert(get_lzma_name)
except AssertionError, e:
    print "Can't find chromium source file."
    print "Try running this tool in the same directory as the chromium source"

def replace_line(file, old_line, new_line):
    # create temp file
    f, file_name = mkstemp()
    new_file = open(file_name, 'w')
    old_file = open(file)
    for line in old_file:
        new_file.write(line.replace(old_line, new_line))
    # close temp file
    new_file.close()
    close(f)
    old_file.close()
    # delete original file
    remove(file)
    # move new file to replace original file
    move(file_name, file)

def remove_line(file, old_line):
    # create temp file
    f, file_name = mkstemp()
    new_file = open(file_name, 'w')
    old_file = open(file)
    for line in old_file:
        if "".join([old_line, "\n"]) == line:
            pass
        elif old_line == line:
            pass
        else:
            new_file.write(line)
    # close temp file
    new_file.close()
    close(f)
    old_file.close()
    # delete original file
    remove(file)
    # move new file to replace original file
    move(file_name, file)

def rename_file(old_file, new_file):
    rename(old_file, new_file) 

# rename the decompressed src directory name and the names of tarball and
# compressed file
def rename_src(old_name, new_name):
    compressed_name = get_lzma_name()
    p = Popen(['lzma', '-d', '-v', '%s' % compressed_name])
    p.wait()
    tarball_name = path.splitext(compressed_name)[0]

    # don't need this name anymore, it's been ranamed to tarball_name when
    # it was decompressed to lzma
    del compressed_name

    p = Popen(['tar', '-x', '-v', '-f', '%s' % tarball_name])

    # change the first part of the tarball (e.g., chromium.*.tar.gz to
    # chromium-browser.*.tar.gz)
    new_tarball_name = \
        ".".join([new_name, ".".join(tarball_name.split(".")[1:])])
    
    p.wait()
    rename(old_name, new_name)
    remove(tarball_name)

    # we don't want to refer to tarball_name anymore
    del tarball_name

    p = Popen(['tar', '-c', '-v', '-f', '%s' % new_tarball_name,
                                        '%s' % new_name ])
    p.wait()

    # we should delete the extracted directory now
    rmtree(new_name)

    # recompress using lzma
    p = Popen(['lzma', '-z', '-v', '-7', '%s' % new_tarball_name])
    p.wait()

