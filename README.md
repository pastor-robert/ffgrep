# ffgrep

A fast file finder and grep tool that combines the functionality of `find` and `grep` into a single command.

*Developed with assistance from Claude AI by Anthropic.*

## Overview

`ffgrep` replaces the common pattern of `find . -name '*.ext' | xargs grep pattern` with a simpler, more efficient command. It recursively searches for files matching a pattern and greps for content within those files.

## Installation

Simply clone this repository and make the script executable:

```bash
git clone https://github.com/your-username/ffgrep.git
cd ffgrep
chmod +x ffgrep.py
```

Optionally, create a symlink to use it system-wide:

```bash
ln -s $(pwd)/ffgrep.py /usr/local/bin/ffgrep
```

## Usage

```bash
./ffgrep.py [options] <file_pattern> <search_pattern>
```

### Arguments

- `file_pattern`: File pattern to search (e.g., "*.c", "*.py", "*.txt")
- `search_pattern`: Regular expression pattern to search for within files

### Options

- `-d, --directory DIR`: Directory to search (default: current directory)
- `-i, --ignore-case`: Case insensitive search
- `-l, --line-numbers`: Show line numbers
- `-n, --filename-only`: Show only filenames that contain matches

### Examples

```bash
# Find 'main' function in all C files
./ffgrep.py "*.c" main

# Case-insensitive search for test functions in Python files
./ffgrep.py "*.py" "def.*test" -i

# Show line numbers for error messages in log files
./ffgrep.py "*.log" "error" -l

# Just show filenames containing TODO comments
./ffgrep.py "*.py" "TODO" -n

# Search in a specific directory
./ffgrep.py -d /path/to/project "*.js" "function"
```

## Features

- **Fast**: Uses generators to avoid loading all file paths into memory
- **Flexible**: Supports glob patterns for file matching and regex for content search
- **Portable**: Single Python script with no external dependencies
- **Unix-friendly**: Follows Unix conventions for exit codes and output format

## Requirements

- Python 3.6+
- No external dependencies

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Exit Codes

- `0`: Matches found
- `1`: No matches found or error occurred