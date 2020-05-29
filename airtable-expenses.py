import sys
import os
import argparse
import subprocess
import applescript
import requests
import tempfile
import pandas as pd
from datetime import datetime
from tabulate import tabulate
from fpdf import FPDF
import PyPDF2
import airtable
import secrets


# TODO add some error catching


# import secrets and set variables
AIRTABLE_KEY = secrets.AIRTABLE_KEY
AIRTABLE_TOKEN = secrets.AIRTABLE_TOKEN
AIRTABLE_URL = secrets.AIRTABLE_URL
AIRTABLE_BASE = secrets.AIRTABLE_BASE
AIRTABLE_TABLE = secrets.AIRTABLE_TABLE


def write_to_clipboard(output):
    # write to clipboard for applescript function
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))


def conn_airtbale():
    # create a connection to the airtable base
    try:
        conn = airtable.Airtable(
            AIRTABLE_BASE, AIRTABLE_TABLE, api_key=AIRTABLE_KEY)
    except:
        print("Error! Couldn't connect to Airtable.")

    return conn


def cleanup_date(date):
    # set end date for expense report
    try:
        year = int(date.split('-')[0])
        month = int(date.split('-')[1])
        day = int(date.split('-')[2])
        exp_date = datetime(year, month, day)
    except:
        print('Not a valid date! Pleas change date and run again.')
        sys.exit()

    return exp_date


def download_pdfs(expenses, tmp_dir, exp_date):
    # download all pdf receipts from airtable url
    print(f'Downloading {len(expenses)} receipt(s)...')

    for expense in expenses:
        if datetime.strptime(expense['fields']['Date'], '%Y-%m-%d') <= exp_date:
            exp_id = expense['id']
            file_path = f'{tmp_dir}/{exp_id}.pdf'
            url = expense['fields']['Receipt'][0]['url']
            receipt = requests.get(url)

            with open(file_path, 'wb') as f:
                f.write(receipt.content)


def create_df(data, exp_date):
    # create a pandas dataframe to hold the data
    df = pd.DataFrame()

    # setup lists for found expense(s) info
    dates = []
    descriptions = []
    companies = []
    vendors = []
    amounts = []

    # iterate through expenses insert data into lists
    for expense in data:
        if datetime.strptime(expense['fields']['Date'], '%Y-%m-%d') <= exp_date:
            dates.append(expense['fields']['Date'])
            companies.append(expense['fields']['Card'])
            vendors.append(expense['fields']['Vendor'])
            descriptions.append(expense['fields']['Description'])
            amounts.append(expense['fields']['Amount'])

    # fill in the Pandas dataframe
    df['Date'] = dates
    df['Description'] = descriptions
    df['Company (Card)'] = companies
    df['Vendor'] = vendors
    df['Amount'] = amounts

    # add in a total line
    df.loc['Total'] = pd.Series(df['Amount'].sum(), index=['Amount'])
    # total = df['Amount'].sum()

    return df


def create_pdf(table, exp_date, tmp_dir):
    # format data and set PDF filename and output path
    formatted_exp_date = exp_date.strftime('%Y-%m-%d')
    path = f'{tmp_dir}/1.pdf'

    # setup PDF page and add in info
    print('Creating expense report...')
    pdf = FPDF('L', 'in', 'Letter')

    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, .5, 'Expense Report for Josh Duncan', align='C')
    pdf.ln(h=.5)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, .5, f'Expenses Through: {formatted_exp_date}', align='C')
    pdf.ln(h=.5)
    pdf.set_font('Courier', 'B', 9)

    for line in table.split('\n'):
        pdf.cell(0, .5, line, align='C')
        pdf.ln(h=.1875)

    # output the final PDF report file
    pdf.output(path, 'F')


