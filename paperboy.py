import logging
import os
from datetime import datetime
from logging.config import dictConfig

import requests
import sendgrid
from bs4 import BeautifulSoup
from sendgrid.helpers.mail import Email, Content, Mail


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


SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
TO_EMAILS = os.environ.get('TO_EMAILS', '').split(',')


class Paperboy():
    def __init__(self, today=None, dry=True):
        self.today = today or datetime.now().strftime('%Y%m%d')
        self.url = f'http://www.wsj.com/itp/{today}/us/whatsnews'

        self.dry = dry

        self.headers = {
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/69.0.3497.100 Safari/537.36'
            )
        }

        self.sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

    def is_story(self, tag):
        return tag.name == 'p' and not tag.text.startswith('Subscriber Content')

    def extract_stories(self, soup, css_class):
        column = soup.find('div', class_=css_class)

        # find() returns None if it can't find a match
        if not column:
            return

        stories = column.find_all(self.is_story)

        return [story.text.strip() for story in stories]

    def deliver(self):
        response = requests.get(self.url, headers=self.headers)
        logger.info(f'{self.url} GET {response.status_code}')

        soup = BeautifulSoup(response.text, 'html.parser')

        business_finance_stories = self.extract_stories(soup, 'mod_contentCol-1')
        world_stories = self.extract_stories(soup, 'mod_contentCol-2')

        if not (business_finance_stories and world_stories):
            logger.info('no news today')
            return

        sg_from_email = Email('whatsnews@paperboy.com')
        # TODO: prettier date
        sg_subject = f"What's News for {self.today}"

        business_finance_content = '\n\n'.join(['# Business and Finance'] + business_finance_stories)
        world_content = '\n\n'.join(['# World'] + world_stories)

        # TODO: html email
        # TODO: incorporate on-this-day note (days repo) at the end
        content = f'{world_content}\n\n{business_finance_content}'
        sg_content = Content('text/plain', content)

        if self.dry:
            print(content)

        for to_email in TO_EMAILS:
            if self.dry:
                logger.info(f'would send to {to_email}')
            else:
                sg_to_email = Email(to_email)
                mail = Mail(sg_from_email, sg_subject, sg_to_email, sg_content)
                response = self.sg.client.mail.send.post(request_body=mail.get())
                logger.info(f'sendgrid email to {to_email} with status {response.status_code}')


def deliver():
    try:
        # Paperboy(dry=False).deliver()

        # results
        Paperboy(today='20181113', dry=False).deliver()

        # no results
        # Paperboy(today='20181112').deliver()
    except:
        logger.exception('something went wrong')


def exception_handler(*args, **kwargs):
    # prevents invocation retry
    return True


if __name__ == '__main__':
    deliver()
