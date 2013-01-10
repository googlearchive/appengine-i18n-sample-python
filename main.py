
import webapp2

from i18n_utils import BaseHandler

class MainHandler(BaseHandler):

    def get(self):
        context = {
            'message': gettext('Hello World!'),
        }
        template = self.jinja2_env.get_template('index.jinja2')
        self.response.out.write(template.render(context))


application = webapp2.WSGIApplication([
        ('/', MainHandler),
], debug=True)
