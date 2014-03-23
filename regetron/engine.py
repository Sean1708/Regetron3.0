import re
import sys
import os

CMD_PATTERN = re.compile("^!([a-z]+)\s*(.*)$")


class ArtificialException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Regetron:

    def __init__(self):
        self.infile_name = None
        self.infile = ""
        self.match_mode = False
        self.from_script = False
        self.prompt = "> "

        self.commands = {
            "help": ("print a help message for the given command",
                     """Usage: !help [cmd]

    When called with no arguments this command prints a short description of
    all available commands. If an argument is supplied a longer description of
    just that command will be printed."""),
            "data": ("load a string into memory to be searched",
                     """Usage: !data "string"

    This command loads the string enclosed in matching quotation marks into
    memory to be searched by the entered regex. Seperate lines can be
    delimited by the escape character '\\n'. Subsequent calls to this command
    will overwrite the previous one."""),
            "load": ("load a file into memory to be searched",
                     """Usage: !load filename

    Loads the specified file into memory so that it can be searched, seperate
    lines in the file are loaded into memory as seperate line. Tilde expansion
    is performed when loading the file."""),
            "match": ("switch between match mode and search mode",
                      """Usage: !match

    Switches between search mode (default) and match mode. Match mode will
    only match if the regex occurs at the beginning of the line whereas in
    search mode the regex can match at any point in the line. In other words
    match mode bahaves as if each regex pattern begins with the caret '^'
    character."""),
            "parse": ("read regex from a file",
                      """Usage: !parse filename

    Matches the regex in the specified file to the loaded text. The regex in
    the file can be written verbosely. Tilde expansion is performed when
    searching for the file."""),
            "prompt": ("change the prompt",
                       """Usage: !prompt [string]

    Sets the prompt to the specified string (default is '> '). If no string is
    given, no prompt is used."""),
            "rep": ("mimic search and replace style regex",
                    """Usage: !rep expression

    Replaces matched regex with another string. The expression should be of the
    form /exp/rep/ where / is any character. The first section exp is the regex
    to match and the second section rep is the string to replace it with.""")
        }

    def load_input_file(self, infile_name):
        # could this cause problems for windows users?
        if infile_name[0:2] == '~/':
            infile_name = os.path.join(
                os.path.expanduser('~'), infile_name[2:]
            )
        self.infile_name = infile_name
        if not os.path.exists(self.infile_name):
            print("File {0} doesn't exist.".format(self.infile_name))
            # allows cmdline.py to know if data couldn't be loaded
            return False
        else:
            self.infile = open(self.infile_name).readlines()
            print("File {0} has been loaded.".format(self.infile_name))
            return True

    def load_script(self, fname):
        sys.stdin = open(fname)
        self.from_script = True

    def setup_readline(self):
        try:
            import readline
            import atexit

            histfile = os.path.join(os.path.expanduser("~"), ".regetronhist")

            try:
                readline.read_history_file(histfile)
            except IOError:
                pass

            atexit.register(readline.write_history_file, histfile)

            readline.parse_and_bind("TAB: complete")
        except:
            print("No readline support, so no scroll back for you.")

    def run_input_loop(self):
        regex = self.read_input()
        while regex:
            self.print_matches(regex)
            regex = self.read_input()

    def print_matches(self, regex):
        if not self.infile:
            print("Input file is empty. Use !load to load something.")
            return

        for i, line in enumerate(self.infile):
            res = self.test_regex(regex, line)
            if res:
                if res.groups():
                    print("{0:04d}: {1!r}".format(i, regex.findall(line)))
                else:
                    print("{0:04d}: {1!s}".format(i, line), end="")

    def test_regex(self, regex, line):
        if self.match_mode:
            return regex.match(line)
        else:
            return regex.search(line)

    def read_input(self):
        while True:
            try:
                exp = self.read_line(self.prompt)

                command = CMD_PATTERN.match(exp)

                if exp == "":
                    return self.read_verbose()
                elif command:
                    result = self.handle_command(*command.groups())
                    if result:
                        return result
                else:
                    return re.compile(exp)
            except EOFError:
                print("" if self.from_script else "\nBYE")
                return False
            except Exception as e:
                print("ERROR", e)

    def read_line(self, prompt=""):
        exp = input(prompt)
        if self.from_script:
            print(exp)

        return exp

    def read_verbose(self):
        exp = []
        l = self.read_line()
        while l:
            exp.append(l)
            l = self.read_line()

        return re.compile('\n'.join(exp), re.VERBOSE)

    def handle_command(self, command, args):
        if command == "data":
            self.set_data(args)
        elif command == "help":
            self.print_help(args)
        elif command == "load":
            self.load_input_file(args)
        elif command == "match":
            self.match_mode = not self.match_mode
            print("Match mode: {0}".format(
                "match" if self.match_mode else "search"
            ))
        elif command == "parse":
            sample = open(args).read()
            return re.compile(sample, re.X)
        elif command == "prompt":
            self.prompt = args
        elif command == "rep":
            self.replace_regex(args)
        else:
            raise ArtificialException(
                "invalid command, see !help for valid commands"
            )

    def set_data(self, args):
        self.infile_name = None

        # remove accidental whitespace
        args = args.strip()
        args = self.check_and_remove_quotes(args)

        data = str(args).split("\\n")
        self.infile = [l + "\n" for l in data]

    def check_and_remove_quotes(self, args):
        if (args[0] == args[-1]) and (args[0] in ["'", '"']):
            return args[1:-1]
        else:
            raise ArtificialException(
                "Data must be enclosed in matching quotation marks."
            )

    def print_help(self, cmd):
        if not cmd:
            print("Available commands are:")
            for k, v in self.commands.items():
                print("\t{0:10} - {1}".format(k, v[0]))
        else:
            try:
                print("{0}".format(self.commands[cmd][1]))
            except KeyError:
                raise ArtificialException(
                    "{0} is not a valid command".format(cmd)
                )

    def replace_regex(self, args):
        bound_char = args[0]
        pattern = args.split(bound_char)
        if len(pattern) != 4:
            print(
                "ERROR format is: !reg /REGEX/REPLACE/ and / can be any char."
            )
        else:
            reg, rep = pattern[1], pattern[2]
            regex = re.compile(reg)
            for i, line in enumerate(self.infile):
                if self.test_regex(regex, line):
                    print(re.sub(regex, rep, line), end="")
