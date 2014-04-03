==================
 LearningProgress
==================

.. image:: https://travis-ci.org/LearningProgress/LearningProgress.svg?branch=master
   :target: https://travis-ci.org/LearningProgress/LearningProgress

.. image:: https://coveralls.io/repos/LearningProgress/LearningProgress/badge.png?branch=master
   :target: https://coveralls.io/r/LearningProgress/LearningProgress

LearningProgress is a small server application based on Django for tracking
individual learning progress on a structured curriculum. It is still under
development.


Run development version
=======================

::

    $ python3 --version  # This should return Python 3.x
    $ git clone https://github.com/LearningProgress/LearningProgress.git
    $ cd LearningProgress
    $ virtualenv .virtualenv --python=python3
    $ source .virtualenv/bin/activate
    $ pip install -r requirements.txt
    $ python manage.py syncdb  # Prompts for input some superuser data.
    $ python manage.py loaddata extras/example-data.json
    $ python manage.py runserver


Requirements
============

LearningProgress uses

* `Python <https://www.python.org/>`_ 3.x
* `Django <https://www.djangoproject.com/>`_ 1.6.x
* `django-mptt <https://github.com/django-mptt/django-mptt/>`_ 0.6.0
* `django-bootstrap3 <https://github.com/dyve/django-bootstrap3/>`_ 3.2.x
* `Bootstrap <http://getbootstrap.com/>`_ 3.1.1
* `jQuery <https://jquery.com/>`_ 1.11.0
* `jQuery Form Plugin <http://malsup.com/jquery/form/>`_ v20140218
* `Coverage.py <http://nedbatchelder.com/code/coverage/>`_ 3.7.1

License
=======

LearningProgress is Free/Libre Open Source Software and distributed under
the MIT License, see LICENSE file. The authors are mentioned in the AUTHORS
file.
