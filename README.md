# appengine-i18n-sample-python

A simple example app showing how to build an internationalized app
with App Engine. The main purpose of this example is to provide how,
and the second goal is to collect feedback from developers in order to
improve our SDK.

## What to internationalize

There are lots of things to internationalize with your web
applications.

1.  Strings in python code
2.  Strings in HTML template
3.  Strings in javascript
4.  Common strings
    - Country Names, Language Names, etc.
5.  Formatting
    - Date/Time formatting
    - Number formatting
    - Currency
6.  Timezone conversion

This example only covers first 3 basic scenarios above. In order to
cover other aspects, I recommend using
[Babel](http://babel.edgewall.org/) and [pytz]
(http://pypi.python.org/pypi/gaepytz). Also, you may want to use
[webapp2_extras.i18n](http://webapp-improved.appspot.com/tutorials/i18n.html)
module.

## Wait, so why not webapp2_extras.i18n?

webapp2_extras.i18n doesn't cover how to internationalize strings in
javascript code. And it depends on babel and pytz, which means you
need to deploy babel and pytz alongside with your code. I'd like to
show a reasonably minimum example for string internationalization in
Python code, jinja2 templates, as well as javascript.


## How to run this example

First of all, please install babel in your local python environment.

### Wait, you just said I don't need babel, are you crazy?

As I said before, you don't need to deploy babel with your
application, but you need to locally use pybabel script which is
provided by babel distribution in order to extract the strings, manage
and compile the translations file.

### Extract strings in Python code and Jinja2 templates to translate

Move into this project directory and invoke the following command:

    $ env PYTHONPATH=/google_appengine_sdk/lib/jinja2 \
        pybabel extract -o locales/messages.pot -F main.mapping .

Since the babel configration file `main.mapping` contains a reference
to `jinja2.ext.babel_extract` helper function which is provided by
jinja2 distribution bundled with the App Engine SDK, you need to add a
PYTHONPATH environment variable pointing to the jinja2 directory in
the SDK.

### Manage and compile translations.

Create an initial translation source by the following command:

    $ pybabel init -l ja -d locales -i locales/messages.pot

Open `locales/ja/LC_MESSAGES/messages.po` with any text editor and
translate the strings, then compile the file by the following command:

    $ pybabel compile -d locales

If any of the strings changes, you can extract the strings again, and
update the translations by the following command:

    $ pybabel update -l ja -d locales -i locales/messages.pot

Note: If you run `pybabel init` against an existant translations file,
you will lose your translations.


### Extract strings in javascript code and compile translations

    $ pybabel extract -o locales/jsmessages.pot -F js.mapping .
    $ pybabel init -l ja -d locales -i locales/jsmessages.pot -D jsmessages

Open `locales/ja/LC_MESSAGES/jsmessages.po` and translate it.

    $ pybabel compile -d locales -D jsmessages


TODO
----

- Write README
  - Add lazy_gettext
  - Use memcache for translations
