import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import date, timedelta
import pandas as pd

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date= input('Enter a start date formatted as YYYY/MM/DD: ')
start_year, start_month, start_day = start_date.split('/')

end_date= input('Enter an end date formatted as YYYY/MM/DD: ')
end_year, end_month, end_day = end_date.split('/')

start_date = date(int(start_year), int(start_month), int(start_day))
end_date = date(int(end_year), int(end_month), int(end_day))

dir_path = os.path.join(os.path.abspath(''), 'matches details')




def main(date):
    link = f'https://www.yallakora.com/match-center/?date={date}'
    page = requests.get(link)

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
                    'Championship': championship_title,
                    'Team A': team_a,
                    'Team B': team_b,
                    'Score': score,
                    'Time': time,
                    'Date': date
                }

                matches_details.append(match)



    get_match_info(championships)
    keys = matches_details[0].keys()


    if not os.path.exists(dir_path): os.makedirs(dir_path)

    with open(os.path.join(dir_path, f'matches_details{date.replace("/","_")}.csv'), 'w') as output:
        dict_writer = csv.DictWriter(output, keys)
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print(f'file created for {date}')


for single_date in daterange(start_date, end_date):
    try:
        main(single_date.strftime('%m/%d/%Y'))

    except IndexError:
        print('No matches for this day')

merge= input('do you want to merge files y/n: ')

if merge =='y' or merge == 'Y':
    files = os.listdir(dir_path)
    df = pd.DataFrame()
    for file in files:
        data = pd.read_csv(os.path.join(dir_path, file))
        df = pd.concat([df, data], axis=0)
        os.remove(os.path.join(dir_path, file))
    df.to_csv(os.path.join(dir_path, f'matches_details_from_{start_date} to {end_date}.csv'), index=False)

