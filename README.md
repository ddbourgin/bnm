# bestnewmusic
[![TravisCI](https://travis-ci.org/ddbourgin/bestnewmusic.svg)](https://travis-ci.org/ddbourgin/bestnewmusic)

View recent highly rated albums in the terminal. 

![bnm](images/bnm.gif "bnm p4k")

`bnm` supports the following sources:
- [Pitchfork 8.0+ Albums](https://pitchfork.com/best/high-scoring-albums/)
- [Resident Advisor Recommends](https://www.residentadvisor.net/reviews.aspx?format=recommend)
- [Forced Exposure Best Sellers](https://forcedexposure.com/Best/BestIndex.html)
- [Boomkat Best Sellers](https://boomkat.com/bestsellers)
- [Midheaven Weekly Best Sellers](https://www.midheaven.com/top-selling)
- [Stranded Recommended Records](https://www.strandedrecords.com/collections/recommended)
- [WFMU Heavily Played Records](http://www.wfmu.org/Playlists/Wfmu/#t)
- [KALX Weekly Top 35](https://www.kalx.berkeley.edu/charts/top-35)

## Installation
Install with pip:
```
pip install bestnewmusic
```

## Usage
```
usage: bnm [-h] [-r] [-l LENGTH] {p4k, ra, bk, mh, fe, sd, wfmu, kalx}

positional arguments:
  {p4k,ra,bk,mh,fe,sd,wfmu,kalx}
    - p4k  : Pitchfork 8.0+ Albums
    - ra   : Resident Advisor Recommends
    - bk   : Boomkat Weekly Best Sellers
    - mh   : Midheaven Weekly Best Sellers
    - fe   : Forced Exposure Weekly Best Sellers
    - sd   : Stranded Recommended Records
    - wfmu : WFMU Weekly Charts
    - kalx : KALX Weekly Charts

optional arguments:
  -h, --help            Show this help message and exit
  -r, --reverse         Display items in reverse order (with most recent last)
  -l, --length          Number of items to display
```

## Example
Show the WFMU weekly play charts for the current week, organized by frequency:
```bash
bnm wfmu
```
Show the first five most recent 8.0+ albums on Pitchfork (incl. reissues):
```bash
bnm p4k -l 5
```
Show the weekly bestsellers on Forced Exposure, ordered from least to most
popular:
```bash
bnm fe -r
```
