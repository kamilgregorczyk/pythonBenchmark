#!/usr/bin/env bash
cd $HOME
apt-get update
apt-get upgrade
apt-get install zsh
apt-get install git-core
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install python3.7
apt-get install python3-pip
pip3 install --upgrade pip
pip3 install virtualenv
pip3 install virtualenvwrapper
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.5
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv -p python3.7 python_benchmark
workon python_benchmark

git clone https://github.com/zemirco/sf-city-lots-json.git
git clone https://github.com/kamilgregorczyk/pythonBenchmark.git
cp sf-city-lots-json/citylots.json pythonBenchmark/test.json
cd pythonBenchmark
apt-get install python3.7-dev
pip install -r requirements.txt
python main.py