
import gettext
import os

import webapp2
from webob.acceptparse import AcceptLanguage


def convert_translations_to_dict(js_translations):
    plural = None
    n_plural = 2
    if '' in js_translations._catalog:
        for l in js_translations._catalog[''].split('\n'):
            if l.startswith('Plural-Forms:'):
                plural = l.split(':', 1)[1].strip()
    if plural is not None:
        for element in map(unicode.strip, plural.split(';')):
            if element.startswith('nplurals='):
                n_plural = int(element.split('=', 1)[1])
            elif element.startswith('plural='):
                plural = element.split('=', 1)[1]
    else:
        n_plural = 2
        plural = '(n == 1) ? 0 : 1'

    translations_dict = {'plural': plural, 'catalog': {}, 'fallback': None}
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
                translations_dict['catalog'][k[0]] = [''] * n_plural
            translations_dict['catalog'][k[0]][int(k[1])] = v
    return translations_dict


class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2_env(self):

        import jinja2
        jinja2_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                os.path.join(os.path.dirname(__file__), 'templates')),
            extensions=['jinja2.ext.i18n'])
        jinja2_env.install_gettext_translations(
            self.request.environ['active_translation'])
        jinja2_env.globals['get_i18n_js_tag'] = self.get_i18n_js_tag
        return jinja2_env

    def get_i18n_js_tag(self):
        template = self.jinja2_env.get_template('javascript_tag.jinja2')
        return template.render({'javascript_body': self.get_i18n_js()})

    def get_i18n_js(self):
        import json

        try:
            js_translations = gettext.translation(
                'jsmessages', 'locales', fallback=False,
                languages=self.request.environ['preferred_languages'],
                codeset='utf-8')
        except IOError:
            template = self.jinja2_env.get_template('null_i18n_js.jinja2')
            return template.render()

        translations_dict = convert_translations_to_dict(js_translations)
        template = self.jinja2_env.get_template('i18n_js.jinja2')
        return template.render(
              {'translations': json.dumps(translations_dict, indent=1)})


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
