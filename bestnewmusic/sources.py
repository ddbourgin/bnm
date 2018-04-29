#!/usr/bin/env python3
from __future__ import print_function

import textwrap
import requests

from termcolor import colored
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import TimeoutException


def render(query_url, page_load_timeout=30):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options)
    browser.set_page_load_timeout(page_load_timeout)

    try:
        browser.get(query_url)
        html_source = browser.page_source
        browser.quit()
        return html_source

    except TimeoutException:
        print("\t\tRetrying page load after {}s timeout".format(PAGE_LOAD_TIMEOUT))
        return render(query_url)


def print_record(**kwargs):
    if 'symbol' not in kwargs:
        kwargs['symbol'] = ''

    if 'index' not in kwargs:
        kwargs['index'] = ''

    # truncate lede at 500 characters
    if len(kwargs['lede']) > 500:
        kwargs['lede'] = kwargs['lede'][:500] + ' ...'

    lede = '\n    '.join(textwrap.wrap(kwargs['lede'], width=70))
    link = colored(kwargs['link'], 'blue')
    album = colored(kwargs['album'].strip(), 'yellow')
    artist = colored(kwargs['artist'].strip(), 'red', attrs=['bold', 'dark'])

    print('{}{} :: {} ({}){}'.format(
        kwargs['index'],
        artist,
        album,
        kwargs['label'],
        kwargs['symbol']
    ))

    if 'status' in kwargs:
        status = kwargs['status']
        if status == 'NOT IN STOCK':
            status = colored(status, 'red')
        elif status == 'LOW STOCK LEVEL':
            status = colored(status, 'magenta')
        print('    {}'.format(status))

    if 'genre' in kwargs:
        genre = colored(kwargs['genre'], 'blue', attrs=['bold', 'dark'])
        print('    {}'.format(genre))

    if 'rating' in kwargs:
        ul_rating = colored('Rating', attrs=['underline'])
        print('    {}: {}'.format(ul_rating, kwargs['rating']))

    print('    "{}"'.format(lede))
    print('    {}\n'.format(link))


def allmusic():
    header = """
               _ _ __  __           _
         /\   | | |  \/  |         (_)
        /  \  | | | \  / |_   _ ___ _  ___
       / /\ \ | | | |\/| | | | / __| |/ __|
      / ____ \| | | |  | | |_| \__ \ | (__
     /_/____\_\_|_|_|  |_|\__,_|___/_|\___|_____ _           _
     |  ____|  | (_) |           ( )      / ____| |         (_)
     | |__   __| |_| |_ ___  _ __|/ ___  | |    | |__   ___  _  ___ ___
     |  __| / _` | | __/ _ \| '__| / __| | |    | '_ \ / _ \| |/ __/ _ \\
     | |___| (_| | | || (_) | |    \__ \ | |____| | | | (_) | | (_|  __/
     |______\__,_|_|\__\___/|_|    |___/  \_____|_| |_|\___/|_|\___\___|
     -------------------------------------------------------------------
    """
    print(header)

    url = "https://www.allmusic.com/newreleases/editorschoice"
    html = render(url)
    soup = BeautifulSoup(html, 'html5lib')
    records = soup.find_all('div', class_='editors-choice')

    for record in records:
        artist = record.find('div', class_='artist').text.strip()
        album = record.find('div', class_='title').text.strip()
        genre = record.find('div', class_='styles').text.strip()
        lede = record.find('div', class_='headline-review').text.strip()
        link = record.find('div', class_='title').find('a').attrs['href']
        try:
            label = record.find('div', class_='label').text.strip()
        except AttributeError:
            # sometimes AMG forgets to add label info...
            label = 'Unknown Label'

        entry = {
            'artist': artist, 'album': album, 'label': label, 'link': link,
            'genre': genre, 'lede': lede}

        print_record(**entry)


def forced_exposure():
    header = """
     ___  __   __   __   ___  __      ___      __   __   __        __   ___
    |__  /  \ |__) /  ` |__  |  \    |__  \_/ |__) /  \ /__` |  | |__) |__
    |    \__/ |  \ \__, |___ |__/    |___ / \ |    \__/ .__/ \__/ |  \ |___

             __   ___  __  ___     __   ___            ___  __   __
            |__) |__  /__`  |     /__` |__  |    |    |__  |__) /__`
            |__) |___ .__/  |     .__/ |___ |___ |___ |___ |  \ .__/
    -----------------------------------------------------------------------
    """
    print(header)

    url = "https://www.forcedexposure.com/Best/BestIndex.html"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html5lib')

    for ix in range(2, 52):
        ix = '0' + str(ix) if ix <= 9 else ix
        prefix = 'ctl00_ContentPlaceHolder1_gvRecBestSeller_ctl{}_'.format(ix)
        artist = soup.find("a", {'id': prefix + 'hlnkArtistId'}).text.title()
        album = soup.find('a', {'id': prefix + 'hrTitle'}).text
        label = soup.find('a', {'id': prefix + 'hlnkLabel'}).text.title()
        lede = soup.find('span', {'id': prefix + 'lblTx_Desc'}).text
        status = soup.find('span', {'id': prefix + 'lblStockStatus'}).text
        link = soup.find('a', {'id': prefix + 'hrTitle'}).attrs['href']
        link = 'https://www.forcedexposure.com/Catalog/{}'.format(
            link.split('../Catalog/')[1])

        artist = artist.strip()
        album = album.strip()

        entry = {
            'artist': artist, 'album': album, 'label': label, 'status': status,
            'link': link, 'lede': lede, 'index': '{}. '.format(int(ix) - 1)}

        print_record(**entry)


