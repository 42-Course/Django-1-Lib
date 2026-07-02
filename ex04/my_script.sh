#!/bin/sh
# Create a python3 virtualenv named django_venv, install the requirements
# (latest stable django + psycopg2), and leave the venv activated on exit.

set -e

VENV="django_venv"

# Create the virtualenv on python3 if it does not exist yet.
if [ ! -d "$VENV" ]; then
    python3 -m venv "$VENV"
fi

# Install the requirement.txt inside the virtualenv.
"$VENV/bin/pip" install --upgrade pip
"$VENV/bin/pip" install -r requirement.txt

# Activate the virtualenv and hand over an interactive shell, so the user
# stays inside the activated environment once the script ends.
. "$VENV/bin/activate"
exec "${SHELL:-/bin/zsh}"
