#!/usr/bin/env python
from __future__ import print_function

import textwrap
import requests

from termcolor import colored
from bs4 import BeautifulSoup

from .util import try_except, render


def print_record(**kwargs):
    if 'symbol' not in kwargs:
        kwargs['symbol'] = ''

    if 'index' not in kwargs:
        kwargs['index'] = ''

    # truncate lede at 500 characters
    if len(kwargs['lede']) > 500:
        kwargs['lede'] = kwargs['lede'][:500] + ' ...'

    artist = kwargs['artist'].encode('utf-8')
    album = kwargs['album'].encode('utf-8')
    label = kwargs['label'].encode('utf-8')
    symbol = kwargs['symbol'].encode('utf-8')
    index = kwargs['index'].encode('utf-8')
    link = kwargs['link'].encode('utf-8')

    link = colored(link.strip(), 'blue')
    album = colored(album.strip(), 'yellow')
    artist = colored(artist.strip(), 'red', attrs=['bold', 'dark'])
    lede = '\n    '.join(textwrap.wrap(
        kwargs['lede'], width=70)).encode('utf-8')

    print('{}{} :: {} ({}){}'.format(index, artist, album, label, symbol))

    if 'status' in kwargs:
        status = kwargs['status']
        if status == 'NOT IN STOCK':
            status = colored(status, 'red')
        elif status == 'LOW STOCK LEVEL':
            status = colored(status, 'magenta')
        print('    {}'.format(status))

    if 'genre' in kwargs:
        genre = kwargs['genre'].encode('utf-8')
        genre = colored(genre, 'blue', attrs=['bold', 'dark'])
        print('    {}'.format(genre))

    if 'rating' in kwargs:
        rating = kwargs['rating'].encode('utf-8')
        ul_rating = colored('Rating', attrs=['underline'])
        print('    {}: {}'.format(ul_rating, rating))

    print('    "{}"'.format(lede))
    print('    {}\n'.format(link))


def allmusic(oldest_first=False):
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

    if oldest_first:
        records = records[::-1]

    for record in records:
        artist = try_except(lambda: record.find(
            'div', class_='artist').text.strip(), 'artist')
        album = try_except(lambda: record.find(
            'div', class_='title').text.strip(), 'album')
        genre = try_except(lambda: record.find(
            'div', class_='styles').text.strip(), 'genre')
        lede = try_except(lambda: record.find(
            'div', class_='headline-review').text.strip(), 'review')
        label = try_except(lambda: record.find(
            'div', class_='label').text.strip(), 'label')
        link = try_except(lambda: record.find(
            'div', class_='title').find('a').attrs['href'].strip(), 'link')

        entry = {
            'artist': artist, 'album': album, 'label': label, 'link': link,
            'genre': genre, 'lede': lede}

        print_record(**entry)


def forced_exposure(oldest_first=False):
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

    indices = range(2, 52)
    if oldest_first:
        indices = reversed(indices)

    for ix in indices:
        ix = '0' + str(ix) if ix <= 9 else ix
        prefix = 'ctl00_ContentPlaceHolder1_gvRecBestSeller_ctl{}_'.format(ix)

        artist = try_except(lambda: soup.find(
            "a", {'id': prefix + 'hlnkArtistId'}).text.strip().title(), 'artist')
        album = try_except(lambda: soup.find(
            'a', {'id': prefix + 'hrTitle'}).text.strip(), 'album')
        label = try_except(lambda: soup.find(
            'a', {'id': prefix + 'hlnkLabel'}).text.title(), 'label')
        lede = try_except(lambda: soup.find(
            'span', {'id': prefix + 'lblTx_Desc'}).text.strip(), 'review')
        status = try_except(lambda: soup.find(
            'span', {'id': prefix + 'lblStockStatus'}).text.strip(), 'status')
        link = try_except(lambda: soup.find(
            'a', {'id': prefix + 'hrTitle'}).attrs['href'].strip(), 'link')

        if 'Unknown link' not in link:
            link = 'https://www.forcedexposure.com/Catalog/{}'.format(
                link.split('../Catalog/')[1])

        entry = {
            'artist': artist, 'album': album, 'label': label, 'status': status,
            'link': link, 'lede': lede, 'index': '{}. '.format(int(ix) - 1)}

        print_record(**entry)


