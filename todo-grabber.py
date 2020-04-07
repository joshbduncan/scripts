import os
import sys
import argparse

# TODO maybe add recursive search option???

file_types = ['.py', '.txt', '.md']

# create the argument parser
my_parser = argparse.ArgumentParser(prog='todo-grabber',
                                    description='List all TODO items in a folder...',
                                    epilog='Duces! :)')

# add the program arguments
my_parser.add_argument('-p',
                       '--path',
                       metavar='path',
                       dest='PATH',
                       type=str,
                       help="the directory to search for todo's",
                       default=os.getcwd())

# execute the parse_args() methos
args = my_parser.parse_args()

# set the path to iterate through
path = args.PATH

# if no path was supplied then use current directory
if not os.path.isdir(path):
    print('Error! Please provide a path or no arguments at all')
    sys.exit()

# iterate through all items in directory
for item in os.listdir(path):
    # set the path of the item
    item_path = f'{path}/{item}'
    # if the item is a file print it
    if os.path.isfile(item_path):
        file_path = item_path
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[-1]

        # store todos for the entire file
        todos = []

        # if the file extention matches what we're looking for
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
                        output = f'> {line[place + 2:]} ({line_num})'
                    else:
                        output = f'> {line} ({line_num})'

                    # add line to todos
                    todos.append(output)

        # if any todo exists then print them out
        if todos != []:
            print(f'File: {file_name}')

            for todo in todos:
                print(todo)

            print('')
