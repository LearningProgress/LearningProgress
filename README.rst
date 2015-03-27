==================
 LearningProgress
==================

.. image:: https://img.shields.io/travis/LearningProgress/LearningProgress.svg?
   :target: https://travis-ci.org/LearningProgress/LearningProgress

.. image:: https://img.shields.io/coveralls/LearningProgress/LearningProgress.svg?
   :target: https://coveralls.io/r/LearningProgress/LearningProgress

.. image:: https://img.shields.io/badge/license-MIT-blue.svg?
   :target: http://opensource.org/licenses/MIT

LearningProgress is a small server application based on Django for tracking
individual learning progress on a structured curriculum. It is still under
development.


Run development version
=======================

*Be sure you have Python 3.3 or higher installed. You also need Python
header files and a static library for proper compiling the ReportLab PDF
Library during install.*

*Ubuntu 12.04 is not supported. If you want to use it anyway, try your very
best.*

::

    $ python3 --version  # This should return Python 3.3.x or higher
    $ git clone https://github.com/LearningProgress/LearningProgress.git
    $ cd LearningProgress
    $ virtualenv .virtualenv --python=python3
    $ source .virtualenv/bin/activate
    $ pip install -r requirements.txt
    $ python manage.py migrate
    $ python manage.py createsuperuser  # Prompts for some input.
    $ python manage.py loaddata extras/example-data-de.json
    $ python manage.py runserver


Requirements
============

LearningProgress uses

* `Python <https://www.python.org/>`_ 3.3.x or higher
* `Django <https://www.djangoproject.com/>`_ 1.7.x
* `django-mptt <https://github.com/django-mptt/django-mptt/>`_ 0.6.1
* `Constance - Dynamic Django settings <https://github.com/jezdez/django-constance/>`_ 1.0.x
* `django-picklefield <https://github.com/gintas/django-picklefield/>`_ 0.3.1
* `Six <https://pythonhosted.org/six/>`_ 1.9.0
* `Reportlab <http://www.reportlab.com/>`_ 3.1.x
* `django-bootstrap3 <https://github.com/dyve/django-bootstrap3/>`_ 5.2.x
* `Bootstrap <http://getbootstrap.com/>`_ 3.3.4
* `jQuery <https://jquery.com/>`_ 1.11.2
* `jQuery Form Plugin <http://malsup.com/jquery/form/>`_ 3.51
* `CKEditor <http://ckeditor.com/>`_ 4.4.7


License
=======

LearningProgress is Free/Libre Open Source Software and distributed under
the MIT License, see LICENSE file. The authors are mentioned in the AUTHORS
file.
