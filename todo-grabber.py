import os
import sys

# TODO maybe add recursive search option???

file_types = ['.py', '.txt', '.md']

# check the provided args for a directory
if len(sys.argv) > 1:
    # if directory provided set it to path
    if os.path.isdir(sys.argv[1]):
        path = sys.argv[1]
    else:
        print('Error! Please provide a path or no arguments at all')
        exit()
else:
    # if not directory provided set it to cwd
    path = os.getcwd()

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
