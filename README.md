# System Scripts

Personal system scripts I use to make life a little easier...

## Table of Contents

- [Airtable Expenses](#airtable-expensespy)
- [Todo Grabber](#todo-grabberpy)

---

## airtable-expenses.py:

Grab all list of my "unsubmitted" work receipts from an Airtable base and generate my expense report. The report is then attached to an auto-generated Outlook email using Applescript. 

The script also downloads a copy of the reciept PDF's from Airtable and appends them to the end of the expense report.

Requirements:  
- [airtable-python-wrapper](https://github.com/gtalarico/airtable-python-wrapper)
- [applescript](https://github.com/andrewp-as-is/applescript.py)
- [argparse](https://docs.python.org/3/library/argparse.html)
- [datetime](https://docs.python.org/3/library/datetime.html)
- [fpdf](https://github.com/reingart/pyfpdf)
- [os](https://docs.python.org/3/library/os.html)
- [pandas](https://pandas.pydata.org/)
- [PyPDF2](https://github.com/mstamy2/PyPDF2)
- [requests](https://requests.readthedocs.io/en/master/)
- [subproces](https://docs.python.org/3/library/subprocess.html)
- [sys](https://docs.python.org/3/library/sys.html)
- [tabulate](https://github.com/astanin/python-tabulate)
- [tempfile](https://docs.python.org/3/library/tempfile.html)

### Usage Examples:

Grab all "unsubmitted" work expenses from Airtable up until the date specified and generate a report.

    python3 airtable-expenses.py -l 2000-01-01

Mark all "unsubmitted" work expenses in Airtable up to the date provided as submitted.

    python3 airtable-expenses.py -m 2000-01-01

### Airtable Base: Receipts

**Table Name:** Expenses  

Fields:
- Date
- Description
- Category (Personal, Work)
- Card
- Vendor
- Amount
- Receipt
- Submitted

---

## todo-grabber.py:

Search for all todo's (ex. 'TODO') from the specified file types in the current directory, supplied directory '-p', or supplied file '-f'.

Requirements:  
- [os](https://docs.python.org/3/library/os.html)
- [sys](https://docs.python.org/3/library/sys.html)
- [argparse](https://docs.python.org/3/library/argparse.html)

### Usage Examples:

Iterate through all of the files in the current directory and print out the todo's.

    python3 todo-grabber.py

Iterate through all of the files in the specified directory '-p ~/path' and print out the todo's.

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
