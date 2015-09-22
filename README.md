# BioDesigner

[![Build Status](https://travis-ci.org/ideaworld/BioDesigner.svg)](https://travis-ci.org/ideaworld/BioDesigner)

[![Coverage Status](https://coveralls.io/repos/ideaworld/BioDesigner/badge.svg?branch=master&service=github)](https://coveralls.io/github/ideaworld/BioDesigner?branch=master)

Synthetic Biology Design toolkit


Installation Guide
---------

> **NOTE:**
> 
> - We're going to assume that you have installed Python 2 and MySQL 5.x and git on your computer.


####Download source code from github

git clone https://github.com/igemsoftware/HFUT-China_2015

git checkout master


#### Install Django
1. Install `pip`
   
   For Unbuntu/Mint Users:
   ```
   apt-get install python-pip
   ```

   Or you can get standalone [pip installer](http://www.pip-installer.org/en/latest/installing.html#using-the-installer).

2. Install Django using `pip`

   For users who has installed `pip`
   
   ```
   pip install django==1.7.6
   ```
   Or you can install Django manually.

    > **Tip:** Know more information on install Django at https://docs.djangoproject.com/en/1.6/intro/install/
    
3.Install additional mysql & python dev lib

	sudo apt-get install python-dev libmysqlclient-dev    
    
#### Set up BioDesigner
1. Open `BioDesigner/settings.py`.
2. Edit your database configuration at line 67.

#### Set up Database
1. To connect MySQL in Python, we need install `mysql-python` first.
   You can install it using `pip`:

   ```
   pip install mysql-python
   ```
   
   > **Tip:** If you get error message like this: `EnvironmentError: mysql_config not found`. 
   
   > **Reference:** http://stackoverflow.com/questions/7475223/mysql-config-not-found-when-installing-mysqldb-python-interface

2. Create database named `biodesigner` in MySQL.

3. Database import
```
	cd /path/to/the/app
	sudo mysql -e 'CREATE DATABASE biodesigner'
	python manage.py syncdb --noinput
	sudo mysql -e 'source xxx.sql' -u username --password=password biodesigner;
```
#### Install Additional Package
1.Pillow
```
	pip install pillow
```

2. Install Elasticsearch

   For Ubuntu/Mint Users:
   Elasticsearch is running on Java, if you don't have a JRE on your machine, please install one.
   
   For example, We use OpenJDK7:
   ```
   apt-get install openjdk-7-jre
   ```
   
   Download and install the Public Signing Key
   ```
   wget -qO - http://packages.elasticsearch.org/GPG-KEY-elasticsearch | sudo apt-key add -
   ```
   
   Add the following to your /etc/apt/sources.list to enable the repository
   ```
   deb http://packages.elasticsearch.org/elasticsearch/1.3/debian stable main
   ```
   
   Run apt-get update and the repository is ready for use. You can install it with :
   ```
   apt-get install elasticsearch
   ```

   For RHEL/CentOS Users:
   Download and install the Public Signing Key
   ```
   rpm --import http://packages.elasticsearch.org/GPG-KEY-elasticsearch
   ```
   Add the following in your /etc/yum.repos.d/ directory in a file named (for example) elasticsearch.repo
   ```
   [elasticsearch-1.3]
   name=Elasticsearch repository for 1.3.x packages
   baseurl=http://packages.elasticsearch.org/elasticsearch/1.3/centos
   gpgcheck=1
   gpgkey=http://packages.elasticsearch.org/GPG-KEY-elasticsearch
   enabled=1
   ```
   
   And your repository is ready for use. You can install it with :
   ```
   yum install elasticsearch
   ```

   Install Elasticsearch bind for python:
   ```
   pip install elasticsearch
   ```

#### Start Server
1. If you want to use this application on a production site, use Apache with mod_wsgi. 
   > **Tip**: Get more information at https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/modwsgi/

2. If you just want to experiment with this application, just use following command:
   
   ```
   python manage.py runserver
   ```
   If you will get following output,
   ```
   May 14, 2014 - 04:50:57
   Django version 1.6.4, using settings 'BioDesigner.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.
   ```
   The application is deployed successfully. And you can use the application by visit http://127.0.0.1:8000 in web browser.

