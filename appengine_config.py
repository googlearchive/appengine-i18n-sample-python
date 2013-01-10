
from i18n_utils import I18nMiddleware

def webapp_add_wsgi_middleware(app):
    app = I18nMiddleware(app)
    return app
