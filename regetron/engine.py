import re
import sys
import cmd
import os

CMD_PATTERN = re.compile("^!([a-z]+)\s*(.*)$")

class Regetron(object):

    def __init__(self):
        self.infile_name = None
        self.infile = ""
        self.match_mode = False

    def setup_readline(self):
        try:
            import readline
        except:
            print "No readline support, so no scroll back for you."

        import atexit

        histfile = os.path.join(os.path.expanduser("~"), ".regetronhist")

        try:
            readline.read_history_file(histfile)
        except IOError:
            pass

        atexit.register(readline.write_history_file, histfile)

        readline.parse_and_bind("TAB: complete")

    def load_input_file(self, infile_name):
        self.infile_name = infile_name
        if not os.path.exists(self.infile_name):
            print "That file doesn't exist."
            return

        self.infile = open(self.infile_name).readlines()


    def read_multiline_regex(self):
        exp = []
        l = raw_input()
        while l:
            exp.append(l)
            l = raw_input()

        return re.compile("\n".join(exp), re.X)

    def set_data(self, args):
        self.infile_name = None
        data = eval(args).split("\n")
        self.infile = [l + "\n" for l in data]

    def handle_command(self, command, args):
        if command == "load":
            self.load_input_file(args)
        elif command == "help":
            print "Commands: !load !match !data"
        elif command == "data":
            self.set_data(args)
        elif command == "parse":
            sample = open(args).read()
            return re.compile(sample, re.X)
        elif command == "match":
            self.match_mode = not self.match_mode
            print "Match mode: %s" % (self.match_mode and "match" or "search")
        else:
            print "Invalid command, only !load and !help is available."

    def read_input(self):
        while True:
            try:
                exp = raw_input("> ")
                command = CMD_PATTERN.match(exp)

                if exp == "":
                    return self.read_multiline_regex()
                if command:
                    result = self.handle_command(*command.groups())
                    if result: return result
                else:
                    return re.compile(exp)
            except EOFError:
                print "\nBYE"
                return False
            except Exception, e:
                print "ERROR", e

    def test_regex(self, regex, line):
        if self.match_mode:
            return regex.match(line)
        else:
            return regex.search(line)

    def print_matches(self, regex):
        if not self.infile:
            print "Input file is empty. Use !load to load something."
            return

        for i, line in enumerate(self.infile):
            if self.test_regex(regex, line):
                print "%.4d: %s" % (i, line),

    def run_input_loop(self):
        regex = self.read_input()
        while regex:
            self.print_matches(regex)
            regex = self.read_input()

