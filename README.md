# Fractale

Défi de la semaine, fractale

# Dépendances

- Pillow, `pip install pillow`

# Installation

    mkdir python
    cd python
    wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz
    tar -xf Python-3.6.8.tgz
    cd Python-3.6.8
    ./configure --enable-optimizations
    make
    make altinstall
    pip3.6 install pipenv
    cd ..
    git clone https://moriya.zapto.org/LCI/fractale.git
    cd fractale
    pipenv install
    cd sources
    pipenv run betterTurtle.py