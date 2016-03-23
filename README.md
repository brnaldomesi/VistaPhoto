# Vistagrid

[![Build Status](https://travis-ci.org/andela-lkabui/checkpoint4.svg?branch=develop)](https://travis-ci.org/andela-lkabui/checkpoint4)
[![Coverage Status](https://coveralls.io/repos/github/andela-lkabui/checkpoint4/badge.svg?branch=develop)](https://coveralls.io/github/andela-lkabui/checkpoint4?branch=develop)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/54a4decaa92b4d2483d7a1c3c42f79c0/badge.svg)](https://www.quantifiedcode.com/app/project/54a4decaa92b4d2483d7a1c3c42f79c0)

## Introduction
*  **`Vistagrid`** is a Django Powered Photo Editing App.
*  It has the following features;
  *  Login via Facebook
  *  Allows uploading of images in a non-blocking manner
  *  Allows users to edit uploaded images using effects and filters including;
    *  Contours
    *  Image Sharpening
    *  Image Blur
    *  Image Detail
    *  Image Emboss
    *  Image Smoothening
  *  Allows users to share uploaded images on Facebook via a public url

## Dependencies

### Back End Dependencies
*  This app's functionality depends on multiple Python packages including;
  *  **[Django](https://www.djangoproject.com/)** - This framework helps is essential in the creation of  object relational models and it also handles routing on the back end.
  *  **[Django Rest Framework](http://www.django-rest-framework.org/)** - This is a powerful and flexible toolkit used for building web browsable REST APIs. It is through this framework that the serializers, viewsets and viewset permissions are made possible
  *  **[python-social-auth](https://github.com/omab/python-social-auth)** - This package provides a social authentication/ registration mechanism and has support for various auth providers, including Facebook, Twitter, Dropbox, Github among others. For this app, it was used to intergrate Facebook authentication.
  *  **[Pillow](https://pillow.readthedocs.org/en/3.1.x/)** - This is an active fork of the now discontinued Python Imaging Library. Pillow is the workhorse behind all the image manipulation capabilities in this app.
  *  **[ipdb](https://pypi.python.org/pypi/ipdb)** - The Python debugger. Very handy during the development process.
  *  **[autoenv](https://github.com/kennethreitz/autoenv)** - This package provides directory based environments. For this app, SOCIAL_AUTH_FACEBOOK_KEY`, `SOCIAL_AUTH_FACEBOOK_SECRET (python-social-auth) and SECRET_KEY (Django) were set as environment variables and utilized this package's features.
  *  **[fake-factory](https://pypi.python.org/pypi/fake-factory/0.5.5)** - Used during the creation of Effect objects so as to give random names to files. This feature is essential to trigger refresh of effect previews in the dashboard view whenever an upload is clicked.
  *  **[coverage](https://pypi.python.org/pypi/coverage)** - A tool for measuring code coverage in Python tests. This measurement is typically used to gauge the effectiveness of tests
  *  **[DJ-Static](https://github.com/kennethreitz/dj-static)** - A simple Django middleware utility that allows you to properly serve static assets from production with a WSGI server like Gunicorn.

## Front End Dependencies
*  **[Materialize CSS](http://materializecss.com/)** - The app's login and dashboard templates have been styled using this CSS framework
*  **[Angular JS](https://angularjs.org/)** - This framework facilitates the dynamic aspects of this app. It enables the application of the Single Page Application philosophy and also has mechanisms to make calls to the backend to update the view with recent data.
  *  Angular Resource - This is an Angular component that is particularly useful when making calls to a RESTful route.
  *  Angular Cookies - An Angular component that provides read/write access to a browser's cookies.
*  **[ng-file-upload](https://github.com/danialfarid/ng-file-upload)** - This library is an angular component that enables file (images in this case) upload and also features a service that enables posting of these uploads to the back end.
*  **[Sweet Alert](http://t4t5.github.io/sweetalert/)** - This alert framework is used to display warning alerts to the user when he/she is about to delete an upload or save changes after edit.
*  **[Font Awesome](https://fortawesome.github.io/Font-Awesome/)** - Iconic font and css toolkit.

## Installation and setup
*  Navigate to a directory of choice on `terminal`.
*  Clone this repository on that directory.
  *  Using SSH;

    >`git clone git@github.com:andela-lkabui/checkpoint4.git`

  *  Using HTTP;

    >`https://github.com/andela-lkabui/checkpoint4.git`

*  Navigate to the repo's folder on your computer
  *  `cd checkpoint4/`
*  Install the app's backend dependencies. For best results, using a [virtual environment](http://virtualenv.readthedocs.org/en/latest/installation.html) is recommended.
  *  `pip install -r requirements`
*  Install the app's database. The default `SQLite` was used for development.
*  Install the app's front end dependencies using bower.
  *  `./node_modules/bower/bin/bower install`

    >In order to use bower, you need to install it through **npm**. You also need to have **node** and **git** installed on your system.

*  Create and apply migrations
  *  `python manage.py makemigrations app`
  *  `python manage.py migrate app`
* Run the app
  *  `python manage.py runserver`
  *  Running the command above will produce output that's similar to the sample below.

  ```
    System check identified 1 issue (0 silenced).
    March 13, 2016 - 18:16:59
    Django version 1.9.2, using settings 'vistagrid.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
  ```

## Tests
*  The tests have been written using Django's **[TestCase](https://docs.djangoproject.com/en/1.9/topics/testing/overview/)** class.
*  They are run using the **`coverage`** tool in order to generate test coverage reports.
*  To run the tests, navigate to the project's root folder (where `requirements.txt` file is located.)
*  Issue the following command on terminal.
  *  `coverage run manage.py test`
*  If the tests are successful, they will complete without failures or errors.

  ```
  .........
  ----------------------------------------------------------------------
  Ran 9 tests in 1.064s

  OK
  ```

*  To view test coverage statistics, run the following command;
  *  `coverage report -m`
  * Below is a sample of the output from the command above.

  ```
    Name                                                         Stmts   Miss  Cover   Missing
    ------------------------------------------------------------------------------------------
    app/__init__.py                                                  0      0   100%
    app/admin.py                                                     3      0   100%
    app/models.py                                                   40      4    90%   32-36
	  							.
								.
								.
    vistagrid/__init__.py                                            0      0   100%
    vistagrid/settings.py                                           26      0   100%
    vistagrid/urls.py                                                8      1    88%   33
    ------------------------------------------------------------------------------------------
    TOTAL                                                          342     31    91%
  ```
