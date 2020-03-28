#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function

import textwrap
import time
import os.path as op

import requests
from bs4 import BeautifulSoup
from termcolor import colored

from .util import try_except, strip, SPACE_HYPHEN_SPACE, HYPHEN_SPACE


def print_record(**kwargs):
    if "symbol" not in kwargs:
        kwargs["symbol"] = ""

    if "index" not in kwargs:
        kwargs["index"] = ""

    artist = strip(kwargs["artist"]).encode("utf-8").decode("utf-8")
    album = strip(kwargs["album"]).encode("utf-8").decode("utf-8")
    label = strip(kwargs["label"]).encode("utf-8").decode("utf-8")
    symbol = strip(kwargs["symbol"]).encode("utf-8").decode("utf-8")
    index = kwargs["index"].encode("utf-8").decode("utf-8")

    album = colored(album, "yellow")
    artist = colored(artist, "red", attrs=["bold", "dark"])

    print("{}{} :: {} ({}){}".format(index, artist, album, label, symbol))

    if "status" in kwargs:
        status = kwargs["status"]
        if status == "NOT IN STOCK":
            status = colored(status, "red")
        elif status == "LOW STOCK LEVEL":
            status = colored(status, "magenta")
        print("    {}".format(status))

    if "genre" in kwargs:
        genre = strip(kwargs["genre"]).encode("utf-8").decode("utf-8")
        genre = colored(genre, "blue", attrs=["bold", "dark"])
        print("    {}".format(genre))

    if "rating" in kwargs:
        rating = strip(kwargs["rating"]).encode("utf-8").decode("utf-8")
        ul_rating = colored("Rating", attrs=["underline"])
        print("    {}: {}".format(ul_rating, rating))

    if "lede" in kwargs:
        #  truncate lede at 500 characters
        if len(kwargs["lede"]) > 500:
            kwargs["lede"] = kwargs["lede"][:500].strip() + " ..."

        lede = (
            "\n    ".join(textwrap.wrap(kwargs["lede"], width=70))
            .encode("utf-8")
            .decode("utf-8")
        )
        print('    "{}"'.format(lede))

    if "link" in kwargs:
        link = strip(kwargs["link"]).encode("utf-8").decode("utf-8")
        link = colored(link.strip(), "blue")
        print("    {}\n".format(link))


def allmusic(oldest_first=False, n_items=None):
    from .util import render

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

    star_map = {
        "10": "5",
        "9": "5",
        "8": "4.5",
        "7": "4",
        "6": "3.5",
        "5": "3",
        "4": "2.5",
        "3": "2",
        "2": "1.5",
        "1": "1",
    }
    url = "https://www.allmusic.com/newreleases/editorschoice"
    html = render(url)
    soup = BeautifulSoup(html, "html5lib")
    records = soup.find_all("div", class_="editors-choice-item")

    if oldest_first:
        records = records[::-1]

    for ix, record in enumerate(records):
        if n_items and ix == n_items:
            break

        artist = try_except(
            lambda: record.find("div", class_="artist").text.strip(), "artist"
        )
        album = try_except(
            lambda: record.find("div", class_="title").text.strip(), "album"
        )
        genre = try_except(
            lambda: record.find("div", class_="genres").text.strip(), "genre"
        )
        lede = try_except(
            lambda: record.find("div", class_="headline-review").text.strip(), "review"
        )
        label = try_except(
            lambda: record.find("div", class_="labels").text.strip(), "label"
        )
        link = try_except(
            lambda: record.find("div", class_="title").find("a").attrs["href"].strip(),
            "link",
        )
        rating = try_except(
            lambda: record.find("span", class_="allmusic-rating").attrs["class"][-1],
            "rating",
        )

        if "Unknown rating" not in rating:
            rating = star_map[rating.split("rating-allmusic-")[-1]]

        entry = {
            "artist": artist,
            "album": album,
            "label": label,
            "link": link,
            "genre": genre,
            "lede": lede,
            "rating": rating,
        }

        print_record(**entry)


