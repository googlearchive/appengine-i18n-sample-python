
import gettext
import os

import webapp2
from webob.acceptparse import AcceptLanguage

JAVASCRIPT_HEAD = r'''
<script type="text/javascript">
'''

TRANSLATIONS_INIT = r'''
var translations = %s;
'''

JAVASCRIPT_FOOT = r'''
</script>
'''

I18N_JAVASCRIPT_NULL = r'''
function gettext(s) { return s; };
function ngettext(singular, plural, count) {
  return (count == 1) ? singular :plural;
}
'''

I18N_JAVASCRIPT = r'''
function get_value_from_translations(translations, msgid) {
  var ret = translations['catalog'][msgid]
  if (typeof(ret) == 'undefined' &&
      typeof(translations['fallback']) != 'undefined') {
      ret = get_value_from_translations(translations['fallback'], msgid);
  }
  return ret;
}

function plural_index(count, translations) {
  var s = 'var n = ' + count + '; var v = ' + translations['plural'];
  eval(s);
  return v;
}

function gettext(msgid) {
  var value = get_value_from_translations(translations, msgid);

  if (typeof(value) == 'undefined') {
    return msgid;
  } else {
    return (typeof(value) == 'string') ? value : value[0];
  }
}

function ngettext(singular, plural, count) {
  var value = get_value_from_translations(translations, singular);

  if (typeof(value) == 'undefined') {
    return (count == 1) ? singular : plural;
  } else {
    return value[plural_index(count, translations)];
  }
}
'''

STRING_FORMAT = r'''
String.prototype.format = function() {
  var args = arguments;
  return this.replace(/{(\d+)}/g, function(match, number) {
    return typeof args[number] != 'undefined'
      ? args[number]
      : match
    ;
  });
};
'''

def convert_translations_to_dict(js_translations):
    plural = None
    nplural = 2
    if '' in js_translations._catalog:
        for l in js_translations._catalog[''].split('\n'):
            if l.startswith('Plural-Forms:'):
                plural = l.split(':',1)[1].strip()
    if plural is not None:
        for element in map(unicode.strip, plural.split(';')):
            if element.startswith('nplurals='):
                nplural = int(element.split('=',1)[1])
            elif element.startswith('plural='):
                plural = element.split('=', 1)[1]
    else:
        nplural = 2
        plural = '(n == 1) ? 0 : 1'

    translations_dict = {}
    translations_dict['plural'] = plural
    translations_dict['catalog'] = {}
    if js_translations._fallback is not None:
        translations_dict['fallback'] = convert_translations_to_dict(
            js_translations._fallback
        )
    for k, v in js_translations._catalog.items():
        if k == '':
            continue
        if type(k) in (str, unicode):
            translations_dict['catalog'][k] = v
        elif type(k) == tuple:
            if not k[0] in translations_dict['catalog']:
                translations_dict['catalog'][k[0]] = [''] * nplural
            translations_dict['catalog'][k[0]][int(k[1])] = v
    return translations_dict


class BaseHandler(webapp2.RequestHandler):
    @property
    def jinja2_env(self):
        if hasattr(self, '_jinja2_env'):
            return self._jinja2_env

        import os
        import jinja2
        jinja2_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                os.path.join(os.path.dirname(__file__), 'templates')),
            extensions=['jinja2.ext.i18n'])
        jinja2_env.install_gettext_translations(
            self.request.environ['active_translation'])
        jinja2_env.globals['get_i18n_js_tag'] = self.get_i18n_js_tag
        self._jinja2_env = jinja2_env
        return jinja2_env

    def get_i18n_js_tag(self):
        return JAVASCRIPT_HEAD + self.get_i18n_js() + JAVASCRIPT_FOOT

    def get_i18n_js(self):
        import json

        try:
            js_translations = gettext.translation(
                'jsmessages', 'locales', fallback=False,
                languages=self.request.environ['preferred_languages'],
                codeset='utf-8')
        except IOError:
            return I18N_JAVASCRIPT_NULL + STRING_FORMAT

        translations_dict = convert_translations_to_dict(js_translations)
        return TRANSLATIONS_INIT % json.dumps(translations_dict, indent=1) +\
               I18N_JAVASCRIPT + STRING_FORMAT



class I18nMiddleware(object):

    def __init__(self, app, default_language='en', locale_path=None):
        self.app = app
        if locale_path is None:
            locale_path = os.path.join(
                os.path.abspath(os.path.dirname(__file__)), 'locales')
        self.locale_path = locale_path
        self.default_language = default_language

    def __call__(self, environ, start_response):
        accept_language = AcceptLanguage(
            environ.get("HTTP_ACCEPT_LANGUAGE", self.default_language))
        preferred_languages = accept_language.best_matches()
        if not self.default_language in preferred_languages:
            preferred_languages.append(self.default_language)
        translation = gettext.translation(
            'messages',self.locale_path, fallback=True,
            languages=preferred_languages, codeset='utf-8')
        translation.install(unicode=True, names=['gettext', 'ngettext'])
        environ['active_translation'] = translation
        environ['preferred_languages'] = preferred_languages

        return self.app(environ, start_response)
