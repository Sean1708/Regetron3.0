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
        self.from_script = False
        self.prompt = "> "

    def read_line(self, prompt=""):
        exp = raw_input(prompt)
        if self.from_script:
            print exp
        return exp

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


    def read_verbose(self):
        exp = []
        l = self.read_line()

        while l:
            exp.append(l)
            l = self.read_line()

        return re.compile("\n".join(exp), re.X)

    def set_data(self, args):
        self.infile_name = None
        data = eval(args).split("\n")
        self.infile = [l + "\n" for l in data]

    def handle_command(self, command, args):
        if command == "load":
            self.load_input_file(args)
        elif command == "help":
            print "Commands: !load !match !data !rep"
        elif command == "data":
            self.set_data(args)
        elif command == "parse":
            sample = open(args).read()
            return re.compile(sample, re.X)
        elif command == "match":
            self.match_mode = not self.match_mode
            print "Match mode: %s" % (self.match_mode and "match" or "search")
        elif command == "rep":
            self.replace_regex(args)
        else:
            print "Invalid command, only !load and !help is available."

    def read_input(self):
        while True:
            try:
                exp = self.read_line(self.prompt)

                command = CMD_PATTERN.match(exp)

                if exp == "":
                    return self.read_verbose()
                if command:
                    result = self.handle_command(*command.groups())
                    if result: return result
                else:
                    return re.compile(exp)
            except EOFError:
                print self.from_script and "\n" or "\nBYE"
                return False
            except Exception, e:
                print "ERROR", e

    def replace_regex(self, args):
        bound_char = args[0]
        pattern = args.split(bound_char)
        if len(pattern) != 4:
            print "ERROR, format is: !reg /REGEX/REPLACE/ and / can be any char."
        else:
            reg, rep = pattern[1], pattern[2]
            regex = re.compile(reg)
            for i, line in enumerate(self.infile):
                if self.test_regex(regex, line):
                    print re.sub(regex, rep, line),
                    
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

    def load_script(self, fname):
        sys.stdin = open(fname)
        self.from_script = True

