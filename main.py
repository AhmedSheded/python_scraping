import requests
from bs4 import BeautifulSoup
import csv

date = input('Please enter a Date in the following format MM/DD/YYYY: ')
link = f'https://www.yallakora.com/match-center/?date={date}'
page = requests.get(link)


def main(page):
    pass

