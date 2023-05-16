import requests
from bs4 import BeautifulSoup
import csv
import os

date = input('Please enter a Date in the following format MM/DD/YYYY: ')
link = f'https://www.yallakora.com/match-center/?date={date}'
page = requests.get(link)


def main(page):
    src = page.content # byte code
    soup = BeautifulSoup(src, 'lxml') # parse to html code
    matches_details = []

    championships = soup.find_all('div', {'class': 'matchesList'})

    def get_match_info(championships):
        for i in range(len(championships)):
            championship_title = championships[i].contents[1].find('h2').text.strip()
            all_matches = championships[i].contents[3].find_all('li')

            number_of_matches = len(all_matches)
            for i in range(number_of_matches):
                # get teams names
                team_a = all_matches[i].find('div', {'class': 'teamA'}).find('p').text.strip()
                team_b = all_matches[i].find('div', {'class': 'teamB'}).find('p').text.strip()

                # get score
                match_result = all_matches[i].find('div', {'class': 'MResult'}).find_all('span', {'class': 'score'})
                score = f'{match_result[0].text.strip()} - {match_result[1].text.strip()}'

                #get time
                time = all_matches[i].find('div', {'class': 'MResult'}).find('span', {'class': 'time'}).text.strip()

                # add match info to matches_details
                match = {
                    'نوع البطولة': championship_title,
                    'الفريق الأول': team_a,
                    'الفريق الثاني': team_b,
                    'النتيجة': score,
                    'ميعاد المبارة': time
                }

                matches_details.append(match)



    get_match_info(championships)
    keys = matches_details[0].keys()
    dir_path = os.path.join(os.path.abspath(''), 'matches details')

    if not os.path.exists(dir_path): os.makedirs(dir_path)

    with open(os.path.join(dir_path, f'matches_details{date.replace("/","_")}.csv'), 'w') as output:
        dict_writer = csv.DictWriter(output, keys)
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print('file created')


try:
    main(page)
except IndexError:
    print('No matches for this day')

