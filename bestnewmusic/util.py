import re


def render(query_url, page_load_timeout=30):
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    browser = webdriver.Chrome(chrome_options=options)
    browser.set_page_load_timeout(page_load_timeout)

    try:
        browser.get(query_url)
        html_source = browser.page_source
        browser.quit()
        return html_source

    except TimeoutException:
        return render(query_url)


def try_except(f, field):
    try:
        out = f()
    except (AttributeError, TypeError, IndexError):
        out = "Unknown {}".format(field)
    return out


def strip_unprintable(s):
    return "".join(c for c in s if c.isprintable())


def strip(s):
    return strip_unprintable(s).strip()


# match any space-hyphen-space (" - ") sequence
SPACE_HYPHEN_SPACE = re.compile(
    r"\s[\u002D\u058A\u05BE\u1400\u1806\u2010-\u2015\u2E17\u2E1A\u2E3A\u2E3B\u2E40\u301C\u3030\u30A0\uFE31\uFE32\uFE58\uFE63\uFF0D]\s"
)

# match any hyphen-space ("- ") sequence
HYPHEN_SPACE = re.compile(
    r"[\u002D\u058A\u05BE\u1400\u1806\u2010-\u2015\u2E17\u2E1A\u2E3A\u2E3B\u2E40\u301C\u3030\u30A0\uFE31\uFE32\uFE58\uFE63\uFF0D]\s"
)
