import logging
import pickle
import time

import requests
from bs4 import BeautifulSoup

from constant import (CHECK_FOR_UPDATES_INTERVAL_IN_SECONDS,
                      SAFE_COUNTRIES_LIST_PICKLE_FILE_NAME, GMAIL_SMTP_SENDER_ACCOUNT_USERNAME)
from notification_utils import gmail_notification

logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    logging.info('test {}'.format(GMAIL_SMTP_SENDER_ACCOUNT_USERNAME))
    while True:
        try:
            safe_countries_up_until_now = pickle.load(open(SAFE_COUNTRIES_LIST_PICKLE_FILE_NAME, 'rb'))
        except FileNotFoundError:
            safe_countries_up_until_now = []
        safe_countries_now = []
        page = requests.get('https://www.gov.uk/guidance/coronavirus-covid-19-travel-'
                            'corridors#countries-and-territories-with-no-self-isolation-'
                            'requirement-on-arrival-in-england', timeout=5)
        soup = BeautifulSoup(page.text, 'html.parser')
        safe_countries_section = soup.select_one('#countries-and-territories-with-no-self-isolation-requirement-on-'
                                                 'arrival-in-england')
        # I am sure that there is some more elegant way to do this
        safe_countries_list_on_website = safe_countries_section.find_next('ul')
        for country in safe_countries_list_on_website:
            if hasattr(country, 'text'):
                safe_countries_now.append(country.text)
        safe_countries_list_changed = len(safe_countries_up_until_now) > 0 \
            and safe_countries_up_until_now != safe_countries_now
        if safe_countries_list_changed:
            logging.info('safe country list changed.')
            countries_changed = [country for country in safe_countries_up_until_now + safe_countries_now if country not in
                                 safe_countries_up_until_now or country not in safe_countries_now]
            notification_message = ''
            for country_changed in countries_changed:
                if country_changed not in safe_countries_up_until_now:
                    notification_message += '{} was added to the safe countries list./n'.format(country_changed)
                else:
                    notification_message += '{} was removed from the safe countries list./n'
            logging.info(notification_message)
            gmail_notification(notification_message)
        else:
            logging.info('safe country list did not change.')
        pickle.dump(safe_countries_now, open(SAFE_COUNTRIES_LIST_PICKLE_FILE_NAME, "wb"))
        logging.info('waiting {} seconds until the next check.'.format(CHECK_FOR_UPDATES_INTERVAL_IN_SECONDS))
        time.sleep(CHECK_FOR_UPDATES_INTERVAL_IN_SECONDS)

