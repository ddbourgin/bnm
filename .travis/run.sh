#!/usr/bin/env bash

if [ "$TRAVIS_OS_NAME" == "osx" ]; then
    export PYENV_VERSION=$PYTHON
    export PATH="/Users/travis/.pyenv/shims:${PATH}"
    pyenv virtualenv venv
    source venv/bin/activate
    tox --skip-missing-interpreters
else
    tox
fi
