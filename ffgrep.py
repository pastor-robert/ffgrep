#!/usr/bin/env python
import os
import re
import sys
import fnmatch

# First arg is always regex, remaining args are
# either directories or file patterns
try:
    regex = sys.argv[1]
    dirs = [d for d in sys.argv[2:] if os.path.isdir(d)]
    fnpats = [d for d in sys.argv[2:] if not os.path.isdir(d)]
    fnpats = ['*'+f if f.startswith('.') else f for f in fnpats]
    if not dirs:
        dirs = ('.',)
    if not fnpats:
        fnpats = ('*',)
except IndexError:
    usage = '''
        USAGE:
            {0} REGEX [FILE ...] [DIR ...]
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
            {0} CONFIG_HIGHMEM .c
                Search for the string CONFIG_HIGHMEM in all C source code
                files in '.' or any subdirectories of '.'.  Like find
                . -name '*.c' -print | xargs egrep -l CONFIG_HIGHMEM

            {0} CONFIG_HIGHMEM .c kernel/power/
                Search for the string only in specific subdirectory.

            {0} HIGHMEM Kconfig
                Search for the string in all files named
                'Kconfig', in all subdirectories of '.'

            {0} HIGHMEM Kconfig kernel
                Search in specific files in specific subdir tree

            {0} HIGHMEM kernel .h .c
            {0} HIGHMEM kernel '.[ch]'
                Equivalent: Look in all C source and Header files in
                specified subdir
    '''.format(os.path.basename(sys.argv[0]) or '<PROGRAM>')
    print(usage)
    sys.exit(1)

# Convert file patterns to a single regex
fnpats = '('+')|('.join(map(fnmatch.translate, fnpats))+')'
fnpats = re.compile(fnpats)

for root in dirs:
    for root, folders, files in os.walk(root):
        if '.svn' in folders:
            folders.remove('.svn')
        for file in files:
            if fnpats.match(file):
                file = os.path.join(root, file)
                with open(file) as fd:
                    if any(re.search(regex, line) for line in fd):
                            print(file)
                            sys.stdout.flush()
