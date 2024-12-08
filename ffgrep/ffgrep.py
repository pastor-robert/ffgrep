#!/usr/bin/env python

'''
ffgrep - search subdirectory's files for pattern
'''

import os
import re
import sys
import fnmatch

def main():
    '''
    main - main
    '''
    # First arg is always regex, remaining args are
    # either directories or file patterns
    try:
        regex = re.compile(sys.argv[1])
        dirs = [d for d in sys.argv[2:] if os.path.isdir(d)]
        fnpats = [d for d in sys.argv[2:] if not os.path.isdir(d)]
        fnpats = ['*'+f if f.startswith('.') else f for f in fnpats]
        if not dirs:
            dirs = ('.',)
        if not fnpats:
            fnpats = ('*',)
    except IndexError:
        program = sys.argv[0] or '<PROGRAM>'
        usage = f'''
            USAGE:
                {program} REGEX [FILE ...] [DIR ...]
                    REGEX - pattern to search for, e.g. "main" or "print.*memory"
                    FILE - filenames to search in, e.g. "mem.h", "*config", or ".c"
                        default - "*"
                    DIR - directories to walk looking for FILE
                        default - "."

            SYNOPSIS:
                For each directory in and below DIR, look for files named like
                FILE.  For each file found, look for REGEX inside that file.
                Print the full path to each file that contains REGEX.

            EXAMPLES:
                {program} CONFIG_HIGHMEM .c
                    Search for the string CONFIG_HIGHMEM in all C source code
                    files in '.' or any subdirectories of '.'.  Like find
                    . -name '*.c' -print | xargs egrep -l CONFIG_HIGHMEM

                {program} CONFIG_HIGHMEM .c kernel/power/
                    Search for the string only in specific subdirectory.

                {program} HIGHMEM Kconfig
                    Search for the string in all files named
                    'Kconfig', in all subdirectories of '.'

                {program} HIGHMEM Kconfig kernel
                    Search in specific files in specific subdir tree

                {program} HIGHMEM kernel .h .c
                {program} HIGHMEM kernel '.[ch]'
                    Equivalent: Look in all C source and Header files in
                    specified subdir
        '''
        print(usage)
        sys.exit(1)

    # Convert file patterns to a single regex
    fnpats = '('+')|('.join(map(fnmatch.translate, fnpats))+')'
    fnpats = re.compile(fnpats)

    for root in dirs:
        for root, folders, files in os.walk(root):
            if '.svn' in folders:
                folders.remove('.svn')
            for file_name in files:
                if fnpats.match(file_name):
                    file_name = os.path.join(root, file_name)
                    with open(file_name, encoding="utf-8") as file:
                        if any(re.search(regex, line) for line in file):
                            print(file_name)
                            sys.stdout.flush()

if __name__ == "__main__":
    main()