def forced_exposure(oldest_first=False, n_items=None):
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
    soup = BeautifulSoup(html, "html5lib")

    indices = range(2, 52)
    if oldest_first:
        indices = reversed(indices)

    for ix in indices:
        if n_items and (ix - 2) == n_items:
            break

        ix = "0" + str(ix) if ix <= 9 else ix
        prefix = "ctl00_ContentPlaceHolder1_gvRecBestSeller_ctl{}_".format(ix)

        artist = try_except(
            lambda: soup.find("a", {"id": prefix + "hlnkArtistId"})
            .text.strip()
            .title(),
            "artist",
        )
        album = try_except(
            lambda: soup.find("a", {"id": prefix + "hrTitle"}).text.strip(), "album"
        )
        label = try_except(
            lambda: soup.find("a", {"id": prefix + "hlnkLabel"}).text.title(), "label"
        )
        lede = try_except(
            lambda: soup.find("span", {"id": prefix + "lblTx_Desc"}).text.strip(),
            "review",
        )
        status = try_except(
            lambda: soup.find("span", {"id": prefix + "lblStockStatus"}).text.strip(),
            "status",
        )
        link = try_except(
            lambda: soup.find("a", {"id": prefix + "hrTitle"}).attrs["href"].strip(),
            "link",
        )

        if "Unknown link" not in link:
            link = "https://www.forcedexposure.com/Catalog/{}".format(
                link.split("../Catalog/")[1]
            )

        entry = {
            "artist": artist,
            "album": album,
            "label": label,
            "status": status,
            "link": link,
            "lede": lede,
            "index": "{}. ".format(int(ix) - 1),
        }

        print_record(**entry)


def pitchfork(n_pages=2, oldest_first=False, n_items=None):
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

    ix = -1
    for pn in pages:
        url = "https://pitchfork.com/best/high-scoring-albums/?page={}".format(pn)
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html5lib")
        records = soup.find_all("div", class_="review")

        if oldest_first:
            records = records[::-1]

        for record in records:
            ix += 1
            if n_items and ix >= n_items:
                break

            albums = record.find_all("h2", class_="review__title-album")
            genres = record.find_all("a", class_="genre-list__link")
            bnms = record.find_all("a", class_="review__meta-bnm")
            artists = record.find_all("ul", class_="artist-list review__title-artist")
            link = try_except(
                lambda: record.find("a", class_="review__link").attrs["href"].strip(),
                "link",
            )

            artist = try_except(
                lambda: set([g.text.strip() for g in artists[0].children]), "artist"
            )
            album = try_except(lambda: set([g.text.strip() for g in albums]), "album")
            genre = try_except(lambda: set([g.text.strip() for g in genres]), "genre")
            bnm = try_except(lambda: set([g.text for g in bnms]), "")

            if isinstance(artist, (list, set)):
                artist = " + ".join(artist)
            if isinstance(album, (list, set)):
                album = " / ".join(album)
            if isinstance(genre, (list, set)):
                genre = " / ".join(genre)

            label, lede, rating = ("Unknown label", "Unknown review", "Unknown rating")

            if "Unknown link" not in link:
                link = "https://pitchfork.com{}".format(link)

                # visit the review page to get genre, rating, & review lede
                review_html = requests.get(link).text
                review = BeautifulSoup(review_html, "html5lib")
                rating = try_except(
                    lambda: review.find("span", class_="score").text.strip(), "rating"
                )

                labels = review.find_all("li", class_="labels-list__item")

                label = try_except(
                    lambda: set([g.text.strip() for g in labels]), "label"
                )
                lede = try_except(
                    lambda: review.find(
                        "div", class_="review-detail__abstract"
                    ).text.strip(),
                    "review",
                )

            if isinstance(label, (list, set)):
                label = ", ".join(label)

            symbol = ""
            if "Best New Reissue" in bnm:
                symbol = colored("**", "red", attrs=["bold"])
            elif "Best New Album" in bnm:
                symbol = colored("*", "red", attrs=["bold"])

            entry = {
                "artist": artist,
                "album": album,
                "label": label,
                "genre": genre,
                "link": link,
                "lede": lede,
                "rating": rating,
                "symbol": symbol,
            }

            print_record(**entry)

    print("{} = Best New Album".format(colored("*", "red", attrs=["bold"])))
    print("{} = Best New Reissue".format(colored("**", "red", attrs=["bold"])))


