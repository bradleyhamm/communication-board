from comboard import comboard_app

DATABASE_FILE = 'data.db'

comboard_app.config['DATABASE'] = DATABASE_FILE
comboard_app.config['MAX_IMAGE_SIZE'] = 4 * 1024 * 1024
