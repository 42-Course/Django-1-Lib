#!/usr/bin/python3
import sys
# The `path` library is installed locally into ./local_lib by my_script.sh.
sys.path.insert(0, 'local_lib')

from path import Path


def main():
    folder = Path('lotr')
    folder.makedirs_p()

    target = folder / 'hello.txt'
    target.write_text('Mae Govannen, mellon\n')

    print(target.read_text(), end='')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print("Error: {}".format(error), file=sys.stderr)
        sys.exit(1)