def resident_advisor(oldest_first=False, n_items=None):
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
    soup = BeautifulSoup(html, "html5lib")
    records = soup.find_all("li", class_="min-height-medium")

    if oldest_first:
        records = records[::-1]

    for ix, record in enumerate(records):
        if n_items and ix == n_items:
            break

        title = try_except(lambda: record.find("h1").text.strip(), "album")
        artist, album = ("Unknown artist", "Unknown album")

        if "Unknown album" not in title:
            try:
                artist, album = SPACE_HYPHEN_SPACE.split(title, 1)
            except ValueError:
                artist, album = HYPHEN_SPACE.split(title, 1)

        href = try_except(lambda: record.find("a").attrs["href"].strip(), "link")
        label = try_except(
            lambda: record.find("div", class_="sub").find("h1").text.strip(), "label"
        )

        rating, lede = ("Unknown rating", "Unknown review")
        if "Unknown link" not in href:
            link = "https://www.residentadvisor.net{}".format(href)

            # visit the review page to get genre, rating, & review lede
            review_html = requests.get(link).text
            review = BeautifulSoup(review_html, "html5lib")

            rating = try_except(
                lambda: "{}".format(review.find("span", class_="rating").text), "rating"
            )
            lede = try_except(
                lambda: review.find("span", class_="reading-line-height")
                .text.strip()
                .split("\n")[0]
                .strip(),
                "review",
            )

        genre = "Unknown genre"
        lines = try_except(
            lambda: review.find("ul", class_="clearfix").find_all("li"), "lines"
        )
        if not "Unknown lines" in lines:
            for li in lines:
                if "Style" in li.text:
                    genre = li.text.strip().split("Style /\n\n")[1].replace("\n", " ")

        entry = {
            "artist": artist,
            "album": album,
            "label": label,
            "genre": genre,
            "link": link,
            "lede": lede,
            #  "rating": rating, # RA doesn't include ratings anymore!
        }
        print_record(**entry)


def boomkat(period="last-week", oldest_first=False, n_items=None):
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

    if period not in ["last-week", "last-month", "last-year"]:
        raise ValueError("Unrecognized period: {}".format(period))

    url = "https://boomkat.com/bestsellers?q[release_date]={}".format(period)
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")
    records = soup.find_all("li", class_="bestsellers-item")

    if oldest_first:
        records = records[::-1]

    for ix, record in enumerate(records):
        if n_items and ix == n_items:
            break

        titles = try_except(
            lambda: record.find("div", class_="product-name").text.strip(), "album"
        )
        genres = try_except(
            lambda: record.find("div", class_="product-label-genre").text.strip(),
            "genre",
        )
        link = try_except(
            lambda: record.find("a", class_="full-listing").attrs["href"].strip(),
            "link",
        )

        label = try_except(lambda: genres.split("\n")[0].strip(), "label")
        genre = try_except(lambda: genres.split("\n")[-1].strip(), "genre")
        artist = try_except(lambda: titles.split("\n")[0].strip(), "artist")
        album = try_except(lambda: titles.split("\n")[-1].strip(), "album")

        # visit the review page to get the review lede
        lede = "Unknown review"
        if "Unknown link" not in link:
            review_html = requests.get(link).text
            review = BeautifulSoup(review_html, "html5lib")
            lede = try_except(
                lambda: review.find("div", class_="product-review")
                .find("strong")
                .text.strip(),
                "review",
            )

        if oldest_first:
            ix = len(records) - ix - 1

        entry = {
            "artist": artist,
            "album": album,
            "label": label,
            "genre": genre,
            "link": link,
            "lede": lede,
            "index": "{}. ".format(ix + 1),
        }

        print_record(**entry)


