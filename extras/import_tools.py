import re

from collections import OrderedDict

from learningprogress.progress.models import Section


import_file='filename'  # Insert name of file here.


white_pattern = re.compile("(\s*)(.+)")
"""
Splits a line into white spaces and the text.
"""


def main():
    """
    Main entry point.
    """
    data = OrderedDict()
    try:
        magic(lines(), data)
    except StopIteration:
        # Catch Exception when the work is done.
        pass
    make(data, parent=None)
    return 0


def lines():
    """
    Generator which returns a tuple for each line.
    """
    with open(import_file) as f:
        while True:
            line = f.readline()
            groups = white_pattern.match(line)
            if groups is None:
                # The file is finished. Stop generator
                #return None  # Python >= 3.3
                raise StopIteration(None)
            whites = len(groups.group(1))
            word = groups.group(2)
            yield whites, word


def magic(lines, my_dict, ebene=0):
    """
    Here is some magic.

    Expects a generator as first argument. The second argument is an
    OrderedDict which is filled one by one.

    The function returns the same data as the generator so that the return
    looks like the "next line".
    """
    while True:
        whites, word = next(lines)
        if whites > ebene:  # step in
            last_key = next(reversed(my_dict))
            last_element = my_dict[last_key]
            last_element[word] = OrderedDict()
            # Now it is about the next step, whites <= ebene
            whites, word = magic(lines, last_element, whites)
        if whites < ebene:  # step out
            # All done.
            break
        else:
            # Add actual line.
            my_dict[word] = OrderedDict()
    return (whites, word)


def make(data, parent):
    for weight, key in enumerate(data):
        s = Section.objects.create(name=key, parent=parent, weight=weight)
        print(s)
        make(data[key], parent=s)
