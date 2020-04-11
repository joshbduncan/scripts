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


# TODO no expenses exist
# TODO no expenses to mark submitted


# import secrets and set variables
AIRTABLE_KEY = secrets.AIRTABLE_KEY
AIRTABLE_TOKEN = secrets.AIRTABLE_TOKEN
AIRTABLE_URL = secrets.AIRTABLE_URL
AIRTABLE_BASE = secrets.AIRTABLE_BASE
AIRTABLE_TABLE = secrets.AIRTABLE_TABLE


def write_to_clipboard(output):
    # Write to clipboard for Applescript function
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))


def conn_airtbale():
    try:
        conn = airtable.Airtable(
            AIRTABLE_BASE, AIRTABLE_TABLE, api_key=AIRTABLE_KEY)
    except:
        print("Error! Couldn't connect to Airtable")

    return conn


def download_pdfs(expenses, tmp_dir):

    print(f'Downloading {len(expenses)} receipt(s)...')

    for expense in expenses:
        exp_id = expense['id']
        file_path = f'{tmp_dir}/{exp_id}.pdf'
        url = expense['fields']['Receipt'][0]['url']
        receipt = requests.get(url)

        with open(file_path, 'wb') as f:
            f.write(receipt.content)

    return tmp_dir


def create_df(data, exp_date):
    # Setup Pandas dataframe
    df = pd.DataFrame()

    # Setup lists for found record(s) info
    dates = []
    descriptions = []
    companies = []
    vendors = []
    amounts = []

    # Iterate through found record(s) and insert data into lists
    for record in data:
        if datetime.strptime(record['fields']['Date'], '%Y-%m-%d') <= exp_date:
            dates.append(record['fields']['Date'])
            companies.append(record['fields']['Company (Card)'])
            vendors.append(record['fields']['Vendor'])
            descriptions.append(record['fields']['Description'])
            amounts.append(record['fields']['Amount'])

    # Fill in the Pandas dataframe
    df['Date'] = dates
    df['Description'] = descriptions
    df['Company (Card)'] = companies
    df['Vendor'] = vendors
    df['Amount'] = amounts

    # Add in a total line
    df.loc['Total'] = pd.Series(df['Amount'].sum(), index=['Amount'])
    total = df['Amount'].sum()

    return df


def create_pdf(table, exp_date, tmp_dir):
    # Format data and set PDF filename and output path
    formatted_exp_date = exp_date.strftime('%Y-%m-%d')
    path = f'{tmp_dir}/1.pdf'

    # Setup PDF page and add in info
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

    # Output the final PDF and open it up in Preview
    pdf.output(path, 'F')


def mark_expense():
    try:
        table = conn_airtbale()
        current_exp = table.get_all(view='Current Expenses', sort='Date')

        if current_exp == []:
            print('There are no current expenses to mark!')
        else:
            for expense in current_exp:
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
my_parser.add_argument('-d',
                       '--date',
                       metavar='date',
                       dest='DATE',
                       type=str,
                       help="grab expenses up until this date (ex. 2000-01-01)")

my_parser.add_argument('-m',
                       '--mark',
                       action="store_true",
                       dest='MARK',
                       help="mark expenses as submitted"
                       )

# execute the parse_args() methos
args = my_parser.parse_args()

# set the path to iterate through
date = args.DATE
mark = args.MARK

if date:
    # Set end date for expense report
    try:
        year = int(date.split('-')[0])
        month = int(date.split('-')[1])
        day = int(date.split('-')[2])
        exp_date = datetime(year, month, day)
    except:
        print('Not a valid date! Pleas change date and run again.')
        exit()

    formatted_exp_date = exp_date.strftime('%Y-%m-%d')
    tmp_dir = tempfile.mkdtemp()
    report_name = f'Expense Report - Josh Duncan - {formatted_exp_date}.pdf'
    report_path = f'/Users/jbd/Dropbox/Carolina Apothecary/Documents/Expense Reports/{report_name}'

    # print(tmp_dir)

    print(f'Fetching all open expenses until {date}...')

    table = conn_airtbale()
    current_exp = table.get_all(view='Current Expenses', sort='Date')

    df = create_df(current_exp, exp_date)

    # Generate the final table for output
    tab_table = tabulate(df, headers='keys', tablefmt='psql', showindex=False,
                         floatfmt='.2f').replace('nan  ', 'Total', 1).replace('nan', '   ')

    create_pdf(tab_table, exp_date, tmp_dir)

    download_pdfs(current_exp, tmp_dir)

    # merge report and receipts
    merger = PyPDF2.PdfFileMerger()

    files = sorted([file for file in os.listdir(tmp_dir)])

    for file in files:
        # print(file)
        file_path = f'{tmp_dir}/{file}'

        merger.append(file_path)
        os.remove(file_path)

    merger.write(report_path)

    os.removedirs(tmp_dir)

    print('Cleaning up...')
    print('Report created!')

    subprocess.call(['open', report_path])

    # Save the date to the clipboard for the Applescript
    write_to_clipboard(f'{date},{report_path}')

    # Open receipts folder
    receipts_path = f'/Users/jbd/Dropbox/Carolina Apothecary/Documents/Expense Reports/Receipts'
    subprocess.call(['open', receipts_path])

    # Run the Outlook Message Applescript
    as_path = '/Users/jbd/Library/Scripts/Expense Report.scpt'
    applescript.run(as_path)

if mark:
    mark_expense()

sys.exit()
