from ext.flask_uploads import UploadSet, configure_uploads

robot_files = UploadSet('robots', ('jar',))


def init_upload(app):
    configure_uploads(app, (robot_files,))
