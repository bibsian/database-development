#!/usr/bin/env python
# Adopted from
# https://simpletutorials.com/
# c/1457/Python+3+Logging+using+DictConfig
import logging
import logging.config

def configure_logger(name, log_path):
    logging.config.dictConfig({
        'version': 1,
        'formatters':{
            'tableformat': {
                'format': '%(asctime)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'}
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'tableformat'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'tableformat',
                'filename': log_path
            }
        },
        'loggers':{
            'tableformat': {
                'level': 'DEBUG',
                'handlers': ['console', 'file']
            }
        },
        'disable_existing_loggers': False
    })
    return logging.getLogger(name)


