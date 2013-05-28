# django-project-starter

A project template for Django 1.5.1. In addition to the basic Django
infranstructure, this template also includes:

1.  A [Vagrant][] configuration file for use with [Digital Ocean][].

To use this project follow these steps:

1.  Create your working environment
2.  Install Django
3.  Create the new project using the django-project-starter template
4.  Set up the development environment
5.  Develop away!

*note: these instructions show creation of a project called "icecream".  You
should replace this name with the actual name of your project.*

# Working Environment

You have several options in setting up your working environment.  We recommend
using [virtualenv][] to seperate the dependencies of your project from your
system's python environment.  If on Linux or Mac OS X, you can also use
[virtualenvwrapper][] to help manage multiple virtualenvs across different
projects.

## Virtualenv Only

First, make sure you are using [virtualenv][]. Once that's installed, create
your virtualenv:

    $ virtualenv --distribute icecream

You will also need to ensure that the virtualenv has the project directory
added to the path. Adding the project directory will allow `django-admin.py` to
be able to change settings using the `--settings` flag.

## Virtualenv with virtualenvwrapper

In Linux and Mac OSX, you can install [virtualenvwrapper][], which will take
care of managing your virtual environments and adding the project path to the
`site-directory` for you:

    $ mkdir icecream
    $ mkvirtualenv -a icecream icecream-dev
    $ cd icecream && add2virtualenv `pwd`


# Installing Django

To install Django in the new virtual environment, run the following command::

    $ pip install django

# Creating your project

To create a new Django project called '**icecream**' using
django-twoscoops-project, run the following command::

    $ django-admin.py startproject \
        --template=https://github.com/55minutes/django-project-starter/archive/vagrant-digitalocean.zip \
        --extension=py,md,html --name=setup_dev icecream

# Set up the development environment

    bin/setup_dev


# Acknowledgements

* [Two Scoops of Django](https://django.2scoops.org)

[Vagrant]: http://www.vagrantup.com
[Digital Ocean]: https://www.digitalocean.com
[virtualenv]: http://www.virtualenv.org
[virtualenvwrapper]: https://bitbucket.org/dhellmann/virtualenvwrapper/
