Envconnect webapp
=================

This Django project contains the web application for the enviro-connect project.

Prerequisites
-------------

    $ make require

Install
-------

    $ make install
    $ make initdb


Development setup: Step-by-step
-------------------------------

    $ virtualenv envconnect
    $ source envconnect/bin/activate
    $ mkdir -p envconnect/reps
    $ cd envconnect/reps
    $ git clone https://github.com/djaodjin/envconnect.git
    $ cd envconnect
    $ ../../bin/pip install -r requirements.txt -r dev-requirements.txt
    $ make install
    $ make initdb
    $ make vendor-assets-prerequisites NPM=npm
    $ diff -u ../../etc/envconnect/site.conf
    -DEBUG=False
    +DEBUG=True
    $ pushd ../../bin
    $ ln -s ../reps/envconnect/node_modules/less/bin/lessc
    $ popd

    $ python manage.py runserver
    # browser http://localhost:8000/envconnect/
