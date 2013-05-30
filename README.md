# django-project-starter

A project template for Django 1.5.1.

To use this project follow these steps:

1.  Create your working environment
2.  Install Django
3.  Create the new project using the django-project-starter template
4.  Set up the development environment
5.  Develop away!

*note: these instructions show creation of a project called "**icecream**".
You should replace this name with the actual name of your project.*

## Dependencies

Using this template requires [virtualenv][] and [virtualenvwrapper][].

Trust us, you'll want to use them anyway.

## Create the working environment

Use [virtualenvwrapper][] to take care of managing your virtual environments
and adding the package path to `site-packages` for you:

```bash
mkdir icecream
cd icecream && mkvirtualenv -a `pwd` icecream-dev
add2virtualenv `pwd`
```

See the documentation for [mkvirtualenv][] and [add2virtualenv][] for details
of what's going on.

## Install Django

To install Django in the new virtual environment, run the following command:

```bash
pip install django
```

## Create your project

To create a new Django project called "**icecream**" using
django-project-template, run the following command:

```bash
django-admin.py startproject \
  --template=https://github.com/55minutes/django-project-starter/archive/basic.zip \
  --extension=py,md,html --name=local_setup icecream .
```

## Set up and test the development environment

```bash
source bin/local_setup
```

Now test to make sure your Django project is up and running:

```bash
django-admin.py runserver
```

You should be able to point your browser at <http://localhost:8000> and see the
rendered example template.

Now go make something amazing using Django!

## Acknowledgements

* [Two Scoops of Django](https://django.2scoops.org)

[virtualenv]: http://www.virtualenv.org
[virtualenvwrapper]: https://bitbucket.org/dhellmann/virtualenvwrapper/
[mkvirtualenv]: http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html#mkvirtualenv
[add2virtualenv]: http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html#add2virtualenv
