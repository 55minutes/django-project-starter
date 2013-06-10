# django-project-template

An opinionated project template for Django 1.5.1 featuring:

* Proven project layout
* [PostgreSQL][]
* [Asset pipeline][django-pipeline] to preprocess, merge, minify, and cache
  bust your CSS, JavaScript, and images
* [Livereload][] to automatically refresh your desktop and mobile browsers when
  you change your presentation related files
* Automatically regenerates [ctags][] when any `.py` files change
* Optimized for development on OS X, but should work in most Linux environments
  well
* Deploy to a [DigitalOcean][] Ubuntu 12.04 droplet

## Sounds good, how do I get started?

1.  Make sure you have everything installed and working:
    * [virtualenv][]
    * [virtualenvwrapper][]
    * [rvm][] or [rbenv][] with ruby-2.0.0-p195
    * [Node.js][]
    * [PostgreSQL][]
2.  Set up your Python virtual environment:
    ```bash
    mkdir icecream
    cd icecream
    mkvirtualenv -a `pwd` icecream-dev
    add2virtualenv `pwd`
    ```
3.  Install Django:
    ```bash
    pip install django
    ```
4.  Star a new project in your working directory:
    ```bash
    django-admin.py startproject \
      --template=https://github.com/55minutes/django-project-template/archive/master.zip \
      --extension=py,md,html --name=local_setup icecream .
    ```
5.  Set up the development environment and start the Django development server:
    ```bash
    source bin/local_setup
    django-admin.py runserver 0.0.0.0:8000
    ```
6.  Start Guard in another shell:
    ```bash
    guard
    ```
7.  Point your browsers at <http://localhost:8000> and you should see the
    sample template rendered.
8.  When you make changes to anything in the following directories, your
    browsers should automatically refresh:
    * ice_cream/templates
    * ice_cream/static

*Note: these instructions show creation of a project called "**icecream**".
You should replace this name with the actual name of your project.*

---

## Dependencies

Most of the dependencies have been captured in the template itself. However,
some of the dependencies require you to set up:

* **Python**: Yes, it comes with OS X, but *please* don't use the built-in
  Python to do your development. Instead, install Python from [Homebrew][]. Be
  sure to familiarize yourself with how [Python works with
  Homebrew][homebrew-python].
* **[virtualenv][] and [virtualenvwrapper][]**: Python development environment.
  Just use [pip][] to install these.
* **[rvm][] or [rbenv][] with ruby-2.0.0-p195**: Yes, Ruby in your Django
  project. We use [Guard][] and its various plugins to perform tasks
  automatically when we edit files.
* **[Node.js][]**: We use tools such as [LESS][] and [yUglify][], which are
  Node.js packages.
* **[PostgreSQL][]**: You should develop on the same DB as production. Also,
  you should use Homebrew for your PostgreSQL installation.

## Create the working environment

Use [virtualenvwrapper][] to take care of managing your virtual environments
and adding the package path to `site-packages` for you:

```bash
mkdir icecream
cd icecream
mkvirtualenv -a `pwd` icecream-dev
add2virtualenv `pwd`
```

The working directory `icecream` is associated with the icecream-dev
virtualenv, and is added to `sys.path`.

See the documentation for [mkvirtualenv][] and [add2virtualenv][] for more
details.

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
  --template=https://github.com/55minutes/django-project-template/archive/master.zip \
  --extension=py,md,html --name=local_setup icecream .
```

## Set up the development environment

```bash
source bin/local_setup
```

We need to `source` the set up script in order to set the
`$DJANGO_SETTINGS_MODULE` environment variable.

You'll want to modify this script for your own needs. The supplied script is a
starting point for bootstrapping the development environment of your specific
project. The idea is that any developer should be able to check out your code,
run this script, and be ready to go.

I try to do as little as possible in the script, delegating most of the heavy
lifting to [Fabric][]. If you're doing serious Django development, you'll want
to learn Fabric.

Running the script out of the box will:

1.  Install Python dependencies
2.  Generate Django `settings.py`
3.  Generate `.ruby-gemset`
4.  Generate `Guardfile`
5.  Generate `postactivate` and `postdeactivate` scripts for the virtualenv
6.  Set `$DJANGO_SETTINGS_MODULE`
7.  Install Ruby dependencies
8.  Install Node.js dependencies
9.  Create the development database
10. Create the `STATIC_ROOT` directory

## Acknowledgements

* [Two Scoops of Django](https://django.2scoops.org)

[DigitalOcean]: https://www.digitalocean.com
[Guard]: https://github.com/guard/guard
[Homebrew]: http://mxcl.github.io/homebrew/
[PostgreSQL]: http://www.postgresql.org
[Vagrant]: http://www.vagrantup.com
[add2virtualenv]: http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html#add2virtualenv
[ctags]: http://ctags.sourceforge.net
[django-pipeline]: https://pypi.python.org/pypi/django-pipeline/
[fabric]: http://fabfile.org
[homebrew-python]: https://github.com/mxcl/homebrew/wiki/Homebrew-and-Python
[livereload]: https://github.com/guard/guard-livereload
[mkvirtualenv]: http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html#mkvirtualenv
[node.js]: http://nodejs.org
[pip]: https://pypi.python.org/pypi/pip
[rbenv]: https://github.com/sstephenson/rbenv
[rvm]: https://rvm.io
[virtualenv]: http://www.virtualenv.org
[virtualenvwrapper]: https://bitbucket.org/dhellmann/virtualenvwrapper/
[less]: http://lesscss.org
[yuglify]: https://github.com/yui/yuglify#readme
