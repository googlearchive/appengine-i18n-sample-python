#!/usr/bin/env python
#
# Copyright 2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A small example showing how to build an i18n app with App Engine."""


import webapp2

from i18n_utils import BaseHandler


class MainHandler(BaseHandler):
    """A simple handler demonstrating how to i18n in Python, Jinja2 and
    Javascript.
    """

    def get(self):
        """A get handler for this sample."""

        context = dict(message=gettext('Hello World from Python code!'))
        template = self.jinja2_env.get_template('index.jinja2')
        self.response.out.write(template.render(context))


application = webapp2.WSGIApplication([
      ('/', MainHandler),
], debug=True)
