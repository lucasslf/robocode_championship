def init_web(app):
    from robot_service.api import robot
    app.register_blueprint(robot.bp)
