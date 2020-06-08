import os
import sys
import argparse

# TODO maybe add recursive search option???


def get_todos_from_file(path):
    # if the item is a file print it
    if os.path.isfile(path):
        file_path = path
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[-1]

        # store todos for the entire file
        todos = []

        # if the file extension matches what we're looking for
        if file_ext in file_types:
            file = open(file_path, 'r')

            # track line number
            line_num = 0

            for line in file:
                # remove whitespace and new lines
                line = line.strip('\n').strip()
                line_num += 1

                # iterate through all todo items
                if 'TODO' in line:
                    if '# ' in line:
                        # strip off comment tag
                        place = line.find('# TODO')
                        output = f'> {line[place + 2:]} (line {line_num})'
                    else:
                        output = f'> {line} (line {line_num})'

                    # add line to todos
                    todos.append(output)

        # if any todo exists then print them out
        if todos != []:
            print(f'File: {file_name} ({len(todos)} total)')

            for todo in todos:
                print(todo)

            print('')


file_types = ['.py', '.sh', '.txt', '.md']

# create the argument parser
my_parser = argparse.ArgumentParser(prog='todo-grabber',
                                    description='List all TODO items...',
                                    epilog='Duces! :)')

# add the program arguments
my_parser.add_argument('-f',
                       '--file',
                       metavar='file',
                       dest='FILE',
                       type=str,
                       help="the file to search through for todo's")

my_parser.add_argument('-p',
                       '--path',
                       metavar='path',
                       dest='PATH',
                       type=str,
                       help="the directory to search for todo's")

# execute the parse_args() method
args = my_parser.parse_args()

# set the path to iterate through
file = args.FILE
path = args.PATH

if file:
    path = file
    # if path was provided check and see if it's an actual path to a file
    if not os.path.isfile(path):
        print(f"No such file or directory: '{path}'")
        sys.exit()

    get_todos_from_file(file)

else:
    # if no arguments are supplied then use current directory
    if not path:
        path = os.getcwd()

    # if path was provided check and see if it's an actual path
    if not os.path.isdir(path):
        print(f"No such file or directory: '{path}'")
        sys.exit()

    # iterate through all items in directory
    for item in os.listdir(path):
        # set the path of the item
        item_path = f'{path}/{item}'

        get_todos_from_file(item_path)
