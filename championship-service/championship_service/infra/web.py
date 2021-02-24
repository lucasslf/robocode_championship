def init_web(app):
    from championship_service.api import championship_api
    app.register_blueprint(championship_api.bp)