def wfmu(oldest_first=False, n_items=None):
    def print_airplay_list(tds, list_ix, name, n_items):
        print("")
        print(colored("{} AIRPLAY".format(name.upper()), attrs=["underline"]))
        records = tds[list_ix].find_all("li")
        enum = 1
        for ix, record in enumerate(records):
            if n_items and enum == n_items + 1:
                break

            artist, rest = SPACE_HYPHEN_SPACE.split(record.text, 1)

            album, label = rest.rsplit("(", 1)
            album = album.strip().strip()
            label = label.replace(")", "").strip()
            entry = {
                "artist": artist,
                "album": album,
                "label": label,
                "index": "    {:>2}. ".format(enum),
            }
            print_record(**entry)
            time.sleep(0.15)
            enum += 1

    header = """
    888       888 8888888888 888b     d888 888     888
    888   o   888 888        8888b   d8888 888     888
    888  d8b  888 888        88888b.d88888 888     888
    888 d888b 888 8888888    888Y88888P888 888     888
    888d88888b888 888        888 Y888P 888 888     888
    88888P Y88888 888        888  Y8P  888 888     888
    8888P   Y8888 888        888   "   888 Y88b. .d88P
    888P     Y888 888        888       888  "Y88888P"

    Most Played: Week of {}
    {}
    {}"""
    url = "http://www.wfmu.org/Playlists/Wfmu"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")

    # get the most recent week's list
    list_element = soup.find_all("a", class_="playlist")[0]
    week_id = list_element.text

    week_url = list_element.attrs["href"]
    week_html = requests.get(week_url).text
    soup = BeautifulSoup(week_html, "html5lib")
    tds = soup.find_all("td", class_="mcnTextBlockInner")

    next_entry = lambda x: x + 1
    if oldest_first:
        tds = tds[::-1]
        next_entry = lambda x: x - 1

    week_url = colored("{}".format(week_url), "blue")
    print(header.format(week_id, week_url, "-" * (len(week_url) - 9)))

    for ix, td in enumerate(tds):
        if "heavy airplay" in td.text.lower():
            print_airplay_list(tds, next_entry(ix), "heavy", n_items)
        elif "medium airplay" in td.text.lower():
            print_airplay_list(tds, next_entry(ix), "medium", n_items)
        elif "light airplay" in td.text.lower():
            print_airplay_list(tds, next_entry(ix), "light", n_items)


def stranded(oldest_first=False, n_items=30):
    header = """
     .d8888b.  888                                  888               888
    d88P  Y88b 888                                  888               888
    Y88b.      888                                  888               888
     "Y888b.   888888 888d888 8888b.  88888b.   .d88888  .d88b.   .d88888
        "Y88b. 888    888P"      "88b 888 "88b d88" 888 d8P  Y8b d88" 888
          "888 888    888    .d888888 888  888 888  888 88888888 888  888
    Y88b  d88P Y88b.  888    888  888 888  888 Y88b 888 Y8b.     Y88b 888
     "Y8888P"   "Y888 888    "Y888888 888  888  "Y88888  "Y8888   "Y88888
    ---------------------------------------------------------------------
    """
    print(header)

    base = "https://www.strandedrecords.com"
    url = op.join(base, "collections/recommended")
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")
    records = soup.find_all("div", class_="details")

    if oldest_first:
        records = records[::-1]

    for ix, record in enumerate(records):
        if n_items and ix == n_items:
            break

        link = op.join(base, record.find("a", class_="clearfix").attrs["href"][1:])
        title = record.find("h4", class_="title").text
        artist, album = SPACE_HYPHEN_SPACE.split(title, 1)
        label = record.find("span", class_="vendor").text
        album = album.replace(" LP", "").strip()
        artist = artist.strip()

        detail_soup = BeautifulSoup(requests.get(link).text, "html5lib")
        paragraphs = detail_soup.find("div", class_="description").find_all("p")
        lede = "\n".join(
            [p.text.strip() for p in paragraphs if not p.text.startswith("Label")]
        )

        entry = {
            "artist": artist,
            "album": album,
            "label": label,
            "link": link,
            "lede": lede,
        }

        print_record(**entry)