def pitchfork(n_pages=2, oldest_first=False):
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

    pages = range(1, n_pages + 1)
    if oldest_first:
        pages = reversed(pages)

    for pn in pages:
        url = ("https://pitchfork.com/best/high-scoring-albums/?page={}"
               .format(pn))
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html5lib')
        records = soup.find_all("div", class_="review")

        if oldest_first:
            records = records[::-1]

        for record in records:
            albums = record.find_all('h2', class_='review__title-album')
            genres = record.find_all('a', class_='genre-list__link')
            bnms = record.find_all('a', class_='review__meta-bnm')
            artists = record.find_all(
                'ul', class_='artist-list review__title-artist')
            link = try_except(lambda : record.find(
                'a', class_='review__link').attrs['href'].strip(), 'link')

            artist = try_except(
                lambda: [g.text.strip() for g in artists], 'artist')
            album = try_except(
                lambda: [g.text.strip() for g in albums], 'album')
            genre = try_except(
                lambda: [g.text.strip() for g in genres], 'genre')
            bnm = try_except(
                lambda: [g.text for g in bnms], '')

            if isinstance(artist, list):
                artist = ' / '.join(artist)
            if isinstance(album, list):
                album = ' / '.join(album)
            if isinstance(genre, list):
                genre = ' / '.join(genre)

            label, lede, rating = (
                'Unknown label', 'Unknown review', 'Unknown rating')

            if 'Unknown link' not in link:
                link = 'https://pitchfork.com{}'.format(link)

                # visit the review page to get genre, rating, & review lede
                review_html = requests.get(link).text
                review = BeautifulSoup(review_html, 'html5lib')
                rating = try_except(lambda: review.find(
                    'span', class_='score').text.strip(), 'rating')

                labels = review.find_all('li', class_='labels-list__item')

                label = try_except(
                    lambda: [g.text for g in labels], 'label')
                lede = try_except(lambda: review.find(
                    'div', class_='review-detail__abstract').text.strip(), 'review')

            if isinstance(label, list):
                label = ', '.join(label)

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


def resident_advisor(oldest_first=False):
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

    if oldest_first:
        records = records[::-1]

    for record in records:
        title = try_except(lambda: record.find('h1').text.strip(), 'album')
        artist, album = ('Unknown artist', 'Unknown album')

        if 'Unknown album' not in title:
            try:
                artist, album = title.split(' - ', 1)
            except ValueError:
                artist, album = title.split('- ', 1)

        href = try_except(lambda: record.find(
            'a').attrs['href'].strip(), 'link')
        label = try_except(lambda: record.find(
            'div', class_='sub').find('h1').text.strip(), 'label')

        rating, lede = ('Unknown rating', 'Unknown review')
        if 'Unknown link' not in href:
            link = 'https://www.residentadvisor.net{}'.format(href)

            # visit the review page to get genre, rating, & review lede
            review_html = requests.get(link).text
            review = BeautifulSoup(review_html, 'html5lib')

            rating = try_except(lambda: '{}'.format(
                review.find('span', class_='rating').text), 'rating')
            lede = try_except(lambda: review.find(
                'span', class_='reading-line-height').text.strip().split('\n')[0].strip(),
                'review')

        genre = 'Unknown genre'
        lines = try_except(lambda: review.find('ul', class_='clearfix').find_all('li'), 'lines')
        if not 'Unknown lines' in lines:
            for li in lines:
                if 'Style' in li.text:
                    genre = li.text.strip().split('Style /\n\n')[1]

        entry = {'artist': artist, 'album': album, 'label': label,
                 'genre': genre, 'link': link, 'lede': lede, 'rating': rating}
        print_record(**entry)


def boomkat(period='last-week', oldest_first=False):
    header = """
        ____                        __         __
       / __ )____  ____  ____ ___  / /______ _/ /_
      / __  / __ \/ __ \/ __ `__ \/ //_/ __ `/ __/
     / /_/ / /_/ / /_/ / / / / / / ,< / /_/ / /_
    /___________/\____/___/_/ /______|\__,_____/
       / __ )___  _____/ /_   / ___/___  / / /__  __________
      / __  / _ \/ ___/ __/   \__ \/ _ \/ / / _ \/ ___/ ___/
     / /_/ /  __(__  ) /_    ___/ /  __/ / /  __/ /  (__  )
    /_____/\___/____/\__/   /____/\___/_/_/\___/_/  /____/
    -------------------------------------------------------
    """
    print(header)

    if period not in ['last-week', 'last-month', 'last-year']:
        raise ValueError('Unrecognized period: {}'.format(period))

    url = 'https://boomkat.com/bestsellers?q[release_date]={}'.format(period)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html5lib')
    records = soup.find_all("li", class_="bestsellers-item")

    if oldest_first:
        records = records[::-1]

    for ix, record in enumerate(records):
        titles = try_except(lambda: record.find(
            'div', class_='product-name').text.strip(), 'album')
        genres = try_except(lambda: record.find(
            'div', class_='product-label-genre').text.strip(), 'genre')
        link = try_except(lambda: record.find(
            'a', class_='full-listing').attrs['href'].strip(), 'link')

        label = try_except(lambda: genres.split('\n')[0].strip(), 'label')
        genre = try_except(lambda: genres.split('\n')[-1].strip(), 'genre')
        artist = try_except(lambda: titles.split('\n')[0].strip(), 'artist')
        album = try_except(lambda: titles.split('\n')[-1].strip(), 'album')

        # visit the review page to get the review lede
        lede = 'Unknown review'
        if 'Unknown link' not in link:
            review_html = requests.get(link).text
            review = BeautifulSoup(review_html, 'html5lib')
            lede = try_except(lambda: review.find(
                'div', class_='product-review').find('strong').text.strip(), 'review')

        if oldest_first:
            ix = len(records) - ix - 1

        entry = {'artist': artist, 'album': album, 'label': label,
                 'genre': genre, 'link': link, 'lede': lede,
                 'index': '{}. '.format(ix + 1)}

        print_record(**entry)