def pitchfork(n_pages=2):
    header = """
           ___ _ _       _      __            _
          / _ (_) |_ ___| |__  / _| ___  _ __| | __
         / /_)/ | __/ __| '_ \| |_ / _ \| '__| |/ /
        / ___/| | || (__| | | |  _| (_) | |  |   <
        \/    |_|\__\___|_| |_|_|  \___/|_|  |_|\_\\
      ___   ___            _   _ _
     ( _ ) / _ \   _      /_\ | | |__  _   _ _ __ ___  ___
     / _ \| | | |_| |_   //_\\\\| | '_ \| | | | '_ ` _ \/ __|
    | (_) | |_| |_   _| /  _  \ | |_) | |_| | | | | | \__ \\
     \___(_)___/  |_|   \_/ \_/_|_.__/ \__,_|_| |_| |_|___/
    ---------------------------------------------------------
    """
    print(header)

    for pn in range(1, n_pages + 1):
        url = ("https://pitchfork.com/best/high-scoring-albums/?page={}"
               .format(pn))
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html5lib')
        records = soup.find_all("div", class_="review")

        for idx, record in enumerate(records):
            albums = record.find_all('h2', class_='review__title-album')
            genres = record.find_all('a', class_='genre-list__link')
            bnms = record.find_all('a', class_='review__meta-bnm')
            link = record.find('a', class_='review__link').attrs['href']
            artists = record.find_all(
                'ul', class_='artist-list review__title-artist')

            artist = [g.text.strip() for g in artists]
            album = [g.text.strip() for g in albums]
            genre = [g.text.strip() for g in genres]
            bnm = [g.text for g in bnms]
            link = 'https://pitchfork.com{}'.format(link)

            # visit the review page to get genre, rating, & review lede
            review_html = requests.get(link).text
            review = BeautifulSoup(review_html, 'html5lib')
            rating = review.find('span', class_='score').text
            labels = review.find_all('li', class_='labels-list__item')

            label = [g.text for g in labels]
            lede = (review.find('div', class_='review-detail__abstract')
                    .text.strip())

            artist = ' / '.join(artist)
            album = ' / '.join(album)
            label = ', '.join(label)
            genre = ' / '.join(genre)

            symbol = ''
            if 'Best New Reissue' in bnm:
                symbol = colored('**', 'red', attrs=['bold'])
            elif 'Best New Album' in bnm:
                symbol = colored('*', 'red', attrs=['bold'])

            entry = {'artist': artist, 'album': album, 'label': label, 'genre': genre,
                     'link': link, 'lede': lede, 'rating': rating, 'symbol': symbol}
            print_record(**entry)

    print('{} = Best New Album'.format(colored('*', 'red', attrs=['bold'])))
    print('{} = Best New Reissue'.format(colored('**', 'red', attrs=['bold'])))


def resident_advisor():
    header = """
       __    _       __                                                   _
      /__\  /_\     /__\ ___  ___ ___  _ __ ___  _ __ ___   ___ _ __   __| |___
     / \// //_\\\\   / \/// _ \/ __/ _ \| '_ ` _ \| '_ ` _ \ / _ \ '_ \ / _` / __|
    / _  \/  _  \ / _  \  __/ (_| (_) | | | | | | | | | | |  __/ | | | (_| \__ \\
    \/ \_/\_/ \_/ \/ \_/\___|\___\___/|_| |_| |_|_| |_| |_|\___|_| |_|\__,_|___/
    ---------------------------------------------------------------------------
    """
    print(header)

    url = "https://www.residentadvisor.net/reviews.aspx?format=recommend"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html5lib')
    records = soup.find_all("li", class_="min-height-medium")

    for record in records:
        title = record.find('h1').text
        href = record.find('a').attrs['href']
        link = 'https://www.residentadvisor.net{}'.format(href)
        label = record.find('div', class_='sub').find('h1').text

        try:
            artist, album = title.split(' - ', maxsplit=1)
        except ValueError:
            artist, album = title.split('- ', maxsplit=1)

        # visit the review page to get genre, rating, & review lede
        review_html = requests.get(link).text
        review = BeautifulSoup(review_html, 'html5lib')
        rating = '{}'.format(review.find('span', class_='rating').text)
        lede = (review.find('span', class_='reading-line-height')
                .text.strip().split('\n')[0])

        genre = 'Unknown genre'
        for li in review.find('ul', class_='clearfix').find_all('li'):
            if 'Style' in li.text:
                genre = li.text.strip().split('Style /\n\n')[1]

        entry = {'artist': artist, 'album': album, 'label': label,
                'genre': genre, 'link': link, 'lede': lede, 'rating': rating}
        print_record(**entry)