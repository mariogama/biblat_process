# -*- coding: utf-8 -*-
import os

"""
    Archivo de configuración de biblat_process

    Variables de entorno:
        - BIBLATP_REMOTE_ADDR: Dirección IP del servidor ALEPH
        - BIBLATP_REMOTE_USER: Usuario del servidor ALEPH
        - BIBLATP_REMOTE_PATH: Directorio remoto para descargar datos
        - BIBLATP_LOCAL_PATH: Directorio local para guardar los datos
"""

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))


class Config:
    REMOTE_USER = os.environ.get('BIBLATP_REMOTE_USER', 'aleph')
    REMOTE_ADDR = os.environ.get('BIBLATP_REMOTE_ADDR', '127.0.0.1')
    REMOTE_PATH = os.environ.get(
        'BIBLATP_REMOTE_PATH',
        '/exlibris/aleph/a21_1/alephm/sql_report/anexo/biblat_process'
    )
    LOCAL_PATH = os.environ.get('BIBLATP_LOCAL_PATH',
                                os.path.join(SCRIPT_PATH, '../data'))
    DB_FILES = ['cla01.txt.gz', 'per01.txt.gz']


class DevelopmentConfig(Config):
    LOCAL_PATH = os.path.abspath(os.path.join(SCRIPT_PATH, '../data'))


class TestingConfig(Config):
    LOCAL_PATH = os.path.abspath(
        os.path.join(SCRIPT_PATH, '../tests/test_files')
    )


class ProductionConfig(Config):
    LOCAL_PATH = os.path.abspath(os.path.join(SCRIPT_PATH, '../data'))


settings_selector = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

config = settings_selector[os.getenv('BIBLAT_PROCESS_CONFIG', 'default')]
