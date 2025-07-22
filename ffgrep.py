#!/usr/bin/env python3

import argparse
import fnmatch
import os
import re
import sys
from pathlib import Path

def find_files(directory, pattern):
    """Find files matching the given pattern."""
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if fnmatch.fnmatch(filename, pattern):
                yield os.path.join(root, filename)

def grep_in_file(filepath, search_pattern, case_insensitive=False, line_numbers=False):
    """Search for pattern in a file and return matching lines."""
    matches = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            flags = re.IGNORECASE if case_insensitive else 0
            regex = re.compile(search_pattern, flags)
            
            for line_num, line in enumerate(f, 1):
                if regex.search(line):
                    line = line.rstrip('\n')
                    if line_numbers:
                        matches.append((line_num, line))
                    else:
                        matches.append(line)
    except (IOError, OSError) as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
    
    return matches

def main():
    parser = argparse.ArgumentParser(
        description='Find files and grep for patterns - combines find and grep functionality',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  ffgrep -n "*.c" main              # Find main in all .c files
  ffgrep -n "*.py" "def.*test" -i   # Case-insensitive search for test functions
  ffgrep "*.txt" "error" -l         # Show line numbers for matches
        '''
    )
    
    parser.add_argument('pattern', help='File pattern to search (e.g., "*.c", "*.py")')
    parser.add_argument('search', help='Pattern to search for within files')
    parser.add_argument('-d', '--directory', default='.', 
                        help='Directory to search (default: current directory)')
    parser.add_argument('-i', '--ignore-case', action='store_true',
                        help='Case insensitive search')
    parser.add_argument('-l', '--line-numbers', action='store_true',
                        help='Show line numbers')
    parser.add_argument('-n', '--filename-only', action='store_true',
                        help='Show only filenames that contain matches')
    
    args = parser.parse_args()
    
    found_matches = False
    
    for filepath in find_files(args.directory, args.pattern):
        matches = grep_in_file(filepath, args.search, args.ignore_case, args.line_numbers)
        
        if matches:
            found_matches = True
            
            if args.filename_only:
                print(filepath)
            else:
                for match in matches:
                    if args.line_numbers:
                        line_num, line = match
                        print(f"{filepath}:{line_num}:{line}")
                    else:
                        print(f"{filepath}:{match}")
    
    return 0 if found_matches else 1

if __name__ == '__main__':
    sys.exit(main())