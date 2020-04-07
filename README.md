# System Scripts

## todo-grabber.py:

Search for all todo's (ex. 'TODO') from the specified file types in the current directory, or any directory if supplied in the arguments.

Python 3:  
- [os module](https://docs.python.org/3/library/os.html)
- [sys module](https://docs.python.org/3/library/sys.html)
- [argparse module](https://docs.python.org/3/library/argparse.html)

### Usage Examples:

Iterate through all of the specified files and print out the todo's in the current directory.

    python3 todo-grabber.py
    
Iterate through all of the specified files and print out the todo's in the specified directory '-p ~/path'.

    python3 todo-grabber.py -p ~/path


**Output Example:**

    File: test-python-file.py
    > TODO move to admin interface (72)

    File: test-markdown-file.md
    > TODO update variables in file.py (22)
    > TODO remove all test data (38)

    File: test-text-file.txt
    > TODO figure out path and file storage (82)
    > TODO reconfigure check_for_dupe (88)
    > TODO check for any available items (160)

