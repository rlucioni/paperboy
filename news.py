import logging
import os
from datetime import datetime, timedelta
from logging.config import dictConfig

import requests
from bs4 import BeautifulSoup


dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '{asctime} {levelname} {process} [{filename}:{lineno}] - {message}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
})

logger = logging.getLogger(__name__)


NEWS_URL = 'http://www.wsj.com/itp/20181110/us/whatsnews'


def check():
    try:
        pass
    except:
        logger.exception('something went wrong')


def exception_handler(*args, **kwargs):
    # prevents invocation retry
    return True


if __name__ == '__main__':
    check()
