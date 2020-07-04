import requests
import argparse
import secrets


class color:  # terminal coloring and bolding
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


token = secrets.FINNHUB_TOKEN


def get_quotes(symbols):  # grab list of quotes from finnhub

    for symbol in symbols:
        symbol = symbol.upper()
        url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={token}'
        r = requests.get(url)
        info = r.json()

        # if symbol error returned
        if 'error' in info:
            print(
                f"{color.BOLD + symbol + color.END}: {color.RED + 'NOT SUPPORTED' + color.END}")
        else:
            change = ((info['c'] - info['pc'])/info['pc']) * 100

            if change < 0:
                change = color.RED + f'{change:.2f}' + color.END
            elif change > 0:
                change = color.GREEN + f'{change:.2f}' + color.END
            else:
                change = f'{change:.2f}'

            print(
                f"{color.BOLD + symbol + color.END}: {info['c']:.2f} ({change}%)")


# create the argument parser
my_parser = argparse.ArgumentParser(prog='market-quotes',
                                    description='Get live stock market quotes.',
                                    epilog='Duces! :)')

# add the program arguments
my_parser.add_argument('-s',
                       '--symbols',
                       metavar='SYMBOL(S)',
                       nargs='+',
                       dest='SYMBOLS',
                       type=str,
                       help="the symbol(s) to grab a quote for")

# execute the parse_args() method
args = my_parser.parse_args()

symbols = args.SYMBOLS

if symbols:
    get_quotes(symbols)
else:
    symbols = ['SPY', 'DIA', 'QQQ', 'IWM', 'VXX', 'GLD']
    get_quotes(symbols)
