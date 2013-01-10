appengine-i18n-sample-python
============================

A small sample showing how to build an internationalized app with App Engine.

What to internationalize
------------------------

There are lots of things to internationalize.

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

This example only covers first 3 basic strings. In order to cover other
aspects, I recommend using [Babel](http://babel.edgewall.org/) and [pytz]
(http://pypi.python.org/pypi/gaepytz). Also, you may want to use
[webapp2_extras.i18n](http://webapp-improved.appspot.com/tutorials/i18n.html)
module.


TODO
----

- Write README
- Add command lines for managements to README
- Add lazy_gettext
- Use memcache for translations
