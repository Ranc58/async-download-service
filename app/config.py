import os

CONFIG = {
    'host': os.environ.get('HOST', 'localhost'),
    'port': int(os.environ.get('PORT', 8080)),
    'logging': os.environ.get('LOGGING'),
    'response_timeout': float(os.environ.get('RESPONSE_TIMEOUT', 0.001)),
    'photos_path': os.environ.get('PHOTOS_PATH', f'{os.getcwd()}/test_photos')
}