def kalx(oldest_first=False, n_items=None):
    header = """
    88      a8P          db         88           8b        d8
    88    ,88'          d88b        88            Y8,    ,8P
    88  ,88"           d8'`8b       88             `8b  d8'
    88,d88'           d8'  `8b      88               Y88P
    8888"88,         d8YaaaaY8b     88               d88b
    88P   Y8b       d8\"\"\"\"\"\"\"\"8b    88             ,8P  Y8,
    88     "88,    d8'        `8b   88            d8'    `8b
    88       Y8b  d8'          `8b  88888888888  8P        Y8

    Most Played: {}
    {}
    ----------------------------------------------------------
    """

    url = "https://www.kalx.berkeley.edu/charts/top-35"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")

    # get the most recent week's list
    week_id = soup.find("h3").text
    records = soup.find_all("div", class_="item-list")[1].find_all("span")

    if oldest_first:
        records = records[::-1]

    week_url = colored("{}".format(url), "blue")
    print(header.format(week_id, week_url))

    for ix, record in enumerate(records):
        if n_items and ix == n_items:
            break

        album_label = record.text.split("|")[1].strip()
        album, label = album_label.rsplit("(", 1)
        album = album.strip()
        label = label.replace(")", "").strip()
        artist = record.find("strong").text.strip()
        entry = {
            "artist": artist,
            "album": album,
            "label": label,
            "index": "    {:>2}. ".format(ix + 1),
        }
        print_record(**entry)
        time.sleep(0.15)


def midheaven(oldest_first=False, n_items=None):
    header = """
                    d8,      d8b  d8b
                   `8P       88P  ?88
                            d88    88b
      88bd8b,d88b   88b d888888    888888b  d8888b d888b8b  ?88   d8P d8888b  88bd88b
      88P'`?8P'?8b  88Pd8P' ?88    88P `?8bd8b_,dPd8P' ?88  d88  d8P'd8b_,dP  88P' ?8b
     d88  d88  88P d88 88b  ,88b  d88   88P88b    88b  ,88b ?8b ,88' 88b     d88   88P
    d88' d88'  88bd88' `?88P'`88bd88'   88b`?888P'`?88P'`88b`?888P'  `?888P'd88'   88b
     d8b                                                 d8b  d8b
     ?88                        d8P                      88P  88P
      88b                    d888888P                   d88  d88
      888888b  d8888b .d888b,  ?88'       .d888b, d8888b888  888   d8888b  88bd88b .d888b,
      88P `?8bd8b_,dP ?8b,     88P        ?8b,   d8b_,dP?88  ?88  d8b_,dP  88P'  ` ?8b,
     d88,  d8888b       `?8b   88b          `?8b 88b     88b  88b 88b     d88        `?8b
    d88'`?88P'`?888P'`?888P'   `?8b      `?888P' `?888P'  88b  88b`?888P'd88'     `?888P'
    --------------------------------------------------------------------------------------
    """
    print(header)

    url = "https://www.midheaven.com/top-selling"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")
    records = soup.find_all("div", class_="uk-panel uk-panel-box")

    if oldest_first:
        records = records[::-1]

    for ix, record in enumerate(records):
        if n_items and ix == n_items:
            break

        artist = try_except(lambda: record.find("h4").text.strip(), "artist")
        album = try_except(lambda: record.find("h5").text.strip(), "album")
        label = try_except(lambda: record.find("h6").text.strip(), "label")
        href = try_except(
            lambda: record.find("div", class_="uk-panel-teaser")
            .find("a")
            .attrs["href"]
            .strip(),
            "link",
        )

        if "Unknown link" not in href:
            link = "http://www.midheaven.com{}".format(href)

            # visit the review page to get genre, rating, & review lede
            review_html = requests.get(link).text
            review = BeautifulSoup(review_html, "html5lib")

            lede = try_except(
                lambda: review.find("div", class_="item-meta").text.strip(), "review"
            )

        if oldest_first:
            ix = len(records) - ix - 1

        entry = {
            "artist": artist,
            "album": album,
            "label": label,
            "link": link,
            "lede": lede,
            "index": "{}. ".format(ix + 1),
        }

        print_record(**entry)


