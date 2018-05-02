# bestnewmusic
Linux/OSX: [![TravisCI](https://travis-ci.org/ddbourgin/bestnewmusic.svg)](https://travis-ci.org/ddbourgin/bestnewmusic)
Windows: [![AppVeyor](https://ci.appveyor.com/api/projects/status/github/ddbourgin/bestnewmusic?svg=True)](https://ci.appveyor.com/project/ddbourgin/bestnewmusic)

View recent highly rated albums in the terminal. 

![bnm](images/bnm.gif "bnm p4k")

Lists are compiled from:
- [Pitchfork 8.0+ Albums](https://pitchfork.com/best/high-scoring-albums/)
- [Resident Advisor Recommends](https://www.residentadvisor.net/reviews.aspx?format=recommend)
- [AllMusic Editor's Choice](https://www.allmusic.com/newreleases/editorschoice)
- [Forced Exposure Best Sellers](https://forcedexposure.com/Best/BestIndex.html)
- [Boomkat Best Sellers](https://boomkat.com/bestsellers)

## Insallation
### OSX
Some commands use chromedriver with Selenium to render webpages. On OSX, the easiest way to install these (if you don't have them already) is to use homebrew:
```
brew update
brew cask install google-chrome
```
then
```
pip install bestnewmusic
```

### Ubuntu
Install the [google-chrome-stable](https://www.ubuntuupdates.org/ppa/google_chrome?dist=stable) package from 3rd party repo:
```
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - 
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt-get update 
sudo apt-get install unzip google-chrome-stable xvfb libxi6 libgconf-2-4
```

Install chromedriver and the bestnewmusic package with pip:
```
pip install bestnewmusic
```

## Usage
### AllMusic Editor's Choice
```bash
bnm am
```
### Resident Advisor Recommends
```bash
bnm ra
```
### Forced Exposure Best Sellers
```bash
bnm fe
```
### Pitchfork 8.0+ Reviews
```bash
bnm p4k
```
### Boomkat Best Sellers
```bash
bnm bk
```
