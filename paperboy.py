import logging
# import os
from datetime import datetime
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


class Paperboy():
    # 20180403 - results
    # 20181111 - no results
    def __init__(self, today=None):
        today = today or datetime.now().strftime('%Y%m%d')
        self.url = f'http://www.wsj.com/itp/{today}/us/whatsnews'

        self.headers = {
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/69.0.3497.100 Safari/537.36'
            )
        }

    def is_story(self, tag):
        return tag.name == 'p' and not tag.text.startswith('Subscriber Content')

    def extract_stories(self, soup, css_class):
        column = soup.find('div', class_=css_class)
        stories = column.find_all(self.is_story)

        return [story.text.strip() for story in stories]

    def deliver(self):
        response = requests.get(self.url, headers=self.headers)
        logger.info(f'{self.url} GET {response.status_code}')

        soup = BeautifulSoup(response.text, 'html.parser')

        # TODO: format and email these!
        business_finance_stories = self.extract_stories(soup, 'mod_contentCol-1')
        world_stories = self.extract_stories(soup, 'mod_contentCol-2')


def deliver():
    try:
        Paperboy(today='20180403').deliver()
    except:
        logger.exception('something went wrong')


def exception_handler(*args, **kwargs):
    # prevents invocation retry
    return True


if __name__ == '__main__':
    deliver()
