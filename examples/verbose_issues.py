import re

strings = ["Hello\n", "there", "yo "]

verb_regex = re.compile(r"""[     # open set
                             A-Z  # capital letter
                            ]     # close set""", re.VERBOSE)

regex = re.compile(r"[A-Z]")

print("STANDARD\n========")
for string in strings:
    print(repr(string))
    print(repr(regex.pattern))
    print(regex.search(string))
    print(re.search(regex, string))
    print()


print("VERBOSE\n=======")
for string in strings:
    print(repr(string))
    print(repr(verb_regex.pattern))
    print(verb_regex.search(string))
    print(re.search(verb_regex, string))
    print()
