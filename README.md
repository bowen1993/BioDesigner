# BioDesigner

[![Build Status](https://travis-ci.org/ideaworld/BioDesigner.svg)](https://travis-ci.org/ideaworld/BioDesigner)

[![Coverage Status](https://coveralls.io/repos/ideaworld/BioDesigner/badge.svg?branch=master&service=github)](https://coveralls.io/github/ideaworld/BioDesigner?branch=master)

Synthetic Biology Design toolkit

##System Environments Requires

Python 2.7 or later(Python 3 is not supported)
Java version "1.8.0_20" or later
pip 1.5.6 or later
MySQL 5.6.20 or later

##Package Requires

####Django
####mysql-python
####elasticsearch
####Pillow

##Set up steps

Django install: 

	pip install Django==$DJANGO_VERSION
	
Mysql-python install:

	pip install MySQL-python
	
Elasticsearch install & run:

	wget https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.7.2.zip
	unzip elasticsearch-1.7.2.zip
	./elasticsearch-1.7.2/bin/elasticsearch -d
	
	

Pillow

	pip install pillow
	
Database import

	mysql -e 'CREATE DATABASE biodesigner'
	python manage.py syncdb --noinput
	mysql -e 'source xxx.sql' -u username --password=password biodesigner;

> sql source file can downloads from github
	
Run server

	python manage.py runserver 0.0.0.0:{port number}


