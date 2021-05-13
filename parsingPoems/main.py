from bs4 import BeautifulSoup
import time
import re
import os
import requests

page = 0
poem_number = 1
corpr = 'https://processing.ruscorpora.ru/search.xml?doc_i_ge_birthday_e=&doc_location=&doc_cyclus=&text=meta&doc_i_ge_verses=&doc_clausula=&doc_location_normalized=&spd=1&spd=1&seed=31330&out=normal&doc_genre_fi=&doc_i_le_birthday_s=&doc_language=&doc_original=&doc_liber=&doc_i_le_verses=&sort=i_grtagging&sort=i_grtagging&doc_i_le_start_year_x=1833&env=alpha&startyear=1800&doc_rhyme=&doc_i_le_words=&doc_header=&doc_author=&lang=ru&doc_strophe=&dpp=50&dpp=50&doc_formula=&is_subcorpus=1&doc_extra=&doc_feet=&doc_strophe_gr=&doc_meter=&endyear=2019&mode=poetic&doc_i_ge_words=&doc_sex=&doc_i_ge_end_year=&p=0'
#corpr = 'https://processing.ruscorpora.ru/search.xml?doc_i_ge_birthday_e=&doc_location=&doc_cyclus=&text=meta&doc_i_ge_verses=&doc_clausula=&doc_location_normalized=&spd=1&spd=1&seed=31330&out=normal&doc_genre_fi=&doc_i_le_birthday_s=&doc_language=&doc_original=&doc_liber=&doc_i_le_verses=&sort=i_grtagging&sort=i_grtagging&doc_i_le_start_year_x=1995&env=alpha&startyear=1800&doc_rhyme=&doc_i_le_words=&doc_header=&doc_author=&lang=ru&doc_strophe=&dpp=50&dpp=50&doc_formula=&is_subcorpus=1&doc_extra=&doc_feet=&doc_strophe_gr=&doc_meter=&endyear=2019&mode=poetic&doc_i_ge_words=&doc_sex=&doc_i_ge_end_year=&p=0'

def GetHTML(link):
    global poem_number
    print('parsing poem', poem_number, '...')
    poem_number += 1
    try:
        time.sleep(0.5)
        got_link = requests.get(link).text
    except requests.exceptions.ConnectionError:
        time.sleep(5)
        got_link = requests.get(link).text
    return got_link


def GetNextPage(link):
    time.sleep(5)
    if BeautifulSoup(GetHTML(link)).find_all('p', {'class': 'pager'})[-1].find_all('a')[-1].text == "следующая страница":
        return 'http://processing.ruscorpora.ru' + \
               BeautifulSoup(GetHTML(link)).find_all('p', {'class': 'pager'})[-1].find_all('a')[-1].get('href')
    else:
        return 'end'


def GetSong(link):
    global page
    print('Loading page - ', page)
    with open(r'/home/eduard/anna_poetry/data/accentedPoems4.txt', 'a', encoding='utf-8') as f:
        poems = BeautifulSoup(GetHTML(link), 'lxml').find_all('a', {'class': 'b-kwic-expl'})
        for poem in poems:
            poem = BeautifulSoup(GetHTML('http://processing.ruscorpora.ru/' + poem.get('href').replace('nodia=1', 'nodia=0')), 'lxml').find_all('table')
            if len(poem) > 0:
                for e in poem[-1].find_all('br'):
                    e.replace_with('\n')
            try:
                poem = poem[-1].text.split('\n')[3:-12]
                poem[2] = re.sub('\d+', '', poem[2])
                poem[2] = re.sub(r"[-()\"#/@;:<>{}`+=~|]", "", poem[2])
                poem[2] = re.sub(' ― ', ' ', poem[2])
                poem[2] = re.sub('(\ ){2,}', '\n', poem[2])
                try:
                    f.write('\n'.join(poem))
                except:
                    pass
            except IndexError:
                continue
    nextPage = GetNextPage(link)
    print(nextPage)
    if nextPage != 'end':
        page += 1
        GetSong(nextPage)
    else:
        print('Done')


GetSong(corpr)
