import re
import itertools
import threading
import time
import sys

from termcolor import colored
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager


ua = UserAgent()


class Animate:
    def __init__(
        self,
        fn,
        msg,
        linewidth=80,
        trailing_newline=False,
        animations=["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"],
    ):
        self.fn = fn
        self.msg = msg
        self._is_done = False
        self.animations = animations
        self.linewidth = linewidth
        self.newline = "\n" if trailing_newline is True else ""

    def animate(self):
        for c in itertools.cycle(self.animations):
            if self._is_done:
                break
            c = colored(c, "blue", attrs=["bold"])
            sys.stdout.write(f"\r {c} {self.msg}")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write("\r" + (" " * self.linewidth) + self.newline)

    def __call__(self):
        self.thread = threading.Thread(target=self.animate, daemon=True)
        self.thread.start()
        fn_out = self.fn()
        self.stop()
        self.thread.join()
        return fn_out

    def stop(self):
        self._is_done = True


def initialize_webdriver():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument(f"--user-agent={ua.random}")
    driver = webdriver.Chrome(
        options=options, executable_path=ChromeDriverManager(log_level=0).install()
    )
    return driver


def render_html(url, driver):
    agent = {"userAgent": ua.random}  # randomize user-agent
    driver.execute_cdp_cmd("Network.setUserAgentOverride", agent)
    driver.get(url)
    return driver.page_source


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
