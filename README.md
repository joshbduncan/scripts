# System Scripts

## Table of Contents

- [Airtable Expenses](#airtable-expenes)
- [Todo Grabber](#todo-grabber)
- [The End](#the-end)

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam at ex lobortis, commodo odio vitae, euismod lorem. Pellentesque tempor, lacus vel feugiat tincidunt, nibh nisl faucibus augue, in iaculis libero libero eu metus. Vestibulum congue libero massa, id rutrum risus tincidunt ultrices. Cras nunc est, accumsan a varius ut, mollis non mi. Pellentesque sit amet hendrerit massa, at sollicitudin risus. Nulla eget suscipit felis, vel malesuada arcu. Donec vitae massa sed enim tristique maximus et commodo enim. Donec tempor mi vitae viverra pretium. Cras vitae feugiat ante. Duis turpis augue, dapibus quis molestie sit amet, sodales ut tortor. Mauris ultricies, mi vitae tincidunt pretium, odio mauris suscipit nisi, sit amet sagittis nisl lacus nec tortor.

Aliquam vel mauris ac lectus sagittis aliquam ac ut sem. Praesent non est molestie, pulvinar nisi rhoncus, commodo ex. Nulla feugiat at quam vel congue. Nunc in ligula sed nulla aliquet euismod ac non metus. Nullam fermentum a mi ut euismod. Duis cursus finibus nulla, ac scelerisque odio cursus quis. Sed tincidunt nunc vel leo dictum egestas. Morbi tempus mattis ante semper ultricies. Donec vulputate ut turpis in congue.

Nam non erat sit amet enim faucibus volutpat. Duis vel pulvinar mi. Ut non ultrices justo. Morbi vitae ipsum at felis convallis porta. Nullam vitae elit ex. Maecenas quam ipsum, sagittis eu quam quis, ultricies varius orci. Curabitur id suscipit dui. Nulla et velit mattis, rhoncus odio ac, dictum mi.

Sed molestie elementum rutrum. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed id metus ac diam vulputate volutpat. Sed hendrerit aliquet eros interdum accumsan. Sed luctus diam et mauris auctor hendrerit. Donec fringilla elementum urna nec convallis. Cras metus libero, pulvinar at sagittis sed, feugiat vitae sapien. Quisque condimentum ut eros eget vulputate. Suspendisse faucibus dictum purus at cursus. Quisque convallis quam dui. In tempor arcu ligula, id tempor est mollis lacinia. Donec pretium elementum enim ac scelerisque. Maecenas neque sapien, aliquet a metus tempor, vehicula vestibulum diam. Etiam ultrices egestas mauris, sed euismod mauris facilisis vel.

Vestibulum venenatis ante at lorem sollicitudin convallis. Fusce vestibulum neque ac odio lacinia fringilla. Ut tristique risus quis arcu convallis, ut convallis est convallis. Nunc non accumsan nibh, non ultricies risus. Etiam mattis, augue in tempor iaculis, quam neque euismod urna, vitae ornare ex ante at ex. Quisque sagittis velit ac dolor pretium consectetur. Donec scelerisque mollis metus a pretium. Aenean maximus purus non justo finibus, eget sollicitudin ex elementum. Mauris maximus, augue vitae tincidunt fermentum, ante ex luctus sem, vel feugiat ligula nisi sit amet justo. Morbi ut vulputate nisl, et finibus leo. Cras elit eros, luctus quis condimentum vitae, lacinia quis neque. Vivamus sit amet elit feugiat, pretium nisl ac, ullamcorper lectus. Donec posuere imperdiet erat at rutrum. In hac habitasse platea dictumst. Sed eu nulla lectus. Praesent porttitor efficitur risus nec vehicula.

## todo-grabber:

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

## airtable-expenses:

Info to come...

## The End
