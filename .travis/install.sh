#!/usr/bin/env bash

echo '[Running install.sh]'
if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    brew update
    brew cask install google-chrome
    brew install openssl readline
    brew outdated pyenv || brew upgrade pyenv
    brew install pyenv-virtualenv
    pyenv install $PYENV_VERSION
    export PATH="/Users/travis/.pyenv/shims:${PATH}"
    pyenv-virtualenv venv
    source venv/bin/activate
    wget -qO- https://bootstrap.pypa.io/get-pip.py | python

    # A manual check that the correct version of Python is running.
    echo $(python --version)
else
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - 
    sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
    sudo apt-get update
    sudo apt-get install unzip google-chrome-stable xvfb
fi
