# bestnewmusic
[![TravisCI](https://travis-ci.org/ddbourgin/bestnewmusic.svg)](https://travis-ci.org/ddbourgin/bestnewmusic)

View recent highly rated albums in the terminal. 

![bnm](images/bnm.gif "bnm p4k")

`bnm` supports the following sources:
- [Pitchfork 8.0+ Albums](https://pitchfork.com/best/high-scoring-albums/)
- [Resident Advisor Recommends](https://www.residentadvisor.net/reviews.aspx?format=recommend)
- [AllMusic Editor's Choice](https://www.allmusic.com/newreleases/editorschoice)
- [Forced Exposure Best Sellers](https://forcedexposure.com/Best/BestIndex.html)
- [Boomkat Best Sellers](https://boomkat.com/bestsellers)
- [Midheaven Weekly Best Sellers](https://www.midheaven.com/top-selling)
- [WFMU Heavily Played Records](http://www.wfmu.org/Playlists/Wfmu/#t)

## Installation
### OSX
Some commands use Selenium and chromedriver to render Javascript-driven pages. On OSX, the easiest way to install these (if you don't have them already) is to use homebrew:
```
brew update
brew cask install google-chrome
```
then
```
pip install bestnewmusic
```

### Ubuntu
Install the [google-chrome-stable](https://www.ubuntuupdates.org/ppa/google_chrome?dist=stable) package from the Google Linux repo:
```
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - 
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt-get update 
sudo apt-get install google-chrome-stable
```

Install `bnm` with pip:
```
pip install bestnewmusic
```

## Usage
#### AllMusic Editor's Choice
```bash
bnm am
```
#### Resident Advisor Recommends
```bash
bnm ra
```
#### Forced Exposure Best Sellers
```bash
bnm fe
```
#### Pitchfork 8.0+ Reviews
```bash
bnm p4k
```
#### Boomkat Best Sellers
```bash
bnm bk
```

#### Midheaven Best Sellers
```bash
bnm mh
```

#### WFMU Heavily Played Records
```bash
bnm wfmu
```