def metacritic(oldest_first=False):
    from .util import render

    header = """
                  .-.
                    /|/|         /                   .-.    /  .-.
                   /   |  .-.---/---.-.  .-.    ).--.`-'---/---`-'.-.
                  /    |./.-'_ /   (  | (      /    /     /   /  (
             .-' /     |(__.' /     `-'-'`---'/  _.(__.  / _.(__. `---'
            (__.'      `.
       .-.                             .-.
      (_) )-.                /           /|/|         /
         / __)    .-.  . ---/---        /   |  .-.---/---.-.    .  .-.  .-._.).--..-.
        /    `. ./.-'_/ \  /           /    |./.-'_ /   (  |   / \(    (   )/   ./.-'_
       /'      )(__.'/ ._)/       .-' /     |(__.' /     `-'-'/ ._)`---'`-'/    (__.'
    (_/  `----'     /            (__.'      `.               /
    ---------------------------------------------------------------------------------
    """
    print(header)

    url = "http://www.metacritic.com/browse/albums/release-date/new-releases/metascore?view=detailed"
    html = render(url)
    soup = BeautifulSoup(html, "html5lib")
    records = soup.find_all("td", class_="clamp-summary-wrap")
    records = records[:35]

    if oldest_first:
        records = records[::-1]

    for ix, record in enumerate(records):
        album = try_except(
            lambda: record.find("h3", class_="product_title").find("a").text.strip(),
            "album",
        )
        artist = try_except(
            lambda: SPACE_HYPHEN_SPACE.split(
                record.find("span", class_="product_artist").text
            )[-1].strip(),
            "artist",
        )
        genres = try_except(
            lambda: record.find("li", class_="stat genre")
            .find("span", class_="data")
            .text.split(", "),
            "genre",
        )
        href = try_except(
            lambda: record.find("h3", class_="product_title")
            .find("a")
            .attrs["href"]
            .strip(),
            "link",
        )
        rating = try_except(
            lambda: record.find("a", class_="basic_stat product_score").text.strip(),
            "rating",
        )

        genre = try_except(lambda: [g.strip() for g in genres], "genre")

        if isinstance(genre, list):
            genre = " / ".join([g for g in genre if "..." not in g])

        if "Unknown link" not in href:
            link = "http://www.metacritic.com{}".format(href)

            # visit the review page to get genre, rating, & review lede
            review_html = render(link)
            review = BeautifulSoup(review_html, "html5lib")

            lede = try_except(
                lambda: review.find("li", class_="summary_detail product_summary")
                .find("span", class_="data")
                .text.strip(),
                "review",
            )
            label = try_except(
                lambda: review.find("li", class_="summary_detail product_company")
                .find("span", class_="data")
                .text.strip(),
                "label",
            )

        if oldest_first:
            ix = len(records) - ix - 1

        entry = {
            "artist": artist,
            "album": album,
            "label": label,
            "genre": genre,
            "link": link,
            "lede": lede,
            "rating": rating,
            "index": "{}. ".format(ix + 1),
        }

        print_record(**entry)
