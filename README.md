# daa-competition - Дизайн и анализ на алгоритми - състезание

Състезание по алгоритми.
Потребителите ще могат да се логват, регистрират, пращат решения
на python писани (на които ще се опитвам да им меря сложността, памет,
коректност на изходните данни) и накрая да показвам класацията след като
мине времето за изпращане на решения.

#Quick Pyramid installation

```bash
python3.4 -c 'import setuptools' &&
wget https://raw.githubusercontent.com/doitwrong/daa-competition/master/requirements/ez_setup.py &&
python3.4 ez_setup.py &&
easy_install virtualenv &&
export VENV=~/env &&
virtualenv $VENV &&
$VENV/bin/easy_install "pyramid==1.5.7" &&
rm ez_setup.py

```

#Project setup and run

```bash
git clone https://github.com/doitwrong/daa-competition &&
cd daa-competition/ &&
$VENV/bin/python setup.py test -q &&
$VENV/bin/python setup.py develop &&
$VENV/bin/pserve development.ini --reload

```