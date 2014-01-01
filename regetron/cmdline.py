#!/usr/bin/env python

import re
import sys
import cmd
import os
from regetron.engine import Regetron

def main():
    SHELL = Regetron()

    WELCOME = """
    Regetron! The regex teaching SHELL.

Type your regex at the prompt and hit enter. It'll show you the
lines that match that regex, or nothing if nothing matches.
Hit CTRL-D to quit (CTRL-Z on windows).
"""

    if len(sys.argv) >= 2:
        exists = SHELL.load_input_file(sys.argv[1])

        if len(sys.argv) == 3 and exists:
            try:
                SHELL.load_script(sys.argv[2])
            except FileNotFoundError:
                print("Script {0} doesn't exist.".format(sys.argv[2]))
    else:
        SHELL.setup_readline()
        print(WELCOME)


    SHELL.run_input_loop()


if __name__ == "__main__":
    main()
