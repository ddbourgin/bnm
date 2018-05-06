#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    brew update;
    brew cask install google-chrome;
else
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - ;
    sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list';
    sudo apt-get update;
    sudo apt-get install unzip google-chrome-stable xvfb;
fi
