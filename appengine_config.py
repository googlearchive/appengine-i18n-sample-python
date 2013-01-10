
def webapp_add_wsgi_middleware(app):
    from i18n_utils import I18nMiddleware
    app = I18nMiddleware(app)
    return app
