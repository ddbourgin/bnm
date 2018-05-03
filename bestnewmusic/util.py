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
        return render(query_url)


def try_except(f, field):
    try:
        out = f()
    except (AttributeError, TypeError, IndexError) as e:
        out = 'Unknown {}'.format(field)
    return out
