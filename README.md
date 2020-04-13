# System Scripts

## Table of Contents

- [Airtable Expenses](#airtable-expenes.py)
- [Todo Grabber](#todo-grabber.py)
- [The End](#the-end)

# airtable-expenses.py

Info to come...

## todo-grabber.py:

Search for all todo's (ex. 'TODO') from the specified file types in the current directory, supplied directory '-p', or supplied file '-f'.

Python 3 Modules:  
- [os module](https://docs.python.org/3/library/os.html)
- [sys module](https://docs.python.org/3/library/sys.html)
- [argparse module](https://docs.python.org/3/library/argparse.html)

### Usage Examples:

Iterate through all of the files in the current directory and print out the todo's.

    python3 todo-grabber.py

Iterate through all of the files in the specified directory '-p ~/path' and print out the todo's .

    python3 todo-grabber.py -p ~/path

Print out todo's for the specified file '-f file.py'.

    python3 todo-grabber.py -f ~/path/file.py


**Output Example:**

    File: test-python-file.py (1 total)
    > TODO move to admin interface (72)

    File: test-markdown-file.md (2 total)
    > TODO update variables in file.py (22)
    > TODO remove all test data (38)

    File: test-text-file.txt (3 total)
    > TODO figure out path and file storage (82)
    > TODO reconfigure check_for_dupe (88)
    > TODO check for any available items (160)

### Specified File Types

The specified file types are set in the 'file_types' list variable.

    file_types = ['.py', '.txt', '.md']
    
## The End