def mark_expense(exp_date):
    # mark all current expenses on airtable as "submitted"
    # should be ran with the -m flag after creating a report
    try:
        table = conn_airtbale()
        current_exp = table.get_all(view='CA - Open Expenses', sort='Date')

        if current_exp == []:
            print('There are no expenses to mark... Exiting!')
            sys.exit()
        else:
            for expense in current_exp:
                if datetime.strptime(expense['fields']['Date'], '%Y-%m-%d') <= exp_date:
                    exp_id = expense['id']
                    exp_name = expense['fields']['Description']

                    print(f'Marking expense {exp_name} as submitted...')

                    fields = {'Submitted': True}
                    table.update(exp_id, fields)

            print('Done!')
    except:
        print('Error! Somthing went wrong...')
        sys.exit()


# create the argument parser
my_parser = argparse.ArgumentParser(prog='airtable-expense-grabber',
                                    description='Grab all open expenses from Airtable...',
                                    epilog='Duces! :)')

# add the program arguments
my_parser.add_argument('-l',
                       '--list',
                       metavar='list',
                       dest='LIST',
                       type=str,
                       help="downloaded expenses up until this date (ex. 2000-01-01)")

my_parser.add_argument('-m',
                       '--mark',
                       metavar='mark',
                       dest='MARK',
                       type=str,
                       help="mark expenses as submitted up until this date (ex. 2000-01-01)")

# parse the provided args
args = my_parser.parse_args()

# if no args provided
if not args.LIST and not args.MARK:
    print('No arguments provided! Use expenses -h for help.')
    sys.exit()

# testing input
# print(args)
# sys.exit()

# set variables from provided args
date = args.LIST
mark = args.MARK

if date:
    # set end date for expense report
    exp_date = cleanup_date(date)

    formatted_exp_date = exp_date.strftime('%Y-%m-%d')

    # make a temp directory to work from
    tmp_dir = tempfile.mkdtemp()

    # setup report file name and storage info
    report_name = f'Expense Report - Josh Duncan - {formatted_exp_date}.pdf'
    report_path = f'/Users/jbd/Dropbox/Documents/Carolina Apothecary/Expense Reports/{report_name}'

    print(f'Fetching all open expenses until {date}...')
    table = conn_airtbale()
    current_exp = table.get_all(view='CA - Open Expenses', sort='Date')

    if current_exp == []:
        print('There are no expenses to report... Exiting!')
        sys.exit()

    # put airtable info into pandas dataframe
    df = create_df(current_exp, exp_date)

    # generate the final table for output and print to screen
    tab_table = tabulate(df, headers='keys', tablefmt='psql', showindex=False,
                         floatfmt='.2f').replace('nan  ', 'Total', 1).replace('nan', '   ')
    print(tab_table)

    # would you like to download the final report
    print('\n')
    cont = input(
        'Would you like to download your final expense report? (y/n): ').lower()
    if cont != 'y':
        sys.exit()
    else:
        create_pdf(tab_table, exp_date, tmp_dir)
        download_pdfs(current_exp, tmp_dir, exp_date)

        # merge report and receipts
        merger = PyPDF2.PdfFileMerger()

        # grab a list of all files in the temp directory
        files = sorted([file for file in os.listdir(tmp_dir)])

        for file in files:
            file_path = f'{tmp_dir}/{file}'
            merger.append(file_path, import_bookmarks=False)
            # delete the receipts file after appending
            os.remove(file_path)

        # save the final report with attached receipts
        merger.write(report_path)

        # delete the temp directory
        os.removedirs(tmp_dir)

        print('Cleaning up...')
        print('Report created!')

        # open the report to check for correctness
        subprocess.call(['open', report_path])

        # save the date to the clipboard for the Applescript
        write_to_clipboard(f'{date},{report_path}')

        # open receipts folder
        # receipts_path = '/Users/jbd/Dropbox/Documents/Receipts'
        # subprocess.call(['open', receipts_path])

        # run the Outlook Message Applescript and attached report
        as_path = '/Users/jbd/Library/Scripts/Expense Report.scpt'
        applescript.run(as_path)

    # would you like to go ahead and mark all expenses as submitted
    print('\n')
    cont = input(
        'Would you mark all current expenses as submitted? (y/n): ').lower()
    if cont != 'y':
        sys.exit()
    else:
        mark = args.LIST

if mark:
    # set end date for marked expenses
    exp_date = cleanup_date(mark)

    mark_expense(exp_date)

sys.exit()
