#!/bin/sh
# Install the development version of path.py into ./local_lib and run the
# program that uses it.

set -e

LIB_DIR="local_lib"
LOG_FILE="path_install.log"

# Display the pip version in use.
pip --version

# Fresh install into local_lib (crush any previous install).
rm -rf "$LIB_DIR"

# Install the development version of path.py from its GitHub repository.
pip install --upgrade --target "$LIB_DIR" \
    "git+https://github.com/jaraco/path.git#egg=path" > "$LOG_FILE" 2>&1

# If the install succeeded, run the program.
if [ -d "$LIB_DIR/path" ] || [ -f "$LIB_DIR/path.py" ]; then
    python3 my_program.py
else
    echo "path installation failed, see $LOG_FILE" >&2
    exit 1
fi
