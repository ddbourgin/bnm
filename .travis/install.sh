#!/usr/bin/env bash

echo '[Running install.sh]'
if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    brew update
    brew install openssl readline
    brew outdated pyenv || brew upgrade pyenv
    brew install pyenv-virtualenv
    pyenv install $PYENV_VERSION
    export PATH="/Users/travis/.pyenv/shims:${PATH}"
    pyenv virtualenv venv
    source venv/bin/activate
    wget -qO- https://bootstrap.pypa.io/get-pip.py | python

    # A manual check that the correct version of Python is running.
    echo $(python --version)
    pip install tox-travis
else
    sudo apt-get update
    pip install tox-travis
fi
